from flask_restful import Resource
from server.flask import broker


# 3 - Exponer un endpoint de lectura. Se nos indica un depósito y una ubicación, y este
# liste los productos y cantidad que hay en el mismo.
class Productos(Resource):
    def get(self, deposito, ubicacion):
        code, message, data = broker.get_productos(deposito, ubicacion)

        return {"mensaje": message, "data": data}, code

    def post(self):
        pass


class Producto(Resource):
    def get(self, identifier):
        code, message, data = broker.get_producto(identifier)

        return {"mensaje": message, "data": data}, code

    def post(self):
        pass
