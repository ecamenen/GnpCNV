#!/bin/bash


main(){
	locate namefile
	namefile="$1"

	execute=$(python /home/ecamenen/Documents/git/GnpCNV/parsingMetadata2iRODS/parsing_metadata2iRODS.py $namefile)
	echo "$execute"
}

main $1

