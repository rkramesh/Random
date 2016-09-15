#!/bin/sh
#run this in crontab 


SYNCSCRIPT()
{
SVNEXE="/usr/bin/svn"
SVNREP="/path/to/checkout/repo"
SVNURL="http://subverion.ip.addr.ess/repos"
SVNUSER="svnadmin"
SVNPASS="password"
SVNM="/path/to/svnmerge.py"
LOGFILE="/var/log/svnsync.log"
LOGDATE=`date +"%d/%m/%Y %Z %H:%M:%S"`
PROGNAME=$(basename $0)
 
LOGFUN()
{
        echo "$LOGDATE - $1" >> $LOGFILE
}
 
initializeANSI()
{
  esc="E"
  blackf="${esc}[30m";   redf="${esc}[31m";    greenf="${esc}[32m"
  yellowf="${esc}[33m"   bluef="${esc}[34m";   purplef="${esc}[35m"
  cyanf="${esc}[36m";    whitef="${esc}[37m"
 
  blackb="${esc}[40m";   redb="${esc}[41m";    greenb="${esc}[42m"
  yellowb="${esc}[43m"   blueb="${esc}[44m";   purpleb="${esc}[45m"
  cyanb="${esc}[46m";    whiteb="${esc}[47m"
 
  boldon="${esc}[1m";    boldoff="${esc}[22m"
  italicson="${esc}[3m"; italicsoff="${esc}[23m"
  ulon="${esc}[4m";      uloff="${esc}[24m"
  invon="${esc}[7m";     invoff="${esc}[27m"
 
  reset="${esc}[0m"
}
 
initializeANSI
 
USAGE()
{
        echo -e "${redf}Usage: $PROGNAME -c [Options] -r [RepositoryName/<branch|trunk|tags>] [-u <Repository URL>]${reset}"
        echo -e "${yellowf}Example for Checkout : $PROGNAME -c co -r TestRepo/tags/buddyrelease/28072008/"
        echo -e "Example for Commit   : $PROGNAME -c ci -r TestRepo/tags/buddyrelease/28072008/"
        echo -e "Example for List     : $PROGNAME -c ls -r TestRepo/tags/buddyrelease/28072008/"
        echo -e "Example for Update   : $PROGNAME -c co -r TestRepo/tags/buddyrelease/28072008/${reset}"
        echo -e "${boldon}Options Available for -c:${reset}"
        echo -e "t${boldon}${italicson}ls - List Repository"
        echo -e "tco - Checkout Repository"
        echo -e "tci - Commit Repository"
        echo -e "tup - Update Repository"
        echo -e "tmg - Merge Repository${reset}"
        echo
}
 
if [ $# -le 1 ]
then
        USAGE
        LOGFUN "NO ARGUMENTS PASSED!!!"
        exit
fi
 
while getopts dc:r:u: OPTIONS
do
        case ${OPTIONS} in
           c) SVNARG=${OPTARG};;
           r) REPOARG=${OPTARG};;
           u) URLARG=${OPTARG};;
           *) USAGE
              exit 2;;
        esac
done
 
if [ "$REPOARG" == "" ] || [ "$SVNARG" == "" ]
then
        echo "-c and -r are Mandatory "
        echo -e "tExample for Checkout : $PROGNAME -c co -r TestRepo/tags/buddyrelease/28072008/"
        echo -e "tExample for Commit : $PROGNAME -c ci -r TestRepo/tags/buddyrelease/28072008/"
        echo -e "tExample for List : $PROGNAME -c ls -r TestRepo/tags/buddyrelease/28072008/"
        echo -e "tExample for Update : $PROGNAME -c co -r TestRepo/tags/buddyrelease/28072008/"
        exit 3
fi
 
if [ "$SVNARG" == "ls" ]
then
        $SVNEXE $SVNARG $SVNURL/$REPOARG/
        exit
fi
 
if [ "$SVNARG" == "co" ]
then
        cd $SVNREP
        if ! test -d $REPOARG
        then
                /bin/mkdir -p $REPOARG
        fi
 
        $SVNEXE $SVNARG $SVNURL/$REPOARG/ $SVNREP/$REPOARG --username $SVNUSER --password $SVNPASS
        cd $SVNREP/$REPOARG
        $SVNM init -f /tmp/initmessage.txt
 
        $SVNEXE ci -m "Need to Commit after initialising auto merging." $SVNREP/$REPOARG --username $SVNUSER --password $SVNPASS
 
        $SVNEXE up .
 
        exit
fi
 
if [ "$SVNARG" == "ci" ]
then
        $SVNEXE $SVNARG -m "" $SVNREP/$REPOARG --username $SVNUSER --password $SVNPASS
 
        exit
fi
 
if [ "$SVNARG" == "up" ]
then
        $SVNEXE $SVNARG $SVNREP/$REPOARG --username $SVNUSER --password $SVNPASS
 
        exit
fi
 
if [ "$SVNARG" == "mg" ]
then
        CONT=0
        CONT2=0
        if [ ! -d "$SVNREP/$REPOARG" ]
        then
                $SVNEXE co $SVNURL/$REPOARG/ $SVNREP/$REPOARG --username $SVNUSER --password $SVNPASS
 
                cd $SVNREP/$REPOARG
                $SVNM init -f /tmp/initmessage.txt
 
                $SVNEXE ci -m "Need to Commit after initialising auto merging."
            $SVNREP/$REPOARG --username $SVNUSER --password $SVNPASS
 
                $SVNEXE up .
 
        fi
        cd $SVNREP/$REPOARG
        echo "Updating Repo $SVNREP/$REPOARG...."
        $SVNEXE --username $SVNUSER --password $SVNPASS up .
 
        $SVNM --username $SVNUSER --password $SVNPASS merge -f /tmp/CommitMessage.txt
 
        CONT=`find . -name "*.merge-*.r*" |wc -l`
        CONT2=`find . -name "*.working"|wc -l`
        if [ $CONT -gt 0 ] && [ $CONT2 -gt 0 ]
        then
                $SVNEXE revert $SVNREP/$REPOARG
 
                LOGFUN "There is conflict in $SVNREP/$REPOARG. Please Resolve this manually with the help of developer(s)."
                /bin/rm -f /tmp/CommitMessage.txt
        else
                LOGFUN "No Conflicts found Merging $REPOARG"
                echo "Merging..."
                if [ -f /tmp/CommitMessage.txt ]
                then
                        echo "Commiting..."
                        $SVNEXE ci -F /tmp/CommitMessage.txt $SVNREP/$REPOARG --username $SVNUSER --password $SVNPASS
 
                        /bin/rm -f /tmp/CommitMessage.txt
                else
                        echo "Nothing to merge...."
                        LOGFUN "Nothing to merge for $REPOARG"
                fi
        fi
        exit
fi
}
SYNCSCRIPT -c mg -r project1/branch/developmentBranch1
SYNCSCRIPT -c mg -r project1/branch/developmentBranch2
SYNCSCRIPT -c mg -r project2/branch/developmentBranch1
