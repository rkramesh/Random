#!/bin/sh




## A simple shell script used to merge braches of Subversion.
versions=`svn log $2 --stop-on-copy | grep '^r[0-9]*' | awk '{print $1}'`
head_version=`echo $versions | awk '{print $1}' | grep -o '[0-9]*$'`
tail_version=`echo $versions | awk '{print $NF}' | grep -o '[0-9]*$'`
merge_cmd="svn merge -r $tail_version:$head_version $2 ."
 
echo 'Preparing environment:'
echo "Preparing environment done!\nChecking out $1"
svn co $1 .
echo "Checking out $1 done!\nMerging branches:$merge_cmd"
$merge_cmd
echo "Merging branches done:$merge_cmd"

### New svn script not to be updated with above function
check_errs()
{
  # Function. Parameter 1 is the return code
  # Para. 2 is text to display on failure.
  if [ "${1}" -ne "0" ]; then
      echo "ERROR # ${1} : ${2}"
      # as a bonus, make our script exit with the right error code.
      exit ${1}
  fi
}

check_uncommitted()
{
    UNCOMMITTED=`svn st | grep "^[UGMC\?\!AD]"`
    if [ -n "$UNCOMMITTED" ]; then
        echo "You have some uncommitted files:"
        echo "$UNCOMMITTED"
        echo -n "Are you sure you want to continue? (y or n): "
        read CONTINUE
        case $CONTINUE in
            [yY]) break ;;
            * ) exit 0 ;;
        esac
    fi
}

if [ $# != 1 ]; then
    echo "";
    echo "";
    echo "      Usage";
    echo "      svn-merge-to-trunk.sh BRANCH_NAME";
    echo "";
    echo "      BRANCH_NAME - The name of the branch to be merged e.g. style-tweaks";
    echo "";
    exit 1;
fi

svn info > /dev/null 2>&1
check_errs $? "Not a working directory!"

#get SVN URL
URL=`svn info | grep "^Repository Root:" | sed s/"Repository Root: "//g`

check_uncommitted

# switch to branch
echo "Switching to branch..."
svn switch ${URL}/branches/${1}
check_errs $? "Could not switch to branch, does it exist?"

# get first revision of branch
echo "Getting first revision of branch..."
FIRST_REV=`svn log --stop-on-copy | grep "^r[0-9]" | tail -1 | cut -d" " -f1`

# switch back to trunk
echo "Switching to trunk..."
svn switch ${URL}/trunk
check_errs $? "Could not switch to trunk for some strange reason"

# do a dry run of the merge
echo "This is what's gonna happen:"
svn merge -${FIRST_REV}:HEAD ${URL}/branches/${1} --dry-run
check_errs $? "Something weird happened when we tried to do a dry run of the merge"
echo -n "Merge now? (y or n): "
read yn
case $yn in
    [yY]) break ;;
    * ) exit 1 ;;
esac

# merge
echo "Merging..."
svn merge -${FIRST_REV}:HEAD ${URL}/branches/${1}
check_errs $? "Something weird happened when we tried to merge"
echo "Done!"

echo -n "Right, now test like a mofo and commit when you're happy!"
echo -n ""

#shall we commit?
#echo -n "Would you like to commit the merge now? (y or n): "
#read yn
#case $yn in
#    [yY]) break ;;
#    * ) exit 0 ;;
#esac

#commit
#svn ci -m "merged branch ${1}"
#check_errs $? "Unable to commit :("

#echo "Done!"
exit 0
