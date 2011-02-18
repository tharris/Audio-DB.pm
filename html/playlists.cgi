#!/usr/bin/perl

# $Id: playlists.cgi,v 1.1.1.1 2004/09/20 00:50:55 todd Exp $

use CGI qw/:standard *table *TR *td *center center *div/;
use CGI::Carp qw/fatalsToBrowser/;
use CGI::Pretty;

use lib '/Users/todd/lib/todd';
use DebugWeb;

use lib '/Users/todd/projects_personal/';
use MP3::DB::Web;
my $mp3 = MP3::DB::Web->new(-user=>'todd',
			    -pass=>'riosql',
			    -database=>'music');

my $full_url = url();

print header;
print start_html;
print $mp3->buttons;
print end_html;


