use strict;
use warnings FATAL => 'all';
use utf8;

use DBI;


sub add_entry {
    my ($title, $text, $tags) = @_;
    my $dbh = DBI->connect('DBI:SQLite:dbname=mltm.db', '', '');
}

sub get_tag_id {
    my ($tag) = @_;
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