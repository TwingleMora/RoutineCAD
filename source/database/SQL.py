import sqlite3
from source.config import CONFIG

class SQL:
    database_name = ""
    table_name = ""

    def __init__(self):
        self.database_name = CONFIG.db_name
        pass

    def sqlconnection(self):
        self.conn = sqlite3.connect(str(self.database_name) + '.db')
        self.cursor = self.conn.cursor()

    def clear(self):
        self.sqlconnection()
        self.cursor.execute(f"delete from {self.table_name}")
        self.conn.commit()
        self.conn.close()

    def delete(self, table_name):
        # if self.conn.isolation_level is None:
        self.sqlconnection()
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    def create_table(self):
        pass

    # def insert_in_table(self, table_name, id, name, json,active_state=None,start_time=None,end_time=None,interations=None):
    def insert(self, object):
        pass

    def update(self, object):
        pass

    def get_records_as_list(self):
        pass

    def get_records_as_dicts(self):
        pass

    def get_record_by_id(self, id):
        pass

    def delete_record_by_id(self, id):
        pass


