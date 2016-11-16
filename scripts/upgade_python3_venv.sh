#!/bin/bash

if [[ $# -lt 2 ]]
then
	echo 'Usage: ./upgrade_python3_venv.sh <INPUT_REQUIREMENTS_TXT> <OUTPUT_REQUIREMENTS_TXT>'
	exit 1
fi

python3 -m venv _upgrade_env
source _upgrade_env/bin/activate
python3 -m pip install --upgrade -r $1
python3 -m pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 python3 -m pip install -U
python3 -m pip freeze > $2
deactivate
rm -r _upgrade_env

