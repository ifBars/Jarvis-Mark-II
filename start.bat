@echo off
setlocal EnableDelayedExpansion

REM ===============================================================
REM Capture Original Directory and Request Elevation if Not Admin
REM ===============================================================
if "%~1"=="" (
    set "ORIGINAL_PATH=%CD%"
) else (
    set "ORIGINAL_PATH=%~1"
)

REM Check for admin privileges using NET SESSION (only works when elevated)
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -ArgumentList '%ORIGINAL_PATH%' -Verb runAs"
    exit /b
)

:LOOP
cls
REM Change directory to the original folder from which the script was launched
cd /d "%~dp0"

REM ---------------------------------------------------------------
REM Load localized welcome message from locales\setup_messages.json
REM ---------------------------------------------------------------
REM Determine language from config.ini (default to 'en')
set "LANGUAGE=en"
for /f "tokens=2 delims==" %%a in ('findstr /b "language" "%~dp0config.ini"') do set "LANGUAGE=%%a"

REM Store the full path of the JSON file in a variable
set "SETUP_MSG_FILE=%~dp0locales\setup_messages.json"

REM Use PowerShell to extract the welcome message.
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw \"%SETUP_MSG_FILE%\" | ConvertFrom-Json).%LANGUAGE%.welcome)"`) do set "MSG_WELCOME=%%A"

REM ===============================================================
REM Jarvis - Marvel Rivals AI Assistant
REM ===============================================================
echo ================================================
echo %MSG_WELCOME%
echo ================================================

python main.py
pause
goto :LOOP