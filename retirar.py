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
                area, pasillo, fila, cara = self.locator.parse(ubicacion)
                cantidad_disponible = self.broker.get_cantidad_de_producto(producto, deposito, area, pasillo, fila, cara)

                if (cantidad_disponible > 0) and (cantidad_disponible - cantidad) >= 0:

                    if self.broker.retirar_cantidad_de_producto(producto, deposito, area, pasillo, fila, cara, cantidad) == 0:
                        return {
                            'message': 'El stock fue actualizado', 
                            'data': []
                        }, 200

                    else:
                        return {
                            'message': 'Producto no encontrado', 
                            'data': []
                        }, 404           

                else:
                    return {
                        'message': 'No hay stock suficiente', 
                        'data': []
                    }, 406

            else:
                return {
                    'message': 'No se admiten cantidades negativas', 
                    'data': []
                }, 406                

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return {'message': 'Error interno del servidor', 'data': {}}, 500           

    def post(self):
        pass   