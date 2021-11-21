import sqlite3
import traceback
from sqlite3 import Error
from server.log import log


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

            traceback.print_exc()
            data, description = [], []
            log("ERROR: " + str(e))
            raise Exception("Se produjo un error al ejecutar la query")

        finally:
            if con:
                con.close()

        return data, description, rowcount

    def read_table(self, table):
        data, description = [], []

        try:
            data, description = self.execute(f"SELECT * FROM {table}")

            columns = list(map(lambda x: x[0], description))

        except (Exception, Error) as e:
            traceback.print_exc()
            data, description = [], []
            log("ERROR: " + str(e))

        return data, columns

    def write_table(self, table, args):
        try:
            keys = str(list(args.keys())).replace("[", "").replace("]", "")
            values = str(list(args.values())).replace("[", "").replace("]", "")
            self.execute(f"INSERT INTO {table} ({keys}) VALUES ({values})")

        except (Exception, Error) as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
            raise Exception("Se produjo un error al intertar escribir la base de datos")
