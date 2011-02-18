#!/bin/sh
DSN=$1
ADAPTOR=$2

if [ -n "$ADAPTOR" ]
then
   echo "Using ${ADAPTOR}"
else
   ADAPTOR="dbi::mysql"
fi           

mkdir tmp/
echo "Generating album histogram..."
../bin/album_distribution.pl --dsn ${DSN} --adaptor ${ADAPTOR} --user root --pass kentwashere --width 1000 --height 600 -start 1940 -end 2005 > tmp/albums.png
echo "Generating song histogram..."
../bin/song_distribution.pl --dsn ${DSN} --adaptor ${ADAPTOR} --user root --pass kentwashere --width 1000 --height 600 -start 1940 -end 2005 > tmp/songs.png 
echo "Finding artists with multiple genres assigned..."
../bin/artists_with_multiple_genres.pl --dsn ${DSN} --adaptor ${ADAPTOR} --user root --pass kentwashere > tmp/artists_multiple_genres.txt
echo "Generating full album list..."
../bin/generate_album_list.pl --dsn ${DSN} --adaptor ${ADAPTOR} --user root --pass kentwashere --compressed > tmp/album_list.txt
echo "Generating library statistics..."
../bin/library_statistics.pl --dsn ${DSN} --adaptor ${ADAPTOR} --user root --pass kentwashere  > tmp/library_stats.txt
echo "Finding albums that fall below bitrate threshold..."
../bin/albums_below_threshold.pl --dsn ${DSN} --adaptor ${ADAPTOR} --user root --pass kentwashere -threshold 192 > tmp/albums_below_threshold.txt
echo "Generating genre report..."
../bin/genre_statistics.pl --dsn ${DSN} --adaptor ${ADAPTOR} --user root --pass kentwashere > tmp/genre_stats.txt
