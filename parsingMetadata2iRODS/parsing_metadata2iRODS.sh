#!/bin/bash


main(){
local execute nbLine
namefile="$1"

execute=$(python /home/ecamenen/Documents/python/test3.py $namefile)
echo "$execute"
}

main $1

