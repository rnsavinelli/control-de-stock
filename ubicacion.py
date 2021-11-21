import traceback
from log import log


class Ubicacion:
    def parse(self, ubicacion):
        ubicacion_splitted = str(ubicacion).strip().split("-")

        if len(ubicacion_splitted) != 4:
            raise Exception("La ubicación NO tiene el formato AREA-PASILLO-FILA-CARA")

        area = ubicacion_splitted[0]
        pasillo = ubicacion_splitted[1]
        fila = ubicacion_splitted[2]
        cara = ubicacion_splitted[3]

        return area, pasillo, fila, cara
