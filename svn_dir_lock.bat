@echo off
: *******************************************************
:  Get values from action (Set USER from the transaction)
: *******************************************************
set REPOS=%1
set TXN=%2
set SVNLOOK=C:\progra~1\Subversion\bin\svnlook.exe

: *******************************************************
:  If the file doesn't have the correct amount of
:  arguments then go to the end
: *******************************************************
if DEFINED TXN (
	echo.
) else (
	echo.
	echo This file must be run by the repository!
	echo.
	pause
	goto EndAll
)

: *******************************************************
:  Get the User who is committing
: *******************************************************
for /f "tokens=*" %%a in ('%SVNLOOK% author --transaction %TXN% %REPOS%') do set USER=%%a

: *******************************************************
:  Lock check - Verify that the files being committed
:  have been locked by the committing user.
: *******************************************************
:LockCheck
for /f "tokens=1,2" %%b in ('%SVNLOOK% changed --transaction %TXN% %REPOS%') do (
	if "%%b" == "U" (
		set pass=
		for /f "tokens=1,2*" %%f in ('%SVNLOOK% lock %REPOS% %%c') do (
			set pass=*

			: *******************************************************
			:  Go through the path's properties to get the owner of
			:  the lock.
			: *******************************************************
			if "Owner:" == "%%f" (
				if "%USER%" == "%%g" (
					echo.
				) else (
					goto Err
				)
			)
		)
		if DEFINED pass (
			echo.
		) else (
			goto Err
		)
	)
	: *******************************************************
	:  Make sure the files being deleted do not have locks.
	:  Otherwise you will have a zombie lock.
	: *******************************************************
	if "%%b" == "D" (
		for /f "tokens=1,2*" %%f in ('%SVNLOOK% lock %REPOS% %%c') do (
			goto Err
		)
	)
)
goto LogMessageCheck

: *******************************************************
:  If there's an error display error dialogue
: *******************************************************
:Err
echo. 1>&2
echo. 1>&2
echo Please follow these guidlines: 1>&2
echo  - Files being updated should be locked. 1>&2
echo  - Files being deleted should NOT be locked. 1>&2
echo  - Files being added should NOT be locked. 1>&2
echo. 1>&2
echo Please lock / unlock the files according to the guidlines above 1>&2
echo and then try committing again. 1>&2
echo. 1>&2
echo NOTE: DO NOT LOCK FILES THAT ARE BEING ADDED OR DELETED. 1>&2
echo. 1>&2
echo. 1>&2
exit 1


: *******************************************************
:  Make sure that the log message contains some text.
: *******************************************************
:LogMessageCheck
for /f "tokens=*" %%i in ('%SVNLOOK% log --transaction %TXN% %REPOS%') do set LOGMSG="%%i"
IF DEFINED LOGMSG goto EndAll

: *******************************************************
:  If there's an error display error dialogue
: *******************************************************
echo. 1>&2
echo. 1>&2
echo Please enter a descriptive log message and then try 1>&2
echo committing again. 1>&2
echo. 1>&2
echo. 1>&2
exit 1

:EndAll