#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error


class SQLite:
    def __init__(self, database_file):
        self.database_file = str(database_file)

    def execute(self, query):
        data, description = [], []

        try:
            con = sqlite3.connect(self.database_file)
            cur = con.cursor()
            cur.execute(query)
            data = cur.fetchall()
            description = cur.description
            rowcount = cur.rowcount
            con.commit()

        except (Exception, Error) as e:
            if con:
                con.close()

            data, description = [], []
            raise Exception(f"Se produjo un error al ejecutar la query: {str(e)}")

        finally:
            if con:
                con.close()

        return data, description, rowcount

    def read_table(self, table):
        data, description = self.execute(f"SELECT * FROM {table}")

        columns = list(map(lambda x: x[0], description))

        return data, columns

    def write_table(self, table, args):
        keys = str(list(args.keys())).replace("[", "").replace("]", "")
        values = str(list(args.values())).replace("[", "").replace("]", "")

        self.execute(f"INSERT INTO {table} ({keys}) VALUES ({values})")

    def select(self, columns, table, condition):
        return self.execute(f"SELECT {columns} FROM {table} WHERE {condition}")

    def update(self, table, modifications, condition):
        return self.execute(f"UPDATE {table} SET {modifications} WHERE {condition}")
