rem -----------------------------------
rem  Setup MongoDB Server for development
rem -----------------------------------
@echo off

set MONGOPATH="C:\Program Files\MongoDB\Server\3.0\bin\"
set PATH=%MONGOPATH%;%PATH%
         
rem start mongo.exe --host 127.0.0.1 --port 27017 cstat

start mongo.exe --host 127.0.0.1 --port 27017 -u statuser -p 12345 cstat