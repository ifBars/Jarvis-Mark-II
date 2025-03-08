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

REM Change directory to the original folder from which the script was launched
cd /d "%ORIGINAL_PATH%"

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
    powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe' -OutFile '%ORIGINAL_PATH%\python_installer.exe'"
    
    echo Installing Python silently...
    start "" /wait "%ORIGINAL_PATH%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

    REM Manually update PATH in this session (adjust path if necessary)
    set "PYTHON_DIR=C:\Program Files\Python310\"
    set "PATH=%PYTHON_DIR%;%PYTHON_DIR%Scripts\;%PATH%"
    
    echo Python installation finished.
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
echo 2^) vosk-model-en-us-0.22 (1.8GB)
echo 3^) vosk-model-en-us-0.22-lgraph (128MB)
echo 4^) vosk-model-en-us-0.42-gigaspeech (2.3GB)
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
    set "VOSK_MODEL_FOLDER=vosk-model-en-us-0.22"
    set "VOSK_MODEL_URL=https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
    goto DownloadModel
)
if "%MODEL_CHOICE%"=="3" (
    set "VOSK_MODEL_FOLDER=vosk-model-en-us-0.22-lgraph"
    set "VOSK_MODEL_URL=https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip"
    goto DownloadModel
)
if "%MODEL_CHOICE%"=="4" (
    set "VOSK_MODEL_FOLDER=vosk-model-en-us-0.42-gigaspeech"
    set "VOSK_MODEL_URL=https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip"
    goto DownloadModel
)

:DownloadModel
echo.
if not exist "%ORIGINAL_PATH%\%VOSK_MODEL_FOLDER%" (
    echo Downloading Vosk model "%VOSK_MODEL_FOLDER%" from %VOSK_MODEL_URL%...
    powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri '%VOSK_MODEL_URL%' -OutFile '%ORIGINAL_PATH%\%VOSK_MODEL_FOLDER%.zip'"
    
    echo Extracting Vosk model...
    REM Extract the ZIP to a temporary folder
    powershell -ExecutionPolicy Bypass -Command "Expand-Archive -Path '%ORIGINAL_PATH%\%VOSK_MODEL_FOLDER%.zip' -DestinationPath '%ORIGINAL_PATH%\temp_model' -Force"
    
    REM Create the final destination folder
    if not exist "%ORIGINAL_PATH%\%VOSK_MODEL_FOLDER%" mkdir "%ORIGINAL_PATH%\%VOSK_MODEL_FOLDER%"
    
    REM Move the contents from the extracted inner folder to the destination folder
    powershell -ExecutionPolicy Bypass -Command "Move-Item -Path '%ORIGINAL_PATH%\temp_model\%VOSK_MODEL_FOLDER%\*' -Destination '%ORIGINAL_PATH%\%VOSK_MODEL_FOLDER%' -Force"
    
    REM Remove the temporary extraction folder
    rmdir /s /q "%ORIGINAL_PATH%\temp_model"
    
    del "%ORIGINAL_PATH%\%VOSK_MODEL_FOLDER%.zip"
) else (
    echo Vosk model folder "%VOSK_MODEL_FOLDER%" already exists.
)
goto Dependencies

:Dependencies
echo.
REM Install Python dependencies
echo Installing required Python packages...
start /wait "Installing pip dependencies" cmd /c "pip install --upgrade pip && pip install --upgrade setuptools wheel && pip install -r "%ORIGINAL_PATH%\requirements.txt" || pause"
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
) else (
    echo Dependencies installed successfully.
)
echo.

REM Update config.ini file if it exists
if exist "%ORIGINAL_PATH%\config.ini" (
    echo Updating config.ini...
    REM Update base_dir to the ORIGINAL_PATH
    powershell -Command "(Get-Content '%ORIGINAL_PATH%\config.ini') -replace '^base_dir\s*=.*$', 'base_dir = %ORIGINAL_PATH%' | Set-Content '%ORIGINAL_PATH%\config.ini'"
    
    REM Only update model_path if a Vosk model was downloaded (i.e. VOSK_MODEL_FOLDER is defined)
    if defined VOSK_MODEL_FOLDER (
        REM Build the full path to the model folder
        set "VOSK_MODEL=%VOSK_MODEL_FOLDER% "
        REM Using delayed expansion to substitute the variable inside the PowerShell command
        powershell -Command "(Get-Content '%ORIGINAL_PATH%\config.ini') -replace '^model_path\s*=.*$', 'model_path = !VOSK_MODEL!' | Set-Content '%ORIGINAL_PATH%\config.ini'"
    )
    echo config.ini updated successfully.
) else (
    echo config.ini not found in %ORIGINAL_PATH%.
)

REM Remind user to update config.ini file
echo Please open the config.ini file in this folder and update the following:
echo  - Google API Key: api_key
echo  - OBS: host, port, password
echo  - Any other configuration values as required.
pause

echo ================================================
echo Setup is complete!
echo You can now run the start.bat to start Jarvis.
echo ================================================
pause
