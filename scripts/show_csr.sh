#!/bin/bash

set -e
set -u

if [[ $# -lt 1 ]] ; then
	echo "Usage:   ./show_csr.sh <FILE>"
	echo "Example: ./show_csr.sh abcxyz.crt"
	exit 1
fi

readonly FILE="$1"
if [ "$(head -n1 "$FILE" | cut -b-10)" = "-----BEGIN" ] ; then
	readonly IN_FORM=pem
else
	readonly IN_FORM=der
fi

openssl req -in "$FILE" -inform "$IN_FORM" -noout -text -verify
