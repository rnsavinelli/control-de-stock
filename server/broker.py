import os
from server.sqlite import SQLite
import traceback
from server.log import log
from server.ubicacion import Ubicacion


class Broker:
    def __init__(self, database_file):
        self.database = SQLite(database_file)
        self.locator = Ubicacion()

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
            data, description, _ = self.database.execute(
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
            data, description, _ = self.database.execute(
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
            data, description, _ = self.database.execute(
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

            data, _, _ = self.database.execute(
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

    def add_producto(self, deposito, ubicacion, producto, cantidad):
        try:
            # Validar que la dirección tenga el patrón correcto.
            area, pasillo, fila, cara = self.locator.parse(ubicacion)

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 406, str(e), {}

        try:
            # Validar que el producto/item sea almacenado en nuestros depósitos.
            data, description, _ = self.database.execute(
                f"SELECT * FROM PRODUCTO WHERE ID={producto} LIMIT 1"
            )

            n_entries = len(self.bundle(data, description))

            if n_entries == 0:
                return 404, "Producto no encontrado", {}

            table_producto = self.bundle(data, description)

            if table_producto[0]["ALMACENAMIENTO"] != "fullfilment":
                return 406, "El producto no pertence a fullfilment", {}

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}

        try:
            # No se pueden colocar más de 3 productos distintos en una ubicación.
            data, description, _ = self.database.execute(
                f'SELECT * FROM PRODUCTO_POR_DEPOSITO \
                    WHERE \
                    ID_DEPOSITO="{str(deposito)}" \
                    AND AREA="{str(area)}" \
                    AND PASILLO={int(pasillo)} \
                    AND FILA={int(fila)} \
                    AND CARA="{str(cara)}"'
            )

            entries = self.bundle(data, description)
            n_entries = len(entries)

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}

        # No se pueden colocar más de 3 productos distintos en una ubicación.
        if (int(producto) in [x["ID_PRODUCTO"] for x in entries]) or (n_entries < 3):

            cantidad_almacenada = 0
            for entry in entries:
                cantidad_almacenada = cantidad_almacenada + entry["CANTIDAD"]
                print(entry["CANTIDAD"])

            if cantidad_almacenada + int(cantidad) > 100:
                return (
                    406,
                    f"Solo queda espacio para {100 - cantidad_almacenada} productos en esta ubicación",
                    {},
                )

            try:
                args = {
                    "ID_PRODUCTO": producto,
                    "ID_DEPOSITO": deposito,
                    "AREA": area,
                    "PASILLO": pasillo,
                    "FILA": fila,
                    "CARA": cara,
                    "CANTIDAD": cantidad,
                }

                _, _, rowcount = self.database.execute(
                    f'UPDATE PRODUCTO_POR_DEPOSITO SET CANTIDAD=CANTIDAD + {int(cantidad)} \
                        WHERE \
                        ID_PRODUCTO={int(producto)} \
                        AND ID_DEPOSITO="{str(deposito)}" \
                        AND AREA="{str(area)}" \
                        AND PASILLO={int(pasillo)} \
                        AND FILA={int(fila)} \
                        AND CARA="{str(cara)}"'
                )

                if rowcount == 0:
                    self.database.write_table("PRODUCTO_POR_DEPOSITO", args)

                return 200, "La base de datos fue actualizada", {}

            except Exception as e:
                traceback.print_exc()
                log("ERROR: " + str(e))
                return 500, str(e), {}

        else:
            return 406, "No pueden almacenarse más productos en esta ubicación", {}
