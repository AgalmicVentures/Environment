#!/bin/bash

set -u

if [[ $# -lt 2 ]]
then
	echo "Returns the line counts of the given author in each file whose name matches the given pattern"
	echo "Usage:   ./git_author_line_counts.sh <AUTHOR> <PATTERN>"
	echo "Example: ./git_author_line_counts.sh Ian *.[ch]"
	exit 1
fi

for FILE in `find . -name "$2" | sort`
do
	git blame --line-porcelain $FILE | sed -n "s/^author $1//p" | sort | uniq -c | sort -rn | awk '{printf "%s", $1}'
	echo " $FILE"
done | sort -rn
