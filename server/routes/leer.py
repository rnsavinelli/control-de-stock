#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Resource

from server.endpoint import Endpoint

# 3 - Exponer un endpoint de lectura. Se nos indica un depósito y una ubicación, y este
# liste los productos y cantidad que hay en el mismo.
class Leer(Resource, Endpoint):
    def __init__(self, **kwargs):
        Endpoint.__init__(self, database_file=kwargs["database_file"])

    def get(self, deposito, ubicacion):
        try:
            area, pasillo, fila, cara = self.parse_ubicacion(ubicacion)
            self.validar_deposito(deposito)

        except Exception as e:
            return self.build_response(str(e), {}, 406)

        message, data, code = self._get_productos(deposito, area, pasillo, fila, cara)

        return self.build_response(message, data, code)

    def _get_productos(self, deposito, area, pasillo, fila, cara):
        try:
            data, description, _ = self.database.select(
                "*",
                "PRODUCTO_POR_DEPOSITO",
                f'ID_DEPOSITO="{str(deposito)}" AND AREA="{str(area)}" \
                    AND PASILLO={int(pasillo)} AND FILA={int(fila)} \
                    AND CARA="{str(cara)}"',
            )

            result = self.bundle(data, description)

            if result != []:
                return "Productos encontrados", result, 200

            else:
                return "No se encontraron productos", {}, 404

        except Exception as e:
            return str(e), {}, 500
