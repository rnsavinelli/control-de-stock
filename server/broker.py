import os
from server.sqlite import SQLite
import traceback
from server.log import log
from server.ubicacion import Ubicacion


class Broker:
    def __init__(self, database_file):
        self.database = SQLite(database_file)
        self.locator = Ubicacion()

    def _bundle(self, data, description):
        payload = list()

        if data != []:
            for values in data:
                keys = map(lambda x: x[0], description)
                payload.append(dict(zip(list(keys), list(values))))

            return payload

        else:
            return []

    def get_cantidad_de_producto(self, producto, deposito, ubicacion):
        try:
            area, pasillo, fila, cara = self.locator.parse(ubicacion)

            data, description, _ = self.database.select(
                "CANTIDAD",
                "PRODUCTO_POR_DEPOSITO",
                f'ID_PRODUCTO={int(producto)} AND ID_DEPOSITO="{str(deposito)}" AND AREA="{str(area)}" \
                    AND PASILLO={int(pasillo)} AND FILA={int(fila)} AND CARA="{str(cara)}"',
            )

            result = self._bundle(data, description)

            if result != []:
                return result[0]["CANTIDAD"]

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))

        return -1

    def get_productos(self, deposito, ubicacion):
        try:
            area, pasillo, fila, cara = self.locator.parse(ubicacion)

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 406, str(e), {}

        try:
            data, description, _ = self.database.select(
                "*",
                "PRODUCTO_POR_DEPOSITO",
                f'ID_DEPOSITO="{str(deposito)}" AND AREA="{str(area)}" AND PASILLO={int(pasillo)} \
                    AND FILA={int(fila)} AND CARA="{str(cara)}"',
            )

            result = self._bundle(data, description)

            if result != []:
                return 200, "Productos encontrados", result

            else:
                return 404, "No se encontraron productos", {}

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}

    def get_producto_segun_deposito(self, identifier, deposito):
        try:
            data, description, _ = self.database.select(
                "*",
                "PRODUCTO_POR_DEPOSITO",
                f'ID_PRODUCTO={int(identifier)} AND ID_DEPOSITO="{str(deposito)}"',
            )

            result = self._bundle(data, description)

            if result != []:
                return 200, "Productos encontrados", result

            else:
                return 404, "No se encontraron productos", {}

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}

    def retirar_cantidad_de_producto(self, producto, deposito, ubicacion, cantidad):
        try:
            area, pasillo, fila, cara = self.locator.parse(ubicacion)

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 406, str(e), {}

        try:
            self.database.update(
                "PRODUCTO_POR_DEPOSITO",
                f"CANTIDAD=CANTIDAD-{int(cantidad)}",
                f'ID_PRODUCTO={int(producto)} AND ID_DEPOSITO="{str(deposito)}" AND AREA="{str(area)}" \
                    AND PASILLO={int(pasillo)} AND FILA={int(fila)} AND CARA="{str(cara)}"',
            )

            return 200, "El stock fue actualizado", {}

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}

    def add_producto(self, deposito, ubicacion, producto, cantidad):
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
