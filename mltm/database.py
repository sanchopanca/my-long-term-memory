import os.path
import sqlite3


db_file_path = os.path.join(os.environ.get('HOME'), '.mltm.db')


class DB:
    def __init__(self):
        self.connection = sqlite3.connect(db_file_path)
        self.cursor = self.connection.cursor()
        self.init()

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

    def init(self):
        create_statements = ['''
        CREATE TABLE IF NOT EXISTS entries
        (
            title TEXT,
            content TEXT
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS tags
        (
            name TEXT
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS tags_entries
        (
            tag_id INTEGER,
            entry_id INTEGER,
            PRIMARY KEY (tag_id, entry_id)
        )
        WITHOUT ROWID;
        ''']
        for statement in create_statements:
            self.execute(statement)
