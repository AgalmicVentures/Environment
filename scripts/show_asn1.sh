#!/bin/bash

set -e
set -u

if [[ $# -lt 1 ]] ; then
	echo "Usage:   ./show_asn1.sh <FILE>"
	echo "Example: ./show_asn1.sh abcxyz.crt"
	exit 1
fi

readonly FILE="$1"
if [ "$(head -n1 "$FILE" | cut -b-10)" = "-----BEGIN" ] ; then
	readonly IN_FORM=pem
else
	readonly IN_FORM=der
fi

openssl asn1parse -in "$FILE" -inform "$IN_FORM"
