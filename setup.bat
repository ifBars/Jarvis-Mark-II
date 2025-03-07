@echo off
REM ================================================
REM Jarvis - Marvel Rivals AI Assistant Setup Script
REM Modularized version by ifBars (based on Patchi's Mark 2)
REM ================================================

echo ================================================
echo Jarvis - Marvel Rivals AI Assistant Setup
echo Modularized version by ifBars (based on Patchi's Mark 2)
echo ================================================

REM Check if Python is installed
echo Checking for Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed.
    echo Downloading Python installer...
    REM Change the URL below to update the Python version as needed.
    powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe' -OutFile '%CD%\python_installer.exe'"
    
    echo Installing Python silently...
    REM The following parameters install for all users and add Python to PATH.
    start /wait %CD%\python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    REM Check if installation succeeded
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python installation failed.
        pause
        exit /b 1
    ) else (
        echo Python installed successfully.
    )
) else (
    echo Python is installed.
)
echo.

REM Check for George TTS voice on machine
echo Checking for George TTS Voice...
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens\MSTTS_V110_enGB_GeorgeM" >nul 2>&1

if %errorlevel%==0 (
    echo George TTS Voice is installed and will be used by Jarvis.
) else (
    echo George TTS Voice is not installed, Jarvis will default to use the David voice.
)
echo.

REM Run registry copy command for TTS (requires admin privileges)
echo Running TTS registry copy command...
reg copy "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH_OneCore\Voices\Tokens" "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens" /s /f >nul 2>&1
if errorlevel 1 (
    echo WARNING: Failed to run registry command. You might need to run this script as administrator.
) else (
    echo Registry command executed successfully.
)
echo.

REM ====================================================
REM VOSK Model Download Section with Selection Menu
REM ====================================================
echo Please select which Vosk model you want to download:
echo 1^) vosk-model-small-en-us-0.15 (40MB)
echo 2^) vosk-model-small-en-us-0.22 (1.8GB)
echo 3^) vosk-model-en-us-0.22 (128MB)
echo 4^) vosk-model-large-en-us-0.22 (2.3GB)
echo 5^) Skip (I will download it manually)
choice /c:12345 /m "Enter your choice (1-5):"
set "MODEL_CHOICE=%errorlevel%"

if "%MODEL_CHOICE%"=="5" (
    echo Skipping Vosk model download. Make sure you download and extract the model manually.
    goto Dependencies
)

if "%MODEL_CHOICE%"=="1" (
    set "VOSK_MODEL_FOLDER=vosk-model-small-en-us-0.15"
    set "VOSK_MODEL_URL=https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    goto DownloadModel
)
if "%MODEL_CHOICE%"=="2" (
    set "VOSK_MODEL_FOLDER=vosk-model-small-en-us-0.22"
    set "VOSK_MODEL_URL=https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.22.zip"
    goto DownloadModel
)
if "%MODEL_CHOICE%"=="3" (
    set "VOSK_MODEL_FOLDER=vosk-model-en-us-0.22"
    set "VOSK_MODEL_URL=https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
    goto DownloadModel
)
if "%MODEL_CHOICE%"=="4" (
    set "VOSK_MODEL_FOLDER=vosk-model-large-en-us-0.22"
    set "VOSK_MODEL_URL=https://alphacephei.com/vosk/models/vosk-model-large-en-us-0.22.zip"
    goto DownloadModel
)

:DownloadModel
echo.
if not exist "%VOSK_MODEL_FOLDER%" (
    echo Downloading Vosk model "%VOSK_MODEL_FOLDER%" from %VOSK_MODEL_URL%...
    powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri '%VOSK_MODEL_URL%' -OutFile '%CD%\%VOSK_MODEL_FOLDER%.zip'"
    echo Extracting Vosk model...
    powershell -ExecutionPolicy Bypass -Command "Expand-Archive -Path '%CD%\%VOSK_MODEL_FOLDER%.zip' -DestinationPath '%CD%\%VOSK_MODEL_FOLDER%' -Force"
    del "%CD%\%VOSK_MODEL_FOLDER%.zip"
) else (
    echo Vosk model folder "%VOSK_MODEL_FOLDER%" already exists.
)
goto Dependencies

:Dependencies
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
echo Please open the config.ini file in this folder and update the following:
echo  - General: base_dir, api_key, voice_key
echo  - Vosk: model_path (set to the folder you downloaded, e.g. %VOSK_MODEL_FOLDER% or your manual folder)
echo  - OBS: host, port, password
echo  - Any other configuration values as required.
pause

echo ================================================
echo Setup is complete!
echo You can now run the application using:
echo   python main.py
echo ================================================
pause
