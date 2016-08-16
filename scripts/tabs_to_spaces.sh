#!/bin/bash

if [[ $# -eq 0 ]]
then
	echo "Usage: ./tabs_to_spaces.sh <FILE> [<FILE> ...]"
fi

UNAME=`uname`
if [ $UNAME == "Darwin" ]
then
	sed -i '' -e $'s|[\t]|    |g' $@
else
	sed --in-place -e $'s|[\t]|    |g' $@
fi
