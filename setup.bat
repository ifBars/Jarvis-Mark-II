@echo off
REM ================================================
REM Jarvis - Marvel Rivals AI Assistant Setup Script
REM Modularized version by ifBars (based on Patchi's Mark 1 & Mark 2)
REM ================================================

echo ================================================
echo Jarvis - Marvel Rivals AI Assistant Setup
echo ================================================

REM Check if Python is installed
echo Checking for Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed.
    echo Please download and install Python from https://www.python.org/downloads/ then rerun this script.
    pause
    exit /b 1
) else (
    echo Python is installed.
)
echo.

REM Check for the required TTS voice: Microsoft George (en-GB)
echo Checking for Microsoft English (United Kingdom) voice pack...
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens\MSTTS_V110_enGB_GeorgeM" >nul 2>&1
if errorlevel 1 (
    echo WARNING: The required voice pack (MSTTS_V110_enGB_GeorgeM) was not found.
    echo Please download and install the Microsoft English (United Kingdom) Voice Pack via your system's speech settings.
    pause
) else (
    echo Microsoft English (United Kingdom) voice pack found.
)
echo.

REM Run registry copy command for TTS (requires admin privileges)
echo Running TTS registry copy command...
reg copy "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH_OneCore\Voices\Tokens" "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens" /s /f
if errorlevel 1 (
    echo WARNING: Failed to run registry command. You might need to run this script as administrator.
) else (
    echo Registry command executed successfully.
)
echo.

REM Download Vosk model if not already present
set VOSK_MODEL_FOLDER=vosk-model-small-en-us-0.15
REM CHANGE THIS URL TO YOUR VOSK MODEL DOWNLOAD LINK
set VOSK_MODEL_URL=https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip

if not exist "%VOSK_MODEL_FOLDER%" (
    echo Downloading Vosk model from %VOSK_MODEL_URL%...
    powershell -Command "Invoke-WebRequest -Uri '%VOSK_MODEL_URL%' -OutFile '%CD%\vosk-model-small-en-us-0.15.zip'"
    echo Extracting Vosk model...
    powershell -Command "Expand-Archive -Path '%CD%\vosk-model-small-en-us-0.15.zip' -DestinationPath '%CD%\vosk-model-small-en-us-0.15' -Force"
    del "%CD%\vosk-model-small-en-us-0.15.zip"
) else (
    echo Vosk model folder already exists.
)
echo.

REM Install Python dependencies
echo Installing required Python packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
) else (
    echo Dependencies installed successfully.
)
echo.

REM Remind user to update config.ini file
echo.
echo Please open the config.ini file in this folder and update the following:
echo  - General: base_dir, api_key, voice_key
echo  - Vosk: model_path (set to "vosk-model-small-en-us-0.15")
echo  - OBS: host, port, password
echo  - Any other configuration values as required.
pause

echo ================================================
echo Setup is complete!
echo You can now run the application using:
echo   python main.py
echo ================================================
pause
