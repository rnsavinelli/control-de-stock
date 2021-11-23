#!/usr/bin/python
# -*- coding: utf-8 -*-


class Ubicacion:
    def _area_validator(self, area):
        if len(area) != 2:
            return False

        for character in str(area):
            if not character.isalpha():
                return False

        return True

    def _cara_validator(self, cara):
        return self._area_validator(cara)

    def _pasillo_validator(self, pasillo):
        if len(pasillo) != 2:
            return False

        for character in str(pasillo):
            if not character.isdigit():
                return False

        return True

    def _fila_validator(self, fila):
        return self._pasillo_validator(fila)

    def parse(self, ubicacion):
        ubicacion_splitted = str(ubicacion).strip().split("-")

        if len(ubicacion_splitted) != 4:
            raise Exception("La ubicación NO tiene el formato AREA-PASILLO-FILA-CARA")

        area = ubicacion_splitted[0]
        pasillo = ubicacion_splitted[1]
        fila = ubicacion_splitted[2]
        cara = ubicacion_splitted[3]

        if (
            not self._area_validator(area)
            or not self._cara_validator(cara)
            or not self._fila_validator(fila)
            or not self._pasillo_validator(pasillo)
        ):
            raise Exception("La ubicación NO cumple con el estándar definido")

        return area, pasillo, fila, cara
