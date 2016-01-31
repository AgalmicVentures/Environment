
#Load colors
NC='\033[00m'
RED='\033[1;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'

#Load Mercurial completions
if [ -e /etc/bash_completion.d/mercurial ]
then
	source /etc/bash_completion.d/mercurial
fi

UNAME=`uname`

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
if [[ $UNAME == "Darwin" ]]
then
	export JAVA_HOME="/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home"

	alias ls="ls -G"
else
	alias ls="ls --color=always"
fi

alias ll="ls -lAh"

#Enable coloring
alias grep="grep --color=auto"
alias egrep="egrep --color=auto"

#Moving up directories
up() {
	local d=""
	limit=$1
	for ((i=1 ; i <= limit ; i++))
		do
			d=$d/..
		done
	d=$(echo $d | sed 's/^\///')
	if [ -z "$d" ]; then
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
