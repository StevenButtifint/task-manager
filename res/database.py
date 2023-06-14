import sqlite3
from res.constants import *


class Database:
    def __init__(self):
        self.db_connection = sqlite3.connect(LOCAL_DB_DIR)
        self.db_cursor = self.db_connection.cursor()

    def get_weekday_tasks(self, day):
        return self.search_table(WEEKDAY_TABLE_NAME, day, 1)

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

