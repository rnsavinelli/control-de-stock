#!/usr/bin/python
# -*- coding: utf-8 -*-


class Validator:
    def _area_validator(self, area):
        if len(area) != 2:
            return False

        for character in str(area):
            if not character.isalpha():
                return False

        return True

    def _cara_validator(self, cara):
        return self._area_validator(cara) and (str(cara) == "IZ" or str(cara) == "DE")

    def _pasillo_validator(self, pasillo):
        if len(pasillo) != 2:
            return False

        for character in str(pasillo):
            if not character.isdigit():
                return False

        return True

    def _fila_validator(self, fila):
        return self._pasillo_validator(fila)

    def _country_code_validator(self, code):
        if len(code) != 2:
            return False

        for character in str(code):
            if not character.isalpha():
                return False

        return True

    def _numeric_sequence_validator(self, sequence):
        if len(sequence) != 2:
            return False

        for character in str(sequence):
            if not character.isdigit():
                return False

        return True

    def parse_ubicacion(self, ubicacion):
        ubicacion_splitted = str(ubicacion).strip().split("-")

        if len(ubicacion_splitted) == 4:

            area = ubicacion_splitted[0]
            pasillo = ubicacion_splitted[1]
            fila = ubicacion_splitted[2]
            cara = ubicacion_splitted[3]

            if (
                self._area_validator(area)
                and self._cara_validator(cara)
                and self._fila_validator(fila)
                and self._pasillo_validator(pasillo)
            ):
                return area, pasillo, fila, cara

        raise Exception("La ubicacion NO cumple con el estandar definido")

    def validar_deposito(self, deposito):
        if len(deposito) == 4:
            country_code = deposito[0:2]
            numeric_sequence = deposito[2:4]

            if self._country_code_validator(
                country_code
            ) and self._numeric_sequence_validator(numeric_sequence):
                return

        raise Exception("El deposito NO cumple con el estandar definido")

    def validar_cantidad(self, cantidad):
        if int(cantidad) < 0:
            raise Exception("No se admiten cantidades negativas")
