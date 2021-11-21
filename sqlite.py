import sqlite3
import traceback
from sqlite3 import Error
from log import log


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
            con.commit()

        except (Exception, Error) as e:
            traceback.print_exc()
            data, description = [], []
            log("ERROR: " + str(e))

        finally:
            if con:
                con.close()

        return data, description

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
            print(
                self.execute(
                    f"INSERT INTO {table} ({str(args.keys())}) VALUES ({args.values()})"
                ))

        except (Exception, Error) as e:
            traceback.print_exc()
            log("ERROR: " + str(e))
