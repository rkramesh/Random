#!/bin/sh
#run this in crontab 


SYNCSCRIPT="/path/to/svnautomerge.sh"
 
$SYNCSCRIPT -c mg -r project1/branch/developmentBranch1
$SYNCSCRIPT -c mg -r project1/branch/developmentBranch2
$SYNCSCRIPT -c mg -r project2/branch/developmentBranch1
