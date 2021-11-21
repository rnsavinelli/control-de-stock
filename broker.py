from sqlite import SQLite
import traceback
from log import log
from ubicacion import Ubicacion

database_file = "sqlite/marketplace.sqlite"


class Broker:
    database = SQLite(database_file)
    locator = Ubicacion()

    def bundle(self, data, description):
        payload = list()

        if data != []:
            for values in data:
                keys = map(lambda x: x[0], description)
                payload.append(dict(zip(list(keys), list(values))))

            return payload

        else:
            return []

    def get_producto(self, identifier):
        try:
            data, description = self.database.execute(
                f"SELECT * FROM PRODUCTO WHERE ID={int(identifier)}"
            )

            result = self.bundle(data, description)

            if result != []:
                return 200, "Producto encontrado", result

            else:
                return 404, "Producto no encontrado", {}

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}

    def get_productos(self, deposito, ubicacion):
        try:
            area, pasillo, fila, cara = self.locator.parse(ubicacion)

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 406, str(e), {}

        try:
            data, description = self.database.execute(
                f'SELECT * FROM PRODUCTO_POR_DEPOSITO \
                    WHERE \
                    ID_DEPOSITO="{str(deposito)}" \
                    AND AREA="{str(area)}" \
                    AND PASILLO={int(pasillo)} \
                    AND FILA={int(fila)} \
                    AND CARA="{str(cara)}"'
            )

            result = self.bundle(data, description)

            if result != []:
                return 200, "Productos encontrados", result

            else:
                return 404, "Productos no encontrados", {}

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}

    def get_producto_segun_deposito(self, identifier, deposito):
        try:
            data, description = self.database.execute(
                f'SELECT * FROM PRODUCTO_POR_DEPOSITO \
                    WHERE \
                    ID_PRODUCTO={int(identifier)} \
                    AND ID_DEPOSITO="{str(deposito)}"'
            )

            result = self.bundle(data, description)

            if result != []:
                return 200, "Productos encontrados", result

            else:
                return 404, "Productos no encontrados", {}

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}

    def retirar_cantidad_de_producto(self, producto, deposito, ubicacion, cantidad):
        try:
            area, pasillo, fila, cara = self.locator.parse(ubicacion)

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 406, str(e), {}

        try:
            self.database.execute(
                f'UPDATE PRODUCTO_POR_DEPOSITO SET CANTIDAD=CANTIDAD - {int(cantidad)} \
                    WHERE \
                    ID_PRODUCTO={int(producto)} \
                    AND ID_DEPOSITO="{str(deposito)}" \
                    AND AREA="{str(area)}" \
                    AND PASILLO={int(pasillo)} \
                    AND FILA={int(fila)} \
                    AND CARA="{str(cara)}"'
            )

            return 200, "El stock fue actualizado", {}

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}

    def get_cantidad_de_producto(self, producto, deposito, ubicacion):
        try:
            area, pasillo, fila, cara = self.locator.parse(ubicacion)

            data, _ = self.database.execute(
                f'SELECT CANTIDAD FROM PRODUCTO_POR_DEPOSITO \
                    WHERE \
                    ID_PRODUCTO={int(producto)} \
                    AND ID_DEPOSITO="{str(deposito)}" \
                    AND AREA="{str(area)}" \
                    AND PASILLO={int(pasillo)} \
                    AND FILA={int(fila)} \
                    AND CARA="{str(cara)}"'
            )

            if data != []:
                cantidad_disponible = data[0][0]
                return cantidad_disponible

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))

        return -1
