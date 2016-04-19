#!/bin/bash

if [[ $# -lt 2 ]]
then
	echo "Usage:   ./git_find_author.sh <AUTHOR> <PATTERN>"
	echo "Example: ./git_find_author.sh Ian *.[ch]"
	exit 1
fi

for FILE in `find . -name $2 | sort`
do
	git blame --line-porcelain $FILE | sed -n "s/^author $1//p" | sort | uniq -c | sort -rn | awk '{printf "%s", $1}'
	echo " $FILE"
done | sort -rn
