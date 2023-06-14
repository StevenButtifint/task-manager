import sqlite3
from res.constants import *


class Database:
    def __init__(self):
        self.db_connection = sqlite3.connect(LOCAL_DB_DIR)
        self.db_cursor = self.db_connection.cursor()

    def search_table(self, table_name, field, value):
        self.db_cursor.execute(f"SELECT * FROM {table_name} WHERE {field} = ?", (value,))
        return self.db_cursor.fetchall()

