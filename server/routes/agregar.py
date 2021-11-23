from flask_restful import Resource, reqparse
import traceback

from server.logger import log
from server.endpoint import Endpoint

# 1 - Exponer un endpoint REST para agregar productos en una ubicación.
#   a. Se nos indicará el Depósito, producto, cantidad y ubicación donde quiere colocar.
#   b. Validar que la dirección tenga el patrón correcto.
#   c. Que el producto/item sea almacenado en nuestros depósitos.
#   d. No se pueden colocar más de 3 productos distintos en una ubicación.
class Agregar(Resource, Endpoint):
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument("deposito", required=True)
        parser.add_argument("ubicacion", required=True)
        parser.add_argument("producto", required=True)
        parser.add_argument("cantidad", required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        code, message, data = self._add_producto(
            args["deposito"],
            args["ubicacion"],
            args["producto"],
            args["cantidad"],
        )

        return {"mensaje": message, "data": data}, code

    def _add_producto(self, deposito, ubicacion, producto, cantidad):
        # BO Validar que la dirección tenga el patrón correcto.
        try:
            area, pasillo, fila, cara = self.locator.parse(ubicacion)

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 406, str(e), {}
        # EO Validar que la dirección tenga el patrón correcto.

        # BO Validar que el producto/item sea almacenado en nuestros depósitos.
        try:
            data, description, _ = self.database.select(
                "*", "PRODUCTO", f"ID={int(producto)}"
            )

            n_entries = len(self._bundle(data, description))

            if n_entries == 0:
                return 404, "Producto no encontrado", {}

            table_producto = self._bundle(data, description)

            if table_producto[0]["ALMACENAMIENTO"] != "fullfilment":
                return 406, "El producto no se encuentra en nuestros depósitos", {}

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}
        # EO Validar que el producto/item sea almacenado en nuestros depósitos.

        # BO No colocar más de 3 productos distintos en una ubicación.
        try:
            data, description, _ = self.database.select(
                "*",
                "PRODUCTO_POR_DEPOSITO",
                f'ID_DEPOSITO="{str(deposito)}" AND AREA="{str(area)}" AND PASILLO={int(pasillo)} \
                    AND FILA={int(fila)} AND CARA="{str(cara)}"',
            )

            entries = self._bundle(data, description)
            n_entries = len(entries)

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}

        if not (
            (int(producto) in [x["ID_PRODUCTO"] for x in entries]) or (n_entries < 3)
        ):
            return 406, "No pueden almacenarse más productos en esta ubicación", {}
        # EO No colocar más de 3 productos distintos en una ubicación.

        # BO La suma de las cantidades de los productos que hubiera en una ubicación no puede ser mayor a 100 unidades.
        cantidad_almacenada = sum(entry["CANTIDAD"] for entry in entries)

        if cantidad_almacenada + int(cantidad) > 100:
            return (
                406,
                f"Solo queda espacio para {100 - cantidad_almacenada} productos en esta ubicación",
                {},
            )
        # EO La suma de las cantidades de los productos que hubiera en una ubicación no puede ser mayor a 100 unidades.

        try:
            args = {
                "ID_PRODUCTO": producto,
                "ID_DEPOSITO": deposito,
                "AREA": area,
                "PASILLO": pasillo,
                "FILA": fila,
                "CARA": cara,
                "CANTIDAD": cantidad,
            }

            _, _, rowcount = self.database.update(
                "PRODUCTO_POR_DEPOSITO",
                f"CANTIDAD=CANTIDAD + {int(cantidad)}",
                f'ID_PRODUCTO={int(producto)} AND ID_DEPOSITO="{str(deposito)}" AND AREA="{str(area)}" \
                    AND PASILLO={int(pasillo)} AND FILA={int(fila)} AND CARA="{str(cara)}"',
            )

            if rowcount == 0:
                self.database.write_table("PRODUCTO_POR_DEPOSITO", args)

            return 200, "La base de datos fue actualizada", {}

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}
