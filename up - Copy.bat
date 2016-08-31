rem CD C:\Program Files\TortoiseSVN\bin\
rem START TortoiseProc.exe /command:update /path:"C:\www\MyRepo\" /closeonend:0

rem CD C:\Users\radhakrishnanr\Desktop\deployment


CD C:\Users\radhakrishnanr\Desktop\deployment

@echo off

FOR /D %%A IN (*) DO START TortoiseProc.exe /command:update /path:%%A /closeonend:1
