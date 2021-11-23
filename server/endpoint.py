#!/usr/bin/python
# -*- coding: utf-8 -*-

from server.ubicacion import Ubicacion
from server.sqlite import SQLite


class Endpoint:
    def __init__(self, database_file):
        self.database = SQLite(database_file=database_file)
        self.locator = Ubicacion()

    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass

    def _bundle(self, data, description):
        payload = list()

        if data != []:
            for values in data:
                keys = map(lambda x: x[0], description)
                payload.append(dict(zip(list(keys), list(values))))

            return payload

        else:
            return []
