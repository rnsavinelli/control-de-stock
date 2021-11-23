#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Resource

from server.endpoint import Endpoint

# 4 - Exponer un endpoint de búsqueda. Se nos indica el depósito y producto, y este nos
# devuelva las posibles ubicaciones y cantidad en las mismas.
class Buscar(Resource, Endpoint):
    def __init__(self, **kwargs):
        Endpoint.__init__(self, database_file=kwargs["database_file"])

    def get(self, identifier, deposito):
        code, message, data = self._get_producto_segun_deposito(identifier, deposito)

        return {"mensaje": message, "data": data}, code

    def _get_producto_segun_deposito(self, identifier, deposito):
        try:
            data, description, _ = self.database.select(
                "*",
                "PRODUCTO_POR_DEPOSITO",
                f'ID_PRODUCTO={int(identifier)} AND ID_DEPOSITO="{str(deposito)}"',
            )

            result = self._bundle(data, description)

            if result != []:
                return 200, "Productos encontrados", result

            else:
                return 404, "No se encontraron productos", {}

        except Exception as e:
            return 500, str(e), {}
