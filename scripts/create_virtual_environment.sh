#!/bin/bash

# Copyright (c) 2015-2020 Agalmic Ventures LLC (www.agalmicventures.com)
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

set -e
#XXX: no set -u because Python virtual environments are a bit shoddy

if [[ $# -lt 1 ]] ; then
	readonly NAME=env
else
	readonly NAME="$1"
fi

python3 -m venv "$NAME"

#Install requirements if they exist
if [ -e requirements.txt ] ; then
	# shellcheck disable=SC1090
	source "$NAME/bin/activate"
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt
fi
