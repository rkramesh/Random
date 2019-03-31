export HISTCONTROL=erasedups # don't store duplicate lines
export HISTSIZE=100000 #remember 100k unique lines
shopt -s histappend

#mac
# Set Tab name to a Workingdrectory
tab() {
	if [ "$PWD" != "$MYOLDPWD" ]; then
		MYOLDPWD="$PWD";
		printf "\e]1;${PWD##*/}\a"
	fi
}
export PROMPT_COMMAND=tab
# Set window name to a custom string
function winname {
	printf "\e]2;$1\a"
}
#mac
#fast type
alias cd..='cd ../'                         # Go back 1  level
alias ..='cd ../'                           # Go back 1  level
alias ...='cd ../../'                       # Go back 2  levels
alias .3='cd ../../../'                     # Go back 3  levels
alias .4='cd ../../../../'                  # Go back 4  levels
alias .5='cd ../../../../../'               # Go back 5  levels
alias .6='cd ../../../../../../'            # Go back 6  levels
alias c='clear'
alias lt="ls -altr"
alias cp='cp -iv'                           # Preferred 'cp' implementation
alias mv='mv -iv'                           # Preferred 'mv' implementation
alias mkdir='mkdir -pv'                     # Preferred 'mkdir' implementation
alias ll='ls -FGlAhp'                       # Preferred 'ls' implementation
alias less='less -FSRXc'                    # Preferred 'less' implementation
cd() { builtin cd "$@"; ll; }               # Always list directory contents upon 'cd'

# Python server
#   ------------------------------------------------------------
alias server='python -m SimpleHTTPServer 8000'
alias lr='ls -R | grep ":$" | sed -e '\''s/:$//'\'' -e '\''s/[^-][^\/]*\//--/g'\'' -e '\''s/^/   /'\'' -e '\''s/-/|/'\'' | less'
alias ips="ifconfig -a | perl -nle'/(\d+\.\d+\.\d+\.\d+)/ && print $1'"

alias apt='sudo apt-get install -y'

#pi

ip="sudo nmap -nsP 192.168.1.250/24| grep -b2 'Pi' | sed  -r -n -e '1s#.*for\s(.*)#\1#p'"

function pish
{
ip=`sudo nmap -nsP 192.168.1.250/24| grep -b2 'Pi' | sed  -r -n -e '1s#.*for\s(.*)#\1#p'`
   sshpass -p toor ssh -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null root@$ip
if [ "$?" != "0" ]
then
   sshpass -p libreelec ssh -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null root@$ip
fi
}

#vi

alias vi='vim'

#basic 

#kodi
alias kboot='sudo systemctl restart mediacenter'
alias klog='tail -f /home/osmc/.kodi/temp/kodi.log'
kplay(){ kodi-send --action="PlayMedia($1)"; }
