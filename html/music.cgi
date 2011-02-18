#!/usr/bin/perl

# $Id: music.cgi,v 1.1.1.1 2004/09/20 00:50:55 todd Exp $

use CGI qw/:standard *table *TR *td *center center *div/;
use CGI::Carp qw/fatalsToBrowser/;
use CGI::Pretty;

use lib '/Users/todd/lib/todd';
use DebugWeb;

use lib '/Users/todd/projects/music';
use Music::DB::Web;
my $mp3 = Music::DB::Web->new(-user => 'root',
			      -pass => 'root',
			      -dsn  => 'todds');

my $full_url = url();

#my $DEBUG++;

## Variables that might get passed in the url
## Artist, Album
## display used to indicate if we are trying to display:
##          artists, albums, letters, genres - later can inlcude songs

my $columns = {
	       album      => ['#','track','artist','time','bitrate','my rating',
			      'overall rating','my playcount','overall playcount'],
	       AlbumList  => [qw|album artist year|],
	       artist     => ['album','year'],		
	       ArtistList => [qw/artist albums/],
	       GenreList  => ['genre','# of artists'],
	       genre      => [qw/artist/]};

display_playlists if (url_param('action') eq 'add_to_playlist');

print_header();

# Previous invocations.
# Handling searches...
# Handling link-ins to specific objects...
# Handling link-ins to general browsing...

my $results = $mp3->process_requests();

# Top-tier levels of browsing
# Each list object contains summary statistics that
# might be useful for presentation at the top of a page
# and then an array reference of those object types...
display_list($results)     if ((ref $results) =~ /List/);

# Second tier levels of browsing
# These are more specific types of objects.
display_album($results)    if (ref $results eq 'Music::DB::DataTypes::Album');
display_artist($results)   if (ref $results eq 'Music::DB::DataTypes::Artist');
display_genre($results)    if (ref $results eq 'Music::DB::DataTypes::Genre');
display_song($results)     if (ref $results eq 'Music::DB::DataTypes::Song');

# Searching
display_search_form() if (url_param('action') eq 'search');
print end_html;

#####################################################################
#    END MAIN
#####################################################################








#####################################################################
#   Single-entry reports for artist, album, genre, song
#####################################################################
# THE FORMATTING HERE IS PROBABLY SCREWED UP
sub display_album {
  my $album = shift;
  my $title = 'Album Report: ' . $album->album;
  
  # Unfortunately, the album object doesn't have type in it. crap.
  # Must iterate over the songs to extract information on the album
  my $artists = $album->contributing_artists;
  my $art;
  if (scalar @$artists > 1) {
    $title .= ' (Various Artists)';
    $art = 'Various Artists';
  } else {
    $title .=  ' (' . $artists->[0] . ')';
    $art = $artists->[0];
  }

  # Try printing a little table right here of album stats
  print start_table();
  print TR(td('Album'),td($album->album)),
    TR(td('Artist'),td($art)),
      TR(td('Year'),td($album->{year}));
  print end_table;
  
  table_header($title,$album);
  print_object($album) if ($DEBUG);
  
  # Conditionally set column headers if it's a compilation CD
  # Would also like to print artists within columns if this is a compilation CD
  my $count;
  my @songs = $album->songs;
  my $total;
  foreach my $song (@songs) {
    $total++;
    $count = ($count eq 'one' ) ? 'two' : 'one';
    print_object($song) if ($DEBUG);
    
    print start_TR({-class=>"shade$count"});
    $mp3->print_checkboxes($song,$total);
    my $track;
    if ($song->total_tracks) {
      $track = $song->track . '/' . $song->total_tracks;
    } else {
      $track = $song->track;
    }
    
    # I should only print the artist column if this is a compilation CD
    # build_url should be passed the object?
    # or should I just extract the object from the referrer?
    print
      td($track),
	td($song->build_url()),
	  td($song->build_url('artist')),
	    td($song->duration),
	      td($song->bitrate),
		td($song->uber_playcount),
		  td($song->uber_rating),
		    end_TR;
  }
  end_list();

  #### 
  #### Old deprecated code that may be 
  #### useful for formatting of compilation CDs
  ####
  
  ### This does not work for compilation CDs
  #sub display_album {
  #  my ($album,$songs) = @_;
  
  #  # This is silly to do all of this stuff here - what if it is a compilation?
  #  my @col_headers;
  #  if ($album->{type} == 'compilation') {
  #    @col_headers = (qw{Track Song Artist Length Bitrate Filesize}) 
  #      #  } elsif (lc $h->{album} eq 'singles') {
  #      #    @col_headers = ('','Song','Length','Bitrate','Filesize');
  #  } else {
  #    @col_headers = (qw{Track Song Length Bitrate Filesize});
  #  }
  
  #  # Set up the main header table...
  #  my $artist_url = build_url($album->{artist},$album->{artist_id},'artist');
  #  my $album_url  = build_url($h->{album},$album->{album_id},'album');
  
  #  #  my ($amg_link) = amg_link($h->{artist},'AMG');
  
  #  # Change the config of this table a bit for compilations
  #  $artist_url    = 'Various Artists' if ($album->{album_type} eq 'compilation');
  
  #  # Yuck! This is extremely ugly
  #  print 
  #    start_table({-border=>0,-width=>'50%'}),
  #      Tr(td({-bgcolor=>$greyshade,align=>'right'},b("Album")),
  #	 td({-bgcolor=>$blue},b($album_url))),
  #	   Tr(td({-bgcolor=>$greyshade,align=>'right'},b("Artist")),
  #	      td({-bgcolor=>$blue},b($artist_url)));
  #  print
  #    Tr(td({-bgcolor=>$greyshade,align=>'right'},b("Year Released")),
  #       td({-bgcolor=>$blue},b($h->{year_released}))) if ($h->{year_released});
  #    print
  #      Tr(td({-bgcolor=>$greyshade,align=>'right'},b("Genre")),
  #         td({-bgcolor=>$blue},b($genres))),
  #  	 Tr(td({-bgcolor=>$greyshade,align=>'right'},
  #  	       b("Additional Info")),
  #  	    td({-bgcolor=>$blue},b($amg_link))), end_table;
  
  #  print
  #      start_center,
  #        start_table({-width=>$tab_width}), 
  #  	Tr({-align=>'left'},
  #  	   th(\@col_headers));
  
  #  my @rows;
  #  my $count;
  #  if ($album->{type} eq 'compilation') {
  #    foreach (@$songs) {
  #      my $artist_url = build_url($_->{artist},$_->{artist_id},'artist');
  
  #      push (@rows,td([++$count,
  #		      $_->{title},
  #		      $artist_url,
  #		      $_->{duration},
  #		      $_->{bitrate},
  #		      $_->{filesize}]));
  #    }
  #  } else {
  #    foreach (@$songs) {
  #      push (@rows,td([++$count,
  #		      $_->{title},
  #		      $_->{duration},
  #		      $_->{bitrate},
  #		      $_->{filesize}]));
  #    }
}

