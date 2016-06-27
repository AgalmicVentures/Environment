#!/bin/bash

set -u

if [[ $# -lt 1 ]]
then
	echo "Returns a list of authors who edited a file"
	echo "Usage:   ./git_file_authors.sh <FILE>"
	echo "Example: ./git_file_authors.sh foo.c"
	exit 1
fi

git blame --line-porcelain $1 | sed -n 's/^author //p' | sort | uniq -c | sort -rn
