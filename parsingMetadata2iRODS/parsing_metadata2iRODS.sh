#!/bin/bash


main(){
	locate namefile
	namefile="$@"

	CMD="/usr/bin/python2.7 /var/lib/irods/iRODS/server/bin/cmd/parsingMetadata2iRODS_libraryiRODS.py "$namefile
	eval $CMD
}

echo "begin bash"
main $@
