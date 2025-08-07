@echo off
setlocal enabledelayedexpansion

set "sourceFile=realAssistant.py"
set "destinationFolder=E:\Git Projects\realAssistant\revisions"
set "counter=1"

:copyLoop
set "destinationFile=%destinationFolder%\realAssistant_!counter!.py"
if exist "%destinationFile%" (
    set /a counter+=1
    goto copyLoop
)

copy "%sourceFile%" "%destinationFile%"
echo File copied to %destinationFile%
