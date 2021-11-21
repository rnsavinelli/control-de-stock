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
            return self.bundle(data, description)

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return []

    def get_producto_segun_deposito(self, identifier, deposito):
        try:
            data, description = self.database.execute(
                f'SELECT * FROM PRODUCTO_POR_DEPOSITO \
                WHERE \
                ID_PRODUCTO={int(identifier)} AND \
                ID_DEPOSITO="{str(deposito)}" \
                '
            )
            return self.bundle(data, description)

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return []

    def get_productos(self, deposito, ubicacion):
        try:
            area, pasillo, fila, cara = self.locator.parse(ubicacion)

            data, description = self.database.execute(
                f'SELECT * FROM PRODUCTO_POR_DEPOSITO \
                WHERE \
                ID_DEPOSITO="{str(deposito)}" AND \
                AREA="{str(area)}" AND \
                PASILLO={int(pasillo)} AND \
                FILA={int(fila)} AND \
                CARA="{str(cara)}" \
            '
            )

            return self.bundle(data, description)

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return []

    def retirar_cantidad_de_producto(self, producto, deposito, ubicacion, cantidad):
        try:
            area, pasillo, fila, cara = self.locator.parse(ubicacion)

            self.database.execute(
                f'UPDATE PRODUCTO_POR_DEPOSITO \
                SET CANTIDAD=CANTIDAD - {int(cantidad)} \
                WHERE \
                ID_PRODUCTO={int(producto)} AND \
                ID_DEPOSITO="{str(deposito)}" AND \
                AREA="{str(area)}" AND \
                PASILLO={int(pasillo)} AND \
                FILA={int(fila)} AND \
                CARA="{str(cara)}" \
            '
            )
            return 0

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))

        return -1

    def get_cantidad_de_producto(self, producto, deposito, ubicacion):
        try:
            area, pasillo, fila, cara = self.locator.parse(ubicacion)

            data, _ = self.database.execute(
                f'SELECT CANTIDAD \
                FROM PRODUCTO_POR_DEPOSITO \
                WHERE \
                ID_PRODUCTO={int(producto)} AND \
                ID_DEPOSITO="{str(deposito)}" AND \
                AREA="{str(area)}" AND \
                PASILLO={int(pasillo)} AND \
                FILA={int(fila)} AND \
                CARA="{str(cara)}" \
            '
            )

            if data != []:
                cantidad_disponible = data[0][0]
                return cantidad_disponible

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))

        return -1
