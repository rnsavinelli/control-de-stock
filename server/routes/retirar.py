from flask_restful import Resource
from server.flask import broker


# 2 - Exponer un endpoint para poder retirar productos de una ubicación.
# Se nos indicará el depósito, producto, cantidad y ubicación de donde sacarla.
class Retirar(Resource):
    def get(self, deposito, ubicacion, producto, cantidad):
        if cantidad < 0:
            return {
                "mensaje": "No se admiten cantidades negativas",
                "data": {},
            }, 406

        cantidad_disponible = broker.get_cantidad_de_producto(
            producto, deposito, ubicacion
        )

        if cantidad_disponible == -1:
            return {"mensaje": "Producto no encontrado", "data": {}}, 404

        if (cantidad_disponible > 0) and (cantidad_disponible - cantidad) >= 0:
            code, message, data = broker.retirar_cantidad_de_producto(
                producto, deposito, ubicacion, cantidad
            )

            return {"mensaje": message, "data": data}, code

        else:
            return {"mensaje": "No hay stock suficiente", "data": {}}, 406
