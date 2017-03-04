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
    $dbh->do($insert_statement, $title, $text);
    my $entry_id = _get_last_inserted_id('entries');
    _connect_tags_to_entry($tags_ids, $entry_id);
}

sub get_tag_id {
    my ($tag) = @_;
    my $select_statement = <<'    --';
    SELECT rowid
    FROM tags
    WHERE tag = ?
    --
    my $rows = $dbh->selectall_arrayref($select_statement, tag);
    if (@{ $rows } > 0)) {
        return $rows->[0][0];
    } else {
        my $insert_statement = <<'        --';
        INSERT into tags (tag)
        VALUES (?)
        --
        $db->do($insert_statement, $tag);
        return _get_last_inserted_id('tags');
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
    $dbh->do($update_statement, $title, $text, $id)
    my $tags_ids = _get_tags_ids($tags);
    _update_tags_to_entry($tags_ids, $id);
}

sub _update_tags_to_entry {
    my ($tags_ids, $entry_id) = @_;
}

sub _get_last_inserted_id {
    my ($table) = @_;
    return 0;
}

sub _get_tags_ids {
    my ($tags) = @_;
    my @tags_ids;
    for my $tag (@{ $tags }) {
        push(@tags_ids, get_tag_id($tag));
    }
    return \@tags_ids;
}
