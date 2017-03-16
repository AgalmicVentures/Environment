#!/bin/bash

set -u

if [[ $# -lt 2 ]]
then
	echo "Usage:   ./create_ramdisk.sh <NAME> <SIZE>"
	echo "Example: ./create_ramdisk.sh ramdisk 16G"
	exit 1
fi

NAME=$1
SIZE=$2

cd /mnt
mkdir $NAME
mount -t tmpfs -o size=$SIZE tmpfs $NAME
cd -

echo
df -h
echo
free -g
echo
