#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Resource
import traceback

from server.logger import log
from server.endpoint import Endpoint

# 3 - Exponer un endpoint de lectura. Se nos indica un depósito y una ubicación, y este
# liste los productos y cantidad que hay en el mismo.
class Leer(Resource, Endpoint):
    def get(self, deposito, ubicacion):
        code, message, data = self._get_productos(deposito, ubicacion)

        return {"mensaje": message, "data": data}, code

    def _get_productos(self, deposito, ubicacion):
        try:
            area, pasillo, fila, cara = self.locator.parse(ubicacion)

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 406, str(e), {}

        try:
            data, description, _ = self.database.select(
                "*",
                "PRODUCTO_POR_DEPOSITO",
                f'ID_DEPOSITO="{str(deposito)}" AND AREA="{str(area)}" AND PASILLO={int(pasillo)} \
                    AND FILA={int(fila)} AND CARA="{str(cara)}"',
            )

            result = self._bundle(data, description)

            if result != []:
                return 200, "Productos encontrados", result

            else:
                return 404, "No se encontraron productos", {}

        except Exception as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            return 500, str(e), {}
