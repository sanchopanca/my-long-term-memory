CREATE TABLE IF NOT EXISTS entries
(
    title TEXT,
    content TEXT
);

CREATE TABLE IF NOT EXISTS tags
(
    name TEXT
);

CREATE TABLE IF NOT EXISTS tags_entries
(
    tag_id INTEGER,
    entry_id INTEGER,
    PRIMARY KEY (tag_id, entry_id)
)
WITHOUT ROWID;

