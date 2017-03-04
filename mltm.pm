use strict;
use warnings FATAL => 'all';
use utf8;

use DBI;

my $dbh = DBI->connect('DBI:SQLite:dbname=mltm.db', '', '');

sub add_entry {
    my ($title, $text, $tags) = @_;
    my $tags_ids = _get_tags_ids($tags);
    my $insert_statement = <<'    --';
    INSERT INTO entries (title, content)
    VALUES (?, ?)
    --
    $dbh->do($insert_statement, undef, $title, $text);
    my $entry_id = _get_last_inserted_id('entries');
    _update_tags_to_entry($tags_ids, $entry_id);
}

sub get_tag_id {
    my ($tag) = @_;
    my $select_statement = <<'    --';
    SELECT rowid
    FROM tags
    WHERE name = ?
    --
    my $rows = $dbh->selectall_arrayref($select_statement, undef, $tag);
    if (scalar @{ $rows } > 0) {
        return $rows->[0][0];
    } else {
        my $insert_statement = <<'        --';
        INSERT into tags (name)
        VALUES (?)
        --
        $dbh->do($insert_statement, undef, $tag);
        my $id = _get_last_inserted_id('tags');
        return $id;
    }
}

sub search_by_tag_id {
    my ($tag_id) = @_;
}

sub search_arbitrary_text {
    my ($search_text) = @_;
}

sub update_entry {
    my ($id, $title, $text, $tags) = @_;
    my $update_statement = <<'    --';
    UPDATE entries SET
        title = ?,
        content = ?
    WHERE
        rowid = ?
    --
    $dbh->do($update_statement, undef, $title, $text, $id);
    my $tags_ids = _get_tags_ids($tags);
    _update_tags_to_entry($tags_ids, $id);
}

sub _update_tags_to_entry {
    my ($tags_ids, $entry_id) = @_;
    my $delete_statement = <<'    --';
    DELETE FROM tags_entries
    WHERE entry_id = ?
    --
    $dbh->do($delete_statement, undef, $entry_id);
    for my $tag_id (@{ $tags_ids }) {
        my $insert_statement = <<'        --';
        INSERT INTO tags_entries (tag_id, entry_id)
        VALUES (?, ?)
        --
        $dbh->do($insert_statement, undef, $tag_id, $entry_id);
    }
}

sub _get_last_inserted_id {
    my ($table) = @_;
    my $id = $dbh->last_insert_id(undef, undef, $table, 'rowid');
    return $id;
}

sub _get_tags_ids {
    my ($tags) = @_;
    my @tags_ids;
    for my $tag (@{ $tags }) {
        my $id = get_tag_id($tag);
        push(@tags_ids, $id);
    }
    return \@tags_ids;
}
