from flask_restful import Resource, reqparse
from server.flask import broker

# 1 - Exponer un endpoint REST para agregar productos en una ubicación.
#   a. Se nos indicará el Depósito, producto, cantidad y ubicación donde quiere colocar.
#   b. Validar que la dirección tenga el patrón correcto.
#   c. Que el producto/item sea almacenado en nuestros depósitos.
#   d. No se pueden colocar más de 3 productos distintos en una ubicación.
class Agregar(Resource):
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument("deposito", required=True)
        parser.add_argument("ubicacion", required=True)
        parser.add_argument("producto", required=True)
        parser.add_argument("cantidad", required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        code, message, data = broker.add_producto(
            args["deposito"],
            args["ubicacion"],
            args["producto"],
            args["cantidad"],
        )

        return {"mensaje": message, "data": data}, code
