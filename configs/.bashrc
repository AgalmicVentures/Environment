
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

#Load colors
readonly NC='\033[00m'
readonly RED='\033[1;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'

#Load Mercurial completions
if [ -e /etc/bash_completion.d/mercurial ] ; then
	source /etc/bash_completion.d/mercurial
fi

#Check the configuration at regular intervals
if [ -e ~/check_config.sh ] || [ -L ~/check_config.sh ] ; then
	if [ "$(find ~ -name .check_config -maxdepth 1 -mtime +30)" == "" ] ; then
		touch ~/.check_config
		~/check_config.sh
	fi
fi

########## Prompt ##########

prompt() {
	RETURN=$?

	PS1="\n[\[$YELLOW\]\D{%Y-%m-%d %H:%M:%S}\[$NC\]]\n\[$GREEN\]\u@\h\[$NC\]:\[$LIGHT_GREEN\]\w\[$NC\] \[$RED\]=>\[$NC\] "

	if [[ $RETURN -ne 0 ]]
	then
		PS1="\n${RED}Non-zero exit code: ${RETURN}${NC}\n${PS1}"
	fi

	export PS1=$PS1
}
PROMPT_COMMAND=prompt

########## Aliases ##########

#Flags are slightly different on Mac than Linux
UNAME=$(uname)
if [[ $UNAME == "Darwin" ]] ; then
	export JAVA_HOME="/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home"

	alias ls="ls -G"
else
	alias ls="ls --color=auto"
fi

alias ll="ls -lAh"

#Enable coloring
alias grep="grep --color=auto"
alias egrep="egrep --color=auto"

#Handle typos
alias gti=git

#Moving up directories
up() {
	local d=""
	limit=$1
	for ((i=1 ; i <= limit ; i++)) ; do
		d=$d/..
	done
	d=$(echo $d | sed 's/^\///')
	if [ -z "$d" ] ; then
		d=..
	fi
	cd $d
}

#Extraction
extract() {
	if [ -f $1 ] ; then
		case $1 in
			*.tar.bz2)   tar xvjf $1    ;;
			*.tar.gz)    tar xvzf $1    ;;
			*.bz2)       bunzip2 $1     ;;
			*.rar)       unrar x $1       ;;
			*.gz)        gunzip $1      ;;
			*.tar)       tar xvf $1     ;;
			*.tbz2)      tar xvjf $1    ;;
			*.tgz)       tar xvzf $1    ;;
			*.zip)       unzip $1       ;;
			*.Z)         uncompress $1  ;;
			*.7z)        7z x $1        ;;
			*)			echo "Don't know how to extract '$1'..." ;;
		esac
	else
		echo "'$1' is not a valid file!"
	fi
}
