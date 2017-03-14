from mltm.database import DB


db = DB()


# TODO Optimize
class Entry:
    def __init__(self, id, title, content, tags):
        self.id = id
        self.title = title
        self.content = content
        self.tags = tags

    def __repr__(self):
        return 'id: {}, title: {}, content: {}, tags: {}'.\
            format(self.id, self.title, self.content, self.tags)

    def match(self, text):
        if text in self.tags:
            return True
        if text in self.title:
            return True
        if text in self.content:
            return True
        for tag in self.tags:
            if text in tag:
                return True
        return False

    def display(self):
        return 'ID: {}\n{}\n\n{}\n{}\n'.format(self.id, self.title, self.content, ', '.join(self.tags))

    @staticmethod
    def add_entry(title, text, tags):
        tags_ids = _get_tags_ids(tags)
        insert_statement = '''
        INSERT INTO entries (title, content)
        VALUES (?, ?)
        '''
        db.execute(insert_statement, (title, text))
        entry_id = db.get_last_rowid()
        _update_tags_to_entry(tags_ids, entry_id)

    @staticmethod
    def get_entry_by_id(entry_id):
        select_statement = '''
        SELECT entries.title,
               entries.content
        FROM entries
        WHERE rowid = ?
        '''
        entry = db.execute_and_fetch_one(select_statement, (entry_id,))
        if entry is None:
            return None
        select_statement = '''
        SELECT tags.name
        FROM tags
        INNER JOIN tags_entries ON tags.rowid = tags_entries.tag_id
        WHERE tags_entries.entry_id = ?
        '''
        tags = _transpose(db.execute_and_fetch_all(select_statement, (entry_id,)))
        title, content = entry
        return Entry(entry_id, title, content, tags)

    @staticmethod
    def search_by_tag_id(tag_id):
        select_statement = '''
        SELECT entries.rowid
        FROM entries
        INNER JOIN tags_entries ON entries.rowid = tags_entries.entry_id
        WHERE tags_entries.tag_id = ?
        '''
        entries_ids = _transpose(db.execute_and_fetch_all(select_statement, (tag_id,)))
        return [Entry.get_entry_by_id(entry_id) for entry_id in entries_ids]

    @staticmethod
    def get_all():
        select_statement = '''
        SELECT rowid
        FROM entries
        '''
        ids = _transpose(db.execute_and_fetch_all(select_statement))
        return [Entry.get_entry_by_id(id) for id in ids]

    @staticmethod
    def search_arbitrary_text(text):
        return [entry for entry in Entry.get_all() if entry.match(text)]


def get_tag_id(tag, insert_new=False):
    select_statement = '''
    SELECT rowid
    FROM tags
    WHERE name = ?
    '''
    tag_id = db.execute_and_fetch_one(select_statement, (tag,))
    if tag_id is None and insert_new:
        insert_statement = '''
        INSERT into tags (name)
        VALUES (?)
        '''
        db.execute(insert_statement, (tag,))
        tag_id = db.get_last_rowid()
    return tag_id


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
    return [get_tag_id(tag, insert_new=True) for tag in tags]


def _transpose(x):
    return list(next(zip(*x), ()))  # Sorry

if __name__ == '__main__':
    print(Entry.search_arbitrary_text('txt'))
