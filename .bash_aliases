export HISTCONTROL=erasedups # don't store duplicate lines
export HISTSIZE=100000 #remember 100k unique lines
shopt -s histappend

#fast type
alias cd..='cd ../'                         # Go back 1  level
alias ..='cd ../'                           # Go back 1  level
alias ...='cd ../../'                       # Go back 2  levels
alias .3='cd ../../../'                     # Go back 3  levels
alias .4='cd ../../../../'                  # Go back 4  levels
alias .5='cd ../../../../../'               # Go back 5  levels
alias .6='cd ../../../../../../'            # Go back 6  levels
alias c='clear'

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
