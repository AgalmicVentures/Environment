#!/bin/bash

# Copyright (c) 2015-2017 Agalmic Ventures LLC (www.agalmicventures.com)
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

set -eu

if [ "$EUID" -eq 0 ] ; then
	echo "Run this script as the user who will use sublime, rather than root."
	exit 1
fi

##### Install System Packages #####

#Utilies
PACKAGES="geany git gparted ssh valgrind"

#Databases
PACKAGES="$PACKAGES postgresql rabbitmq-server"

#C/C++
PACKAGES="$PACKAGES libboost-dev"

#Python
PACKAGES="$PACKAGES python3-venv python3-pip"

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get -y install "$PACKAGES"
sudo apt-get autoclean

##### Install 3rd Party Software #####

#Sublime text
wget https://download.sublimetext.com/sublime_text_3_build_3126_x64.tar.bz2
tar -xvf sublime_text_3_build_3126_x64.tar.bz2
