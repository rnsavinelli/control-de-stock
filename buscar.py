from flask_restful import Resource
import traceback
from log import log
from broker import Broker

# 4 - Exponer un endpoint de búsqueda. Se nos indica el depósito y producto, y este nos
# devuelva las posibles ubicaciones y cantidad en las mismas.
class Buscar(Resource):
    broker = Broker()

    def get(self, identifier, deposito):
        try:
            data = self.broker.get_producto_segun_deposito(identifier, deposito)

            if data == []:
                return {"mensaje": "Producto no encontrado", "data": {}}, 404

            return {"mensaje": "Producto encontrado", "data": data}, 200

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return {"mensaje": "Error interno del servidor", "data": {}}, 500

    def post(self):
        pass
