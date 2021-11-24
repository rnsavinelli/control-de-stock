#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse

from server.endpoint import Endpoint

# 1 - Exponer un endpoint REST para agregar productos en una ubicación.
#   a. Se nos indicará el Depósito, producto, cantidad y ubicación donde quiere colocar.
#   b. Validar que la dirección tenga el patrón correcto.
#   c. Que el producto/item sea almacenado en nuestros depósitos.
#   d. No se pueden colocar más de 3 productos distintos en una ubicación.
class Agregar(Resource, Endpoint):
    MAX_PRODUCTOS_POR_UBICACION = 3
    MAX_CANTIDAD_PRODUCTOS_POR_UBICACION = 100
    ALMACENAMIENTO_LOCAL = "fullfilment"

    def __init__(self, **kwargs):
        Endpoint.__init__(self, database_file=kwargs["database_file"])

    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument("deposito", required=True)
        parser.add_argument("ubicacion", required=True)
        parser.add_argument("producto", required=True)
        parser.add_argument("cantidad", required=True)

        args = parser.parse_args()

        # Validar que la dirección tenga el patrón correcto.
        try:
            self.validar_cantidad(args["cantidad"])
            area, pasillo, fila, cara = self.parse_ubicacion(args["ubicacion"])
            self.validar_deposito(args["deposito"])

        except Exception as e:
            return self.build_response(str(e), {}, 406)

        message, data, code = self._add_producto(
            args["deposito"],
            area,
            pasillo,
            fila,
            cara,
            args["producto"],
            args["cantidad"],
        )

        return self.build_response(message, data, code)

    def _add_producto(self, deposito, area, pasillo, fila, cara, producto, cantidad):
        try:
            result = self._obtener_producto_por_id(producto)

            if len(result) == 0:
                return "Producto no encontrado", {}, 404

            if not self._almacenado_en_deposito(result[0]["ALMACENAMIENTO"]):
                return "El producto no se encuentra en nuestros depositos", {}, 406

            productos = self._obetener_productos_por_ubicacion(
                deposito, area, pasillo, fila, cara
            )

            # No colocar más de 3 productos distintos en una ubicación.
            if not (
                (int(producto) in [x["ID_PRODUCTO"] for x in productos])
                or (len(productos) < self.MAX_PRODUCTOS_POR_UBICACION)
            ):
                return "No pueden almacenarse mas productos en esta ubicacion", {}, 406

            # La suma de las cantidades de los productos que hubiera en una ubicación
            # no puede ser mayor a 100 unidades.
            cantidad_almacenada = sum(p["CANTIDAD"] for p in productos)

            if (
                cantidad_almacenada + int(cantidad)
                > self.MAX_CANTIDAD_PRODUCTOS_POR_UBICACION
            ):
                return (
                    "Solo queda espacio para "
                    + f"{self.MAX_CANTIDAD_PRODUCTOS_POR_UBICACION - cantidad_almacenada} "
                    + "productos en esta ubicacion",
                    {},
                    406,
                )

            self._actualizar_base_de_datos(
                deposito, area, pasillo, fila, cara, producto, cantidad
            )

            return "La base de datos fue actualizada", {}, 200

        except Exception as e:
            return str(e), {}, 500

    def _obtener_producto_por_id(self, id):
        data, description, _ = self.database.select("*", "PRODUCTO", f"ID={int(id)}")

        return self.bundle(data, description)

    def _obetener_productos_por_ubicacion(self, deposito, area, pasillo, fila, cara):
        data, description, _ = self.database.select(
            "*",
            "PRODUCTO_POR_DEPOSITO",
            f'ID_DEPOSITO="{str(deposito)}" AND AREA="{str(area)}" \
                    AND PASILLO={int(pasillo)} AND FILA={int(fila)} \
                    AND CARA="{str(cara)}"',
        )

        return self.bundle(data, description)

    def _actualizar_base_de_datos(
        self, deposito, area, pasillo, fila, cara, producto, cantidad
    ):
        _, _, rowcount = self.database.update(
            "PRODUCTO_POR_DEPOSITO",
            f"CANTIDAD=CANTIDAD + {int(cantidad)}",
            f'ID_PRODUCTO={int(producto)} AND ID_DEPOSITO="{str(deposito)}"\
                AND AREA="{str(area)}" AND PASILLO={int(pasillo)} \
                AND FILA={int(fila)} AND CARA="{str(cara)}"',
        )

        #
        if rowcount == 0:
            args = {
                "ID_PRODUCTO": producto,
                "ID_DEPOSITO": deposito,
                "AREA": area,
                "PASILLO": pasillo,
                "FILA": fila,
                "CARA": cara,
                "CANTIDAD": cantidad,
            }
            self.database.write_table("PRODUCTO_POR_DEPOSITO", args)

    def _almacenado_en_deposito(self, tipo_almacenamiento):
        return tipo_almacenamiento == "fullfilment"