sub display_genre {
  my $genre = shift;
  print start_div({-id=>"report"});
  print div({-class=>'reporttitle'},'GENRE REPORT');
  
  print b($genre->genre),p;
  
  print_object($genre) if ($DEBUG);

  # Fetch out the columns
  print start_form();
  my @columns = fetch_columns('genre');
  print 
    start_table(-width=>'100%'),
      TR(td(\@columns));
  
  foreach my $artist ($genre->artists) {
      print_object($artist) if ($DEBUG);
      print start_TR();
      print td(checkbox({-name=>stream,
			 -label=>''}));
      print td($artist->build_url());
      print end_td,end_TR;
    }
  print end_table,end_center();
  print end_div;
}


# I'd like to robustify this.  It's kind of boring.
# Add additional formatting of artist,
# Linkouts
# Cover art displays....
sub display_artist {
  my $artist = shift;

  table_header('Artist Report: ' . $artist->artist,$artist);

  my $count = 'one';
  my $total;
  foreach my $album ($artist->albums) {
    $total++;
    $count = ($count eq 'one' ) ? 'two' : 'one';
    print_object($album) if ($DEBUG);
    print start_TR({-class=>"shade$count"});
    $mp3->print_checkboxes($album,$total);
    print start_td(),$album->build_url();
    print span({-class=>'qualifier'},' (contributes songs to)')
      if ($album->type eq 'compilation');
    print end_td;

    print td($album->year),end_TR;
  }
  end_list();
# print end_table,end_center();
#  print end_div;
}


# build_url already has code to build urls from anyobject
# don't ask me how
sub display_song {
  my $song = shift;

  my @general  = (qw/title album artist year duration bitrate genre track total_tracks/);
  my @file     = (qw/filename filesize filepath/);
  my @encoding = (qw/channels samplerate tagtypes type/);

#  table_header('Song Report: ' . $song->{title},$song);
  print_object($song) if ($DEBUG);
  # end_list();
  print h4('General Information');
  print start_table();
  foreach (@general) {
    my $field;
    if (($_ eq 'artist') || ($_ eq 'album')) {
      $field = $song->build_url($_),
    } else {
      $field = $song->{$_};
    }
    print TR(td({-class=>'songlabel'},ucfirst $_,': '),
	     td({-class=>'songfield'},$field));
  }
  print end_table;


  print h4('Popularity');
  print start_table();
  print TR(td({-class=>'songlabel'},ucfirst 'Playcount: '),
	   td({-class=>'songfield'},''));
  print TR(td({-class=>'songlabel'},ucfirst 'Last Played'),
	   td({-class=>'songfield'},''));
  print TR(td({-class=>'songlabel'},ucfirst 'Avg Rating'),
	   td({-class=>'songfield'},''));
  print end_table;

  print h4('Appears On Playlists');
  print start_table();
  print end_table;

  print h4('File Information');
  print start_table();
  foreach (@file) {
    #    print ucfirst $_,': ',$song->{$_},br;
    print TR(td({-class=>'songlabel'},ucfirst $_,': '),
	     td({-class=>'songfield'},$song->{$_}));
  }
  print end_table;
  
  print h4('Encoding Information');
  print start_table();
  foreach (@encoding) {
    print TR(td({-class=>'songlabel'},ucfirst $_,': '),
	     td({-class=>'songfield'},$song->{$_}));
  }
  print end_table;
}





