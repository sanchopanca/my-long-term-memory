from database import DB


db = DB()


class Entry:
    def __init__(self, id, title, text, tags):
        self.id = id
        self.title = title
        self.text = text
        self.tags = tags

    def __repr__(self):
        return 'id: {}, title: {}, text: {}, tags: {}'.\
            format(self.id, self.title, self.text, self.tags)


def add_entry(title, text, tags):
    tags_ids = _get_tags_ids(tags)
    insert_statement = '''
    INSERT INTO entries (title, content)
    VALUES (?, ?)
    '''
    db.execute(insert_statement, (title, text))
    entry_id = db.get_last_rowid()
    _update_tags_to_entry(tags_ids, entry_id)


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
    title, text = entry
    return Entry(entry_id, title, text, tags)


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


def search_by_tag_id(tag_id):
    select_statement = '''
    SELECT entries.rowid
    FROM entries
    INNER JOIN tags_entries ON entries.rowid = tags_entries.entry_id
    WHERE tags_entries.tag_id = ?
    '''
    entries_ids = _transpose(db.execute_and_fetch_all(select_statement, (tag_id,)))
    return [get_entry_by_id(entry_id) for entry_id in entries_ids]


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
    return [get_tag_id(tag, insert_new=True) for tag in tags]


def _transpose(x):
    return list(next(zip(*x), ()))  # Sorry

if __name__ == '__main__':
    print(search_by_tag_id(1))
