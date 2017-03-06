import sqlite3


class DB:
    def __init__(self):
        self.connection = sqlite3.connect('mltm.db')
        self.cursor = self.connection.cursor()

    def execute(self, statement, params=()):
        self.cursor.execute(statement, params)
        self.connection.commit()

    def execute_and_fetch_one(self, statement, params=()):
        self.cursor.execute(statement, params)
        return self.cursor.fetchone()

    def execute_and_fetch_all(self, statement, params=()):
        self.cursor.execute(statement, params)
        return self.cursor.fetchall()

    def get_last_rowid(self):
        return self.cursor.lastrowid