#####################################################################
#   Multi-item reports (when more than one result is returned)
#####################################################################
sub table_header {
  my ($title,$object) = @_;
  print_object($object) if ($DEBUG);
  my @columns = fetch_columns($object->class);
  
  # I need to be more clever with the titling.
  print 
    start_div({-id=>'report'}),
      div({-class=>'reporttitle'},$title),
	start_form(),
	    start_table({-width=>'100%'}),
	    TR({-class=>'colheaders'},
	       td(\@columns));
}

sub results_row {
  my ($type,$record,$total)= @_;
  my @cells;
  if ($type =~ /album/i) {
    push (@cells,
	  $record->build_url('album'),
	  $record->build_url('artist'),
	  $record->year);
  } elsif ($type =~ /artist/i) {
    push (@cells,
	  $record->build_url(),
	  $record->total_albums);
  } else {
    push (@cells,
	  $record->build_url(),
	  $record->total_artists);
  }
  
  $mp3->{hilite} = ($mp3->{hilite} eq 'one' ) ? 'two' : 'one';
  print_object($record) if ($DEBUG);
  print start_TR({-class=>"shade" . $mp3->{hilite}});
  $mp3->print_checkboxes($record,$total);
  print td(\@cells),end_TR;
  return;
}

sub end_list {
  print end_table;
  print hr;
  $mp3->buttons();

  # This is a quick hack to make a javapopup window
  # showing available playlists
  print end_div,end_div;
}

sub display_list {
  my $list = shift;
  my %titles = (
		AlbumList  => 'Album List',
		ArtistList => 'Artist List',
		GenreList  => 'Genre List');

  # Stored list is the general type of list contained
  # with the master object...

  # Am I browsing?  Let's attach the letter as well...
  my $stored_type = $list->class;
  my $title = $titles{$stored_type};
  if (url_param('action') eq 'browse') {
    my $class = url_param('class');
    $title .= '-Browsing ' . ucfirst $class . 's: ' . url_param($class);
  }
  
  table_header($title,$list);
  my $total;
  foreach my $record ($list->$stored_type) {
    $total++;
    # Now I need to specify which fields I want...
    results_row($stored_type,$record,$total);
  }
  end_list();
}


#####################################################################
#   CONFIGURATION
#####################################################################



#####################################################################
#   BOILERPLATE HTML
#####################################################################
sub fetch_columns {
  my $index = shift;
  my @columns;
  push (@columns,'select','stream',@{$columns->{$index}});
  return @columns;
}

sub display_search_form {   # Setup the default search page
  print startform(-action=>$full_url),
    start_center,
      table({-width=>'50%'},
	    th({-colspan=>3,},uc "search " . url_param('class') . 's'),
	    TR(
	       td("Terms:"),
	       td(textfield(-name=>'search_term',
			    -size=>'30',
			    -maxlength=>100)),
	       td({-colspan=>3},
		  popup_menu(-name=>'class',
			     -values=>['Artist',
				       'Album',
				       'Song',
				       'Year Released',
				       'Genre'],
			     -default=>'Artist')),
	       td(submit(-name=>'search_button',
			 -value=>'Search'))));
  print endform,end_center;
}



sub print_start_table {
  my $headings = @_;
  print start_center,
    start_table({-border=>"0",
		 -width=>'80%'});
  print th({-align=>'left'},\@$headings);
  return;
}

sub banner {
  print div({-id=>'banner'},
	    div({-class=>'biglink'},
		'MP3::DB::Web'),
	    div({-id=>'tagline'},
		span({-class=>'left'},
		     'Because sometimes your brain needs to rest.'),
		     #br,'Perl Modules For Database-driven web sharing of MP3s'),
		span({-class=>'right'},
		     span({-class=>'nav'},
			  'Browse:  ',
			  join(' | ',
			       a({-href=>"/music/music.cgi?action=browse&class=artist"},'Artists'),
			       a({-href=>"/music/music.cgi?action=browse&class=album"},'Albums'),
			       a({-href=>"/music/music.cgi?action=browse&class=genre"},'Genres')),
			  br,
			  'Search:  ',
			  join(' | ',
			       a({-href=>"/music/music.cgi?action=search&class=artist"},'Artists'),
			       a({-href=>"/music/music.cgi?action=search&class=album"},'Albums'),
			       a({-href=>"/music/music.cgi?action=search&class=song"},'Songs')),
			 ))));
}


