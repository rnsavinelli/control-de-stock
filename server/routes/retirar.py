#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Resource

from server.endpoint import Endpoint

# 2 - Exponer un endpoint para poder retirar productos de una ubicación.
# Se nos indicará el depósito, producto, cantidad y ubicación de donde sacarla.
class Retirar(Resource, Endpoint):
    def __init__(self, **kwargs):
        Endpoint.__init__(self, database_file=kwargs["database_file"])

    def get(self, deposito, ubicacion, producto, cantidad):
        try:
            self._validar_cantidad(cantidad)
            area, pasillo, fila, cara = self._parse_ubicacion(ubicacion)

        except Exception as e:
            return {"mensaje": str(e), "data": {}}, 406

        try:
            cantidad_disponible = self._get_cantidad_de_producto(
                producto, deposito, area, pasillo, fila, cara
            )

        except Exception as e:
            return {"mensaje": str(e), "data": {}}, 500

        if cantidad_disponible == -1:
            return {"mensaje": "Producto no encontrado", "data": {}}, 404

        if cantidad_disponible - cantidad >= 0:
            try:
                message, data, code = self._retirar_cantidad_de_producto(
                    producto, deposito, area, pasillo, fila, cara, cantidad
                )

                return {"mensaje": message, "data": data}, code

            except Exception as e:
                return {"mensaje": str(e), "data": {}}, 406

        else:
            return {"mensaje": "No hay stock suficiente", "data": {}}, 406

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

        result = self._bundle(data, description)

        if result != []:
            return result[0]["CANTIDAD"]

        return -1

    def _validar_cantidad(self, cantidad):
        if cantidad < 0:
            raise Exception("No se admiten cantidades negativas")
