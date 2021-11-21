from flask_restful import Resource
import traceback
from log import log
from broker import Broker


# 3 - Exponer un endpoint de lectura. Se nos indica un depósito y una ubicación, y este
# liste los productos y cantidad que hay en el mismo.
class Productos(Resource):
    broker = Broker()

    def get(self):
        pass

    def get(self, deposito, ubicacion):
        try:
            data = self.broker.get_productos(deposito, ubicacion)

            if data == []:
                return {"mensaje": "No se encontraron productos", "data": {}}, 404

            return {"mensaje": "Productos encontrados", "data": data}, 200

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return {"mensaje": "Error interno del servidor", "data": {}}, 500

    def post(self):
        pass


class Producto(Resource):
    broker = Broker()

    def get(self, identifier):

        try:
            data = self.broker.get_producto(identifier)

            if data == []:
                return {"mensaje": "Producto no encontrado", "data": {}}, 404

            return {"mensaje": "Producto encontrado", "data": data}, 200

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return {"mensaje": "Error interno del servidor", "data": {}}, 500

    def post(self):
        pass