sub display_playlists {
  print header;
  print start_html;
  print "hello";
  print end_html;
  exit;
}


sub print_header {
  my $script = <<END;
    function OpenPlaylists (c) {
      window.open('playlists.cgi?' +
                      'action=add_to_playlist&user_id=' + c,
                      'comment',
                      'width=200,height=200,scrollbars=yes,status=yes');
  }
END
  print header(-cookie=>$mp3->{cookie});
  
  # Switch the header based on the type of result...
  # THIS NEEDS TO BE REWRITTEN
  my $msg = "debug";
  
  print start_html(-title=>$msg,
		   -style=>{-src=>"/music/music.css"},
		   -script=>$script);
  banner();

  print start_div({-id=>"wrapper"});
  print start_div({-id=>"sidebar"});
  
  print h4("Browse Artists");
  $mp3->table_navigation(-type=>'artist',-span=>9);
  
  print h4("Browse Albums");
  $mp3->table_navigation(-type=>'album',-span=>9);
  
  # This is really ugly...
  print h4(a({-href=>"/music/music.cgi?action=browse&class=genre"},'Browse Genres...'));
  
  print hr;
  print h4(a({-href=>"/music/music.cgi?action=search&class=artist"},'Search Artists'));
  print h4(a({-href=>"/music/music.cgi?action=search&class=album"},'Search Albums'));
  print h4(a({-href=>"/music/music.cgi?action=search&class=song"},'Search Songs'));

  print hr;
  print h4($mp3->build_nav_link(-class  => 'playlist',
			    -action => 'display_options',
			    -text   => 'My Playlists'));
  print h4($mp3->build_nav_link(-class  => 'playlist',
			    -action => 'all_playlists',
			    -text   => 'All Playlists'));

  print hr;
  print h4('Recently Played');
  print h4('Most Often Played');
  print h4('My Preferences');

  print hr;
  print h4('Statistics');
  print h4($mp3->build_nav_link(-class  =>'admin',
			    -action => 'display_options',
			    -text   => 'System Admin'));
  print h4($mp3->build_nav_link(-class  => 'about',
			    -action => 'display',
			    -text   => 'About::MP3::DB'));
  print end_div;
  print end_div;

  print start_div({-id=>"content"});
  
  # Debugging
  #  foreach (keys %{$mp3->{cookie}}) {
  #    print $_,"    :    ",$mp3->{cookie}->{$_},br;
  #    if ($_ eq 'value') {
  #      my %hash = @{$mp3->{cookie}->{$_}};
  #      print join(br,keys %hash),br,br;
  #    }
  #  }
  if ($mp3->{cookie} eq 'NOT AUTHENTICATED' || $mp3->{cookie} eq 'BOGUS GUESS') {
    print_login();
  } else {
    print_about() if (!param || url_param('about'));
  }
}


sub print_login {
  if ($mp3->{cookie} eq 'BOGUS GUESS') {
    print "The username or password entered was incorrect.";
  }

  print h3("Please Log In");
  print start_table();
  print start_form;
  print TR(td('Username: '),td(textfield(-name=>'username')));
  print TR(td('Password: '),td(password_field(-name=>'password')));
  print TR(td({-colspan=>'2'},submit(-name=>'submit',-value=>'Log In')));
  print end_form;
  print end_html;
  exit;
}

sub print_about {
  print h2("MP3::DB");
  
  print h4("Overview");
  print p("MP3::DB is a series of Perl modules for building relational databases of MP3s");
  
  print h4("Features");
  print p("- Build a relational database directly from ID3 tags.");
  print p("- Provide web-accessible access to your collection, complete with streaming.");
  print p("- Multiple users, multiple playlists, ratings, and playcounts!");
  print p("- Supports a variety of databases through an extensible dbi-based plugin architecture.");
  print p("- Generate customized graphical reports of your MP3 collection.");

  print h4("General Documentation");
  print p("- System Requirements.");
  print p("- Configuring and Using MP3::DB::Web.");

  print h4("Developer Documentation");
  print p("- perldoc MP3::DB - perl module that simplifies construction of MP3 databases.");
  print p("- perldoc MP3::DB::Web - a module for presenting your data on the web.");
  print p("- perldoc MP3::DB::Util::Rearrange");
  print end_div;
}


__END__;
