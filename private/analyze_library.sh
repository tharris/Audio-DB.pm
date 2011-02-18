#!/bin/sh
LIBRARY=$1

DATE=`date "+%Y%m%d"`

if [ -n "$LIBRARY" ]
then
   echo "using library ${LIBRARY}..."
else 
   scp poudre:'/Users/todd/Music/iTunes/iTunes\ Music\ Library.xml' library.xml
   LIBRARY="/Users/todd/projects/Audio-DB.pm/private/library.xml"
fi

echo "Creating database (music_${DATE}) from ${LIBRARY}..."
../bin/create_database.pl --user root --pass kentwashere --dsn music_${DATE} --library ${LIBRARY} --adaptor dbi::mysql

echo "Creating report from music_${DATE}..."
./test_all.sh music_${DATE}
