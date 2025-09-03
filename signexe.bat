@echo off
setlocal


REM Set variables
set CERT_NAME=rptscert.pem
set KEY_NAME=rptskey.pem
set CSR_NAME=rptsrequest.csr
set EXE_NAME=realAssistant.exe
set SIGNED_EXE_NAME=realAssistant-signed.exe
set APP_NAME="realAssistant"
set APP_URL=http://local.lan
set TIMESTAMP_URL=http://timestamp.digicert.com

REM Generate a private key
openssl genpkey -algorithm RSA -out %KEY_NAME% -aes256
if errorlevel 1 goto :error

REM Create a certificate signing request (CSR)
openssl req -new -key %KEY_NAME% -out %CSR_NAME%
if errorlevel 1 goto :error

REM Generate a self-signed certificate
openssl x509 -req -days 365 -in %CSR_NAME% -signkey %KEY_NAME% -out %CERT_NAME%
if errorlevel 1 goto :error
REM Sign the executable
osslsigncode sign -certs %CERT_NAME% -key %KEY_NAME% -n %APP_NAME% -i %APP_URL% -t %TIMESTAMP_URL% -in %EXE_NAME% -out %SIGNED_EXE_NAME%
if errorlevel 1 goto :error

echo Signing completed successfully.
goto :end

:error
echo An error occurred during the process.
goto :end

:end
endlocal
pause
