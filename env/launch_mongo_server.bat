rem -----------------------------------
rem  Setup MongoDB Server for development
rem -----------------------------------
@echo off

set MONGOPATH="C:\Program Files\MongoDB\Server\3.0\bin\"
set PATH=%MONGOPATH%;%PATH%
         
start mongod.exe -f ./mongodb.conf