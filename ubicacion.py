import traceback
from log import log


class Ubicacion:
    def parse(self, ubicacion):
        try:
            area = str(ubicacion).strip().split("-")[0]
            pasillo = str(ubicacion).strip().split("-")[1]
            fila = str(ubicacion).strip().split("-")[2]
            cara = str(ubicacion).strip().split("-")[3]

        except Exception as e:
            traceback.print_exc()
            area, pasillo, fila, cara = str(), str(), str(), str()
            log("ERROR: " + str(e))

        return area, pasillo, fila, cara
