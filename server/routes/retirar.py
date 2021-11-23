from flask_restful import Resource
import traceback

from server.logger import log
from server.endpoint import Endpoint

# 2 - Exponer un endpoint para poder retirar productos de una ubicación.
# Se nos indicará el depósito, producto, cantidad y ubicación de donde sacarla.
class Retirar(Resource, Endpoint):
    def get(self, deposito, ubicacion, producto, cantidad):
        if cantidad < 0:
            return {
                "mensaje": "No se admiten cantidades negativas",
                "data": {},
            }, 406

        cantidad_disponible = self._get_cantidad_de_producto(
            producto, deposito, ubicacion
        )

        if cantidad_disponible == -1:
            return {"mensaje": "Producto no encontrado", "data": {}}, 404

        if (cantidad_disponible > 0) and (cantidad_disponible - cantidad) >= 0:
            code, message, data = self._retirar_cantidad_de_producto(
                producto, deposito, ubicacion, cantidad
            )

            return {"mensaje": message, "data": data}, code

        else:
            return {"mensaje": "No hay stock suficiente", "data": {}}, 406

    def _retirar_cantidad_de_producto(self, producto, deposito, ubicacion, cantidad):
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

    def _get_cantidad_de_producto(self, producto, deposito, ubicacion):
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
