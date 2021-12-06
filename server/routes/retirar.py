#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse

from server.endpoint import Endpoint

# 2 - Exponer un endpoint para poder retirar productos de una ubicación.
# Se nos indicará el depósito, producto, cantidad y ubicación de donde sacarla.
class Retirar(Resource, Endpoint):
    def __init__(self, **kwargs):
        Endpoint.__init__(self, database_file=kwargs["database_file"])

    def put(self):

        parser = reqparse.RequestParser()

        parser.add_argument("deposito", required=True)
        parser.add_argument("ubicacion", required=True)
        parser.add_argument("producto", required=True)
        parser.add_argument("cantidad", required=True)

        args = parser.parse_args()

        try:
            self.validar_cantidad(args["cantidad"])
            area, pasillo, fila, cara = self.parse_ubicacion(args["ubicacion"])
            self.validar_deposito(args["deposito"])

        except Exception as e:
            return self.build_response(str(e), {}, 406)

        try:
            cantidad_disponible = self._get_cantidad_de_producto(
                args["producto"], args["deposito"], area, pasillo, fila, cara
            )

            if cantidad_disponible == -1:
                return self.build_response("Producto no encontrado", {}, 404)

            if cantidad_disponible - int(args["cantidad"]) >= 0:
                message, data, code = self._retirar_cantidad_de_producto(
                    args["producto"],
                    args["deposito"],
                    area,
                    pasillo,
                    fila,
                    cara,
                    args["cantidad"],
                )

                return self.build_response(message, data, code)

            else:
                return self.build_response("No hay stock suficiente", {}, 406)

        except Exception as e:
            return self.build_response(str(e), {}, 500)

    def _retirar_cantidad_de_producto(
        self, producto, deposito, area, pasillo, fila, cara, cantidad
    ):
        try:
            self.database.update(
                "PRODUCTO_POR_DEPOSITO",
                f"CANTIDAD=CANTIDAD-{int(cantidad)}",
                f'ID_PRODUCTO={int(producto)} AND ID_DEPOSITO="{str(deposito)}" AND AREA="{str(area)}" \
                    AND PASILLO={int(pasillo)} AND FILA={int(fila)} AND CARA="{str(cara)}"',
            )

            return "El stock fue actualizado", {}, 200

        except Exception as e:
            return str(e), {}, 500

    def _get_cantidad_de_producto(self, producto, deposito, area, pasillo, fila, cara):
        data, description, _ = self.database.select(
            "CANTIDAD",
            "PRODUCTO_POR_DEPOSITO",
            f'ID_PRODUCTO={int(producto)} AND ID_DEPOSITO="{str(deposito)}" AND AREA="{str(area)}" \
                AND PASILLO={int(pasillo)} AND FILA={int(fila)} AND CARA="{str(cara)}"',
        )

        result = self.bundle(data, description)

        if result != []:
            return int(result[0]["CANTIDAD"])

        return -1
