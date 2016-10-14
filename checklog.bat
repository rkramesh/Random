@echo off
cls
set t=%date%_%time%
set d=%t:~10,4%%t:~7,2%%t:~4,2%_%t:~15,2%%t:~18,2%%t:~21,2%
if "%1" == "" GOTO usage
if "%2" == "" GOTO specific
GOTO getcomment

:getcomment
pause
echo Fetching comments..
svn log -v %1 -r %2 > %d%-comments.txt
echo %ERRORLEVEL% > nul
IF %ERRORLEVEL% EQU 1 (Echo Invalid Url,PLease check the URL:%1 & goto err)
goto finish

:specific
echo example:
echo(
echo checklog.bat https://scm.com/branches/RELEASE2/ {2016-11-01}:{2016-12-04}
echo(                                               or
echo checklog.bat https://scm.com/branches/RELEASE2/  11724:11750
echo(
goto err



:usage
echo(
echo(
echo usage: checklog.bat url fromdate:todate 
echo                    or
echo usage: checklog.bat url fromrevision:torevision 
echo(
echo(
goto end

:err
svn info %1 | findstr . > NUL
IF %ERRORLEVEL% EQU 1 Echo Invalid Url,PLease check the URL:%1 
echo Error!,please run the script again
goto end

:finish
echo Script completed,please check comments.txt

:end
