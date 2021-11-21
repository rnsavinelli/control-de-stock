from flask_restful import Resource
from broker import Broker


# 2 - Exponer un endpoint para poder retirar productos de una ubicación.
# Se nos indicará el depósito, producto, cantidad y ubicación de donde sacarla.
class Retirar(Resource):
    broker = Broker()

    def get(self, deposito, ubicacion, producto, cantidad):
        if cantidad > 0:
            cantidad_disponible = self.broker.get_cantidad_de_producto(
                producto, deposito, ubicacion
            )

            if cantidad_disponible == -1:
                return {"mensaje": "Producto no encontrado", "data": {}}, 404

            if (cantidad_disponible > 0) and (cantidad_disponible - cantidad) >= 0:
                code, message, data = self.broker.retirar_cantidad_de_producto(
                    producto, deposito, ubicacion, cantidad
                )

                return {"mensaje": message, "data": data}, code

            else:
                return {"mensaje": "No hay stock suficiente", "data": {}}, 406

        else:
            return {
                "mensaje": "No se admiten cantidades negativas",
                "data": {},
            }, 406

    def post(self):
        pass
