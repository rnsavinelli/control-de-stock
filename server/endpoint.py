#!/usr/bin/python
# -*- coding: utf-8 -*-

from server.validator import Validator
from server.sqlite import SQLite


class Endpoint(Validator):
    def __init__(self, database_file):
        self.database = SQLite(database_file=database_file)

    def bundle(self, data, description):
        payload = list()

        if data != []:
            for values in data:
                keys = map(lambda x: x[0], description)
                payload.append(dict(zip(list(keys), list(values))))

            return payload

        else:
            return []

    def build_response(self, message, data, code):
        return {"mensaje": message, "data": data}, code
