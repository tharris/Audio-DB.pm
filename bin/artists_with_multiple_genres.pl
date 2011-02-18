#!/usr/bin/perl

use Audio::DB::Reports;
use Getopt::Long;
use Pod::Usage;
use strict;

my ($adaptor,$dsn,$user,$pass,$host);
GetOptions('adaptor=s' => \$adaptor,
	   'dsn=s'     => \$dsn,
	   'user=s'    => \$user,
	   'pass=s'    => \$pass,
	   'host=s'    => \$host,
	  );

pod2usage(-verbose => 2) unless ($dsn);

$adaptor ||= 'dbi::mysql';

# Create a new Audio::DB object...
my $report = Audio::DB::Reports->new(-adaptor => $adaptor,
				     -user    => $user,
				     -pass    => $pass,
				     -host    => $host,
				     -dsn     => $dsn);

my $artists = $report->artists_with_multiple_genres();
foreach (sort { $a->artist cmp $b->artist } @$artists) {
  my $artist = $_->artist;
  my @genres = $_->genres;
  printf "%-25s %-30s\n",$artist,join("; ",sort { $a cmp $b } map {$_->genre} @genres);
}

__END__


=pod

=head1 NAME

artists_with_multiple_genres - find artists with multiple genres assigned

=head1 SYNPOSIS

This script finds artists that have more than a single genre assigned
to them.

=head1 USAGE

 artists_with_multiple_genres [options]

=head1 OPTIONS

Options [database]
   dsn      the name of your database
   user     database username, if required
   pass     database password if required
   adaptor  either dbi::sqlite or dbi::mysql (defaults to dbi::mysql)

eg:

artists_with_multiple_genres --dsn music

=head1 AUTHOR

 Todd Harris (harris@cshl.org);
 $Id: artists_with_multiple_genres.PLS,v 1.1 2005/02/27 16:56:25 todd Exp $

=cut

