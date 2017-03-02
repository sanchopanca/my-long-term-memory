use strict;
use warnings FATAL => 'all';
use utf8;

use DBI;

my $dbh = DBI->connect('DBI:SQLite:dbname=mltm.db', '', '');

sub add_entry {
    my ($title, $text, $tags) = @_;
    my @tags_ids;
    for my $tag (@{ $tags }) {
        push(@tags_ids, get_tag_id($tag));
    }
    my $insert_statement = <<'    --';
    INSERT INTO entries (title, content)
    VALUES (?, ?)
    --
    $dbh->do($insert_statement, $title, $text);
    my $entry_id = _get_last_inserted_id('entries');
    _connect_tags_to_entry(\@tags_ids);
}

sub get_tag_id {
    my ($tag) = @_;
    return 0;
}

sub search_by_tag_id {
    my ($tag_id) = @_;
}

sub search_arbitrary_text {
    my ($search_text) = @_;
}

sub update_entry {
    my ($id, $title, $text, $tags) = @_;
}

sub _connect_tags_to_entry {
    my ($tags_ids, $entry_id) = @_;
}

sub _get_last_inserted_id {
    my ($table) = @_;
    return 0;
}