from flask_restful import Resource
from server.flask import broker


# 4 - Exponer un endpoint de búsqueda. Se nos indica el depósito y producto, y este nos
# devuelva las posibles ubicaciones y cantidad en las mismas.
class Buscar(Resource):
    def get(self, identifier, deposito):
        code, message, data = broker.get_producto_segun_deposito(identifier, deposito)

        return {"mensaje": message, "data": data}, code
