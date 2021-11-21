from flask_restful import Resource, reqparse
import traceback
from log import log
from broker import Broker
from ubicacion import Ubicacion

# 3 - Exponer un endpoint de lectura. Se nos indica un depósito y una ubicación, y este
# liste los productos y cantidad que hay en el mismo.
class Productos(Resource):
    broker = Broker()
    locator = Ubicacion()

    def get(self):
        pass

    def get(self, deposito, ubicacion):
        try:
            area, pasillo, fila, cara = self.locator.parse(ubicacion)
            data = self.broker.get_productos(deposito, area, pasillo, fila, cara)

            if data == []:
                return {
                    'mensaje': 'Productos no encontrados', 
                    'data': []
                }, 404

            return {
                'mensaje': 'Productos encontrados', 
                'data': data
            }, 200 

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return {'mensaje': 'Error interno del servidor', 'data': {}}, 500                

    def post(self):
        pass    

class Producto(Resource):
    broker = Broker()
    
    def get(self, identifier):
        
        try:
            data = self.broker.get_producto_por_id(identifier)

            if data == {}:
                return {
                    'mensaje': 'Producto no encontrado', 
                    'data': []
                }, 404

            return {
                'mensaje': 'Producto encontrado', 
                'data': data
            }, 200 

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return {'mensaje': 'Error interno del servidor', 'data': {}}, 500           

    def post(self):
        pass