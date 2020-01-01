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

#XXX: can't use this because of Python's virtual environments
#set -u

if [[ $# -lt 2 ]] ; then
	echo 'Usage: ./upgrade_python3_venv.sh <INPUT_REQUIREMENTS_TXT> <OUTPUT_REQUIREMENTS_TXT>'
	exit 1
fi

#Setup a temporary virtual environment, then upgrade each package there
python3 -m venv _upgrade_env
# shellcheck disable=SC1091
source _upgrade_env/bin/activate
python3 -m pip install --upgrade -r "$1"
python3 -m pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 python3 -m pip install -U
python3 -m pip freeze > "$2"
deactivate
rm -r _upgrade_env
