import sqlite3
from res.constants import *
from res.operations import *


class Database:
    def __init__(self):
        self.db_connection = sqlite3.connect(LOCAL_DB_DIR)
        self.db_cursor = self.db_connection.cursor()

        self.create_table(WEEKDAY_TABLE_NAME, WEEKDAY_TABLE_COLUMN_NAMES, WEEKDAY_TABLE_COLUMN_TYPES)

    def get_weekday_tasks(self, day_index):
        return self.search_table(WEEKDAY_TABLE_NAME, day_index, 1)


    def create_table(self, table_name, column_names, column_types):
        column_argument = self._format_column_arguments(column_names, column_types)
        self.db_cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({column_argument})')
        self.db_connection.commit()

    def create_record(self, table_name, values):
        q_format = "?, "*(len(values)-1) + "?"
        self.db_cursor.execute(f'INSERT INTO {table_name} VALUES ({q_format})', values)
        self.db_connection.commit()

    def search_table(self, table_name, field, value):
        self.db_cursor.execute(f"SELECT * FROM {table_name} WHERE {field} = ?", (value,))
        return self.db_cursor.fetchall()

    def update_weekday_task(self, title, change_field, value):
        self.db_cursor.execute(f"UPDATE {WEEKDAY_TABLE_NAME} SET {change_field} = ? WHERE {WEEKDAY_TABLE_COLUMN_NAMES[0]} = ?", (value, title))
        self.db_connection.commit()

    def add_weekday_task(self, title, description, do_mon, do_tue, do_wed, do_thu, do_fri, do_sat, do_sun):
        self.create_record(WEEKDAY_TABLE_NAME, [title, description, DATE_BLANK, do_mon, do_tue, do_wed, do_thu, do_fri, do_sat, do_sun])
    @staticmethod
    def _format_column_arguments(names, types):
        return ''.join([str(n) + " " + t + ", " for n, t in zip(names, types)])[:-2]


