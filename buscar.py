from flask_restful import Resource
import traceback
from log import log
from broker import Broker

# 4 - Exponer un endpoint de búsqueda. Se nos indica el depósito y producto, y este nos
# devuelva las posibles ubicaciones y cantidad en las mismas.
class Buscar(Resource):
    broker = Broker()

    def get(self, identifier, deposito):
        code, message, data = self.broker.get_producto_segun_deposito(
            identifier, deposito
        )

        return {"mensaje": message, "data": data}, code

    def post(self):
        pass
