#!/usr/bin/perl

use Audio::DB::Reports;
use Getopt::Long;
use Pod::Usage;
use strict;

my ($adaptor,$dsn,$user,$pass,$host,$threshold,$compressed);
GetOptions('adaptor=s'   => \$adaptor,
	   'dsn=s'       => \$dsn,
	   'user=s'      => \$user,
	   'pass=s'      => \$pass,
	   'host=s'      => \$host,
	   'threshold=s' => \$threshold,
           'compressed'  => \$compressed,
	  );

pod2usage(-verbose => 2) unless ($dsn && $threshold);

$adaptor ||= 'dbi::mysql';

# Create a new Audio::DB object...
my $report = Audio::DB::Reports->new(-adaptor => $adaptor,
				     -user    => $user,
				     -pass    => $pass,
				     -host    => $host,
				     -dsn     => $dsn);

my $albums = $report->albums_below_bitrate_threshold(-threshold=>$threshold,-sort_by=>'artist');

foreach my $album_obj (@$albums) {
  my $artist  = $album_obj->artists;
  my $bitrate = $album_obj->bitrates;
  my $album   = $album_obj->album;
  if ($compressed) {
    $artist = substr($artist,0,15);
    $album  = substr($album,0,15);
    printf ("%-5s %-16s %-16s\n",$bitrate,$artist,$album);
#    printf ("%-10s %-30s\n",$artist,$album);
  } else {
    printf ("%-20s %-20s %-30s\n",$artist,$album,$bitrate);
  }
}

__END__


=pod

=head1 NAME

albums_below_bitrate_threshold - find all albums below a given bitrate threshold

=head1 SYNPOSIS

This script provides an easy way to find all albums below a given
bitrate threshold in your collection.

=head1 OPTIONS

Options
   bitrate  the bitrate threshold to search for in kbps
   dsn      the name of your database
   user     database username, if required
   pass     database password if required
   adaptor  either dbi::sqlite or dbi::mysql (defaults to dbi::mysql)
   compressed only print the artist and album

eg:

 albums_below_bitrate_threshold --dsn music --bitrate 128

=head1 AUTHOR

 Todd Harris (harris@cshl.org);
 $Id: albums_below_threshold.PLS,v 1.1 2005/02/27 16:56:25 todd Exp $

=cut

