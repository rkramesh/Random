

echo off
set home=C:\Users\test\Desktop\RELEASE2-BRANCH
set log=C:\Users\test\Desktop\log
set t=%date%_%time%
set d=%t:~10,4%%t:~7,2%%t:~4,2%_%t:~15,2%%t:~18,2%%t:~21,2%
CD %home%
FOR /D %%A IN (*) DO (
    CD %%A
	echo Starting merge for branch %%A >> %log%/%d%-merge.txt 2>> %log%/%d%_mergeerror.txt
	:set trunk="https://scm./branches/Release_1/Source/%%A"	
	:set branch="https://scm./branches/RELEASE2/%%A"
	echo merging https://scm.v/branches/RELEASE2/%%A to https://scm.virtusa.com/affinioncmb/branches/Release_1/Source/%%A
	svn info "https:///RELEASE2/%%A" | findstr /B URL >> %log%/%d%-merge.txt 2>> %log%/%d%_mergeerror.txt
	svn info "https:///branches/Source/%%A"  | findstr /B URL >> %log%/%d%-merge.txt 2>> %log%/%d%_mergeerror.txt
	svn merge "https:///%%A"  https:/s/Release_1/Source/%%A --accept postpone >> %log%/%d%-merge.txt 2>> %log%/%d%_mergeerror.txt
         CD %home%
	)

	
	:function to get svn revision
	 REM svn info -rHEAD %cd%|find "URL"> %temp%\__svnrev.tmp
     REM set /p revision=< %temp%\__svnrev.tmp
     REM del %temp%\__svnrev.tmp
     REM set revision=%revision:~10%
     REM echo %revision%
