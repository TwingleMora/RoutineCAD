from source.config import CONFIG
from source.database.SQL import SQL
from source.routine import Routine

import dateutil.parser


class RoutineDB(SQL):
    columns_def = "id INTEGER, name TEXT NOT NULL, data TEXT, active_state INTEGER, start_time TIMESTAMP,end_time TIMESTAMP, iterations INTEGER, weight INTEGER, Finished INTEGER, EXP INTEGER"
    columns_insert = "(id , name, data,active_state,start_time,end_time,iterations,weight,Finished,EXP) VALUES (?,?,?,?,?,?,?,?,?,?)"
    columns_update = "name = ?, data = ?, active_state = ?,start_time=?,end_time =?,iterations=?, weight=?, Finished=?, EXP=? WHERE id = ?"
    columns_select = "id , name, data, active_state, start_time , end_time , iterations, weight, Finished, EXP"

    def __init__(self):
        super().__init__()

        self.table_name = CONFIG.routine_table_name

    def create_table(self):
        # if self.conn.isolation_level is None:
        self.sqlconnection()
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name}  ({self.columns_def})")
        self.conn.commit()
        self.conn.close()

    def insert(self, routine: Routine):
        # if self.conn.isolation_level is None:
        self.sqlconnection()
        self.cursor.execute(
            f'''INSERT INTO  {self.table_name}  {self.columns_insert}''',
            (routine.routine_id, routine.routine_name, routine.data, routine.active_state, routine.start_time,
             routine.end_time,
             routine.iterations, routine.weight, int(routine.finished), routine.EXP))
        self.conn.commit()
        self.conn.close()

    def update(self, routine: Routine):
        ### KEEEP ROUTINE.ID AT THE END ######
        self.sqlconnection()
        ### KEEEP ROUTINE.ID AT THE END ######
        self.cursor.execute(
            f'''UPDATE {self.table_name} SET {self.columns_update}''',
            (routine.routine_name, routine.data, routine.active_state, routine.start_time, routine.end_time,
             routine.iterations, routine.weight, routine.finished, routine.EXP, routine.routine_id))
        ### KEEEP ROUTINE.ID AT THE END ######
        self.conn.commit()
        ### KEEEP ROUTINE.ID AT THE END ######
        self.conn.close()
        ### KEEEP ROUTINE.ID AT THE END ######

    def update_time(self, routine: Routine):
        ### KEEEP ROUTINE.ID AT THE END ######
        self.sqlconnection()
        ### KEEEP ROUTINE.ID AT THE END ######
        self.cursor.execute(
            f'''UPDATE {self.table_name} SET start_time=?,end_time =?, Finished=? WHERE id = ?''',
            (routine.start_time, routine.end_time, routine.finished, routine.routine_id))
        ### KEEEP ROUTINE.ID AT THE END ######
        self.conn.commit()
        ### KEEEP ROUTINE.ID AT THE END ######
        self.conn.close()
        ### KEEEP ROUTINE.ID AT THE END ######

    def get_routine_by_id(self, record_id):
        # if self.conn.isolation_level is None:
        self.sqlconnection()
        # dict = {"id":None,"name":None,"data":None}
        int_id = int(record_id)
        rows = self.cursor.execute(
            f'''SELECT {self.columns_select}  FROM {self.table_name} WHERE id = {int_id}''').fetchall()

        routine = Routine(routine_id=int(rows[0][0]), routine_name=rows[0][1], data=rows[0][2],
                          active_state=rows[0][3], start_time=dateutil.parser.parse(rows[0][4]),
                          end_time=dateutil.parser.parse(rows[0][5]), iterations=rows[0][6],
                          weight=rows[0][7], finished=rows[0][8], EXP=rows[0][9])

        return routine

    def get_record_by_id(self, record_id):
        # if self.conn.isolation_level is None:
        self.sqlconnection()
        # dict = {"id":None,"name":None,"data":None}
        int_id = int(record_id)
        rows = self.cursor.execute(
            f'''SELECT {self.columns_select}  FROM {self.table_name} WHERE id = {int_id}''').fetchall()

        i = 0
        record = {"id": rows[0][0], "name": rows[0][1], "data": rows[0][2], "active_state": rows[0][3],
                  "start_time": rows[0][4], "end_time": rows[0][5], "iterations": rows[0][6], "weight": rows[0][7],
                  "finished": rows[0][8], "EXP": rows[0][9]}
        return record

    def get_records_as_list(self):
        # if self.conn.isolation_level is None:
        self.sqlconnection()
        # dict = {"id":None,"name":None,"data":None}
        rows = self.cursor.execute(
            f'''SELECT {self.columns_select}  FROM {self.table_name}''').fetchall()

        to_create = [{"id": rows[i][0], "name": rows[i][1], "data": rows[i][2], "active_state": rows[i][3],
                      "start_time": rows[i][4], "end_time": rows[i][5], "iterations": rows[i][6], "weight": rows[i][7],
                      "finished": rows[i][8], "EXP": rows[i][9]} for i in
                     range(len(rows))]
        return to_create

    def get_records_as_dicts(self):
        # if self.conn.isolation_level is None:
        self.sqlconnection()
        # dict = {"id":None,"name":None,"data":None}
        rows = self.cursor.execute(
            f'''SELECT {self.columns_select} FROM {self.table_name}''').fetchall()

        to_update = {int((rows[i][0])): {"name": rows[i][1], "data": rows[i][2], "active_state": rows[i][3],
                                         "start_time": rows[i][4], "end_time": rows[i][5], "iterations": rows[i][6],
                                         "weight": rows[i][7], "finished": rows[i][8], "EXP": rows[i][9]}
                     for i in range(len(rows))}
        return to_update

    def get_routines(self):
        # if self.conn.isolation_level is None:
        self.sqlconnection()
        # dict = {"id":None,"name":None,"data":None}
        rows = self.cursor.execute(
            f'''SELECT {self.columns_select}  FROM {self.table_name}''').fetchall()

        # to_create = [{"id": rows[i][0], "name": rows[i][1], "data": rows[i][2], "active_state": rows[i][3],
        #               "start_time": rows[i][4], "end_time": rows[i][5], "iterations": rows[i][6]} for i in
        #              range(len(rows))]
        routines = [Routine(routine_id=int(rows[i][0]), routine_name=rows[i][1],
                            active_state=rows[i][3], start_time=dateutil.parser.parse(rows[i][4]),
                            end_time=dateutil.parser.parse(rows[i][5]), iterations=rows[i][6],
                            weight=rows[i][7], finished=rows[i][8], EXP=rows[i][9]) for i in range(len(rows))]
        return routines

    def delete_record_by_id(self, id):
        self.sqlconnection()
        self.cursor.execute(f'''DELETE FROM {self.table_name} WHERE id = {id}''')
        self.conn.commit()
        self.conn.close()

    def calculate_new_routine_id(self):
        self.sqlconnection()
        last_id = self.cursor.execute(f'''SELECT  MAX(id) FROM {self.table_name}''').fetchone()
        if last_id[0] is not None:
            return last_id[0] + 1
        else:
            return 0

    def number_of_all_routines(self):
        self.sqlconnection()
        last_id = self.cursor.execute(f'''SELECT  COUNT(id) FROM {self.table_name}''').fetchone()
        if last_id[0] is not None:
            return last_id[0]
        else:
            return 0

    def get_finished_state(self, routine_id):
        self.sqlconnection()
        row = self.cursor.execute(f'''SELECT finished FROM {self.table_name} WHERE id = {routine_id}''').fetchone()
        if row[0] is not None:
            return row[0]
        else:
            return 0

    def get_active_state(self, routine_id):
        self.sqlconnection()
        row = self.cursor.execute(f'''SELECT active_state FROM {self.table_name} WHERE id = {routine_id}''').fetchone()
        if row[0] is not None:
            return row[0]
        else:
            return 0

    def get_end_time(self, routine_id):
        self.sqlconnection()
        row = self.cursor.execute(f'''SELECT end_time FROM {self.table_name} WHERE id = {routine_id}''').fetchone()
        if row[0] is not None:
            return dateutil.parser.parse(row[0])
        else:
            return None

    def get_exp(self, routine_id):
        self.sqlconnection()
        row = self.cursor.execute(f'''SELECT EXP FROM {self.table_name} WHERE id = {routine_id}''').fetchone()
        if row[0] is not None:
            return row[0]
        else:
            return 0

    def get_weight(self, routine_id):
        self.sqlconnection()
        row = self.cursor.execute(f'''SELECT weight FROM {self.table_name} WHERE id = {routine_id}''').fetchone()
        if row[0] is not None:
            return row[0]
        else:
            return 0

    def number_of_active_routines(self):
        self.sqlconnection()
        last_id = self.cursor.execute(
            f'''SELECT  COUNT(id) FROM {self.table_name} WHERE active_state != 0''').fetchone()
        if last_id[0] is not None:
            return last_id[0]
        else:
            return 0
