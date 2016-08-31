rem add TortoiseProc.exe to the path
rem START TortoiseProc.exe /command:update /path:"C:\www\MyRepo\" /closeonend:0

rem CD C:\Users\radhakrishnanr\Desktop\deployment

rem navigate to the parent directory containing subfolders
CD C:\Users\radhakrishnanr\Desktop\deployment

@echo off

FOR /D %%A IN (*) DO START TortoiseProc.exe /command:update /path:%%A /closeonend:1
