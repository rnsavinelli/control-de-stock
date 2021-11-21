from flask_restful import Resource
import traceback
from log import log
from broker import Broker
from ubicacion import Ubicacion


# 2 - Exponer un endpoint para poder retirar productos de una ubicación.
# Se nos indicará el depósito, producto, cantidad y ubicación de donde sacarla.
class Retirar(Resource):
    broker = Broker()
    locator = Ubicacion()

    def get(self, deposito, ubicacion, producto, cantidad):
        try:
            if cantidad > 0:
                cantidad_disponible = self.broker.get_cantidad_de_producto(
                    producto, deposito, ubicacion)

                if (cantidad_disponible >
                        0) and (cantidad_disponible - cantidad) >= 0:

                    if (self.broker.retirar_cantidad_de_producto(
                            producto, deposito, ubicacion, cantidad) == 0):
                        return {
                            "mensaje": "El stock fue actualizado",
                            "data": {}
                        }, 200

                    else:
                        return {
                            "mensaje": "Producto no encontrado",
                            "data": {}
                        }, 404

                else:
                    return {
                        "mensaje": "No hay stock suficiente",
                        "data": {}
                    }, 406

            else:
                return {
                    "mensaje": "No se admiten cantidades negativas",
                    "data": {}
                }, 406

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return {"mensaje": "Error interno del servidor", "data": {}}, 500

    def post(self):
        pass
