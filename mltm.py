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


db = DB()


def add_entry(title, text, tags):
    tags_ids = _get_tags_ids(tags)
    insert_statement = '''
    INSERT INTO entries (title, content)
    VALUES (?, ?)
    '''
    db.execute(insert_statement, (title, text))
    entry_id = db.get_last_rowid()
    _update_tags_to_entry(tags_ids, entry_id)


def get_tag_id(tag):
    select_statement = '''
    SELECT rowid
    FROM tags
    WHERE name = ?
    '''
    tag_id = db.execute_and_fetch_one(select_statement, (tag,))
    if tag_id is None:
        insert_statement = '''
        INSERT into tags (name)
        VALUES (?)
        '''
        db.execute(insert_statement, (tag,))
        tag_id = db.get_last_rowid()
    return tag_id


def search_by_tag_id(tag_id):
    pass


def search_arbitrary_text(text):
    pass


def update_entry(entry_id, title, text, tags):
    update_statement = '''
    UPDATE entries SET
        title = ?,
        content = ?
    WHERE
        rowid = ?
    '''
    db.execute(update_statement, (title, text, entry_id))
    tags_ids = _get_tags_ids(tags)
    _update_tags_to_entry(tags_ids, entry_id)


def _update_tags_to_entry(tags_ids, entry_id):
    delete_statement = '''
    DELETE FROM tags_entries
    WHERE entry_id = ?
    '''
    db.execute(delete_statement, (entry_id,))
    for tag_id in tags_ids:
        insert_statement = '''
        INSERT INTO tags_entries (tag_id, entry_id)
        VALUES (?, ?)
        '''
        db.execute(insert_statement, (tag_id, entry_id))


def _get_tags_ids(tags):
    return [get_tag_id(tag) for tag in tags]

if __name__ == '__main__':
    add_entry('test title', 'test txt', ['test1', 'test2'])
