#!/bin/bash

# Copyright (c) 2015-2022 Agalmic Ventures LLC (www.agalmicventures.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

set -u

if [[ $# -lt 2 ]] ; then
	echo "Returns the line counts of the given author in each file whose name matches the given pattern"
	echo "Usage:   ./git_author_line_counts.sh <AUTHOR> <PATTERN>"
	echo "Example: ./git_author_line_counts.sh Ian *.[ch]"
	exit 1
fi

for FILE in $(find . -name "$2" | sort) ; do
	git blame --line-porcelain "$FILE" | sed -n "s/^author $1//p" | sort | uniq -c | sort -rn | awk '{printf "%s", $1}'
	echo " $FILE"
done | sort -rn
