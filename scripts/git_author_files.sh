#!/bin/bash

set -u

if [[ $# -lt 1 ]]
then
	echo "Returns a list of files edited by the given author"
	echo "Usage:   ./git_author_files.sh <AUTHOR>"
	echo "Example: ./git_author_files.sh \"Ian Hutchinson\""
	exit 1
fi

git log --pretty="%H" --author="$1" |
	while read HASH
	do
		git show --oneline --name-only $HASH | tail -n+2
	done | sort | uniq
