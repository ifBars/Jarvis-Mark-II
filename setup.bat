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
    powershell -Command "Start-Process '%~f0' -ArgumentList '%ORIGINAL_PATH%' -Verb runAs"
    exit /b
)

REM Change directory to the original folder from which the script was launched
cd /d "%~dp0"
set "ORIGINAL_PATH=%~dp0"

REM ===============================================================
REM Remove trailing slash from ORIGINAL_PATH unless it’s a drive root (e.g. C:\)
REM ===============================================================
if NOT "%ORIGINAL_PATH:~-1%"==":" (
   if "%ORIGINAL_PATH:~-1%"=="\" (
       set "ORIGINAL_PATH=%ORIGINAL_PATH:~0,-1%"
   )
)

REM ===============================================================
REM Prompt user to select a language and update config.ini accordingly
REM ===============================================================
:SelectLanguage
echo Please select your language:
echo   1) English (en)
echo   2) Spanish (es)
echo   3) Portuguese (pt)
echo   4) French (fr)
set /p langChoice="Enter your choice (1-4): "

if "%langChoice%"=="1" (
    set "LANGUAGE=en"
) else if "%langChoice%"=="2" (
    set "LANGUAGE=es"
) else if "%langChoice%"=="3" (
    set "LANGUAGE=pt"
) else if "%langChoice%"=="4" (
    set "LANGUAGE=fr"
) else (
    echo Invalid choice. Please try again.
    goto SelectLanguage
)

REM Update (or create) config.ini with the chosen language
if exist "%~dp0config.ini" (
    powershell -Command "(Get-Content '%~dp0config.ini') -replace '^language\s*=.*$', 'language = %LANGUAGE%' | Set-Content '%~dp0config.ini'"
) else (
    echo language=%LANGUAGE% > "%~dp0config.ini"
)

REM ===============================================================
REM Load localized messages from JSON file located at locales\setup_messages.json
set "SETUP_MSG_FILE=%~dp0locales\setup_messages.json"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.language_loading)"`) do set "MSG_LANGUAGE_LOADING=%%A"
echo %MSG_LANGUAGE_LOADING%
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.welcome)"`) do set "MSG_WELCOME=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.admin_request)"`) do set "MSG_ADMIN_REQUEST=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.python_installed)"`) do set "MSG_PYTHON_INSTALLED=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.python_not_installed)"`) do set "MSG_PYTHON_NOT_INSTALLED=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.checking_python)"`) do set "MSG_CHECKING_PYTHON=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.downloading_python)"`) do set "MSG_DOWNLOADING_PYTHON=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.installing_python)"`) do set "MSG_INSTALLING_PYTHON=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.python_finished)"`) do set "MSG_PYTHON_FINISHED=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.checking_tts)"`) do set "MSG_CHECKING_TTS=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.tts_installed)"`) do set "MSG_TTS_INSTALLED=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.tts_not_installed)"`) do set "MSG_TTS_NOT_INSTALLED=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.running_registry)"`) do set "MSG_RUNNING_REGISTRY=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.registry_warning)"`) do set "MSG_REGISTRY_WARNING=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.registry_success)"`) do set "MSG_REGISTRY_SUCCESS=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.select_speech_engine)"`) do set "MSG_SELECT_SPEECH_ENGINE=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.vosk_choice)"`) do set "MSG_VOSK_CHOICE=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.speech_recognition_choice)"`) do set "MSG_SPEECH_RECOGNITION_CHOICE=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.enter_choice)"`) do set "MSG_ENTER_CHOICE=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.vosk_selected)"`) do set "MSG_VOSK_SELECTED=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.select_vosk_model)"`) do set "MSG_SELECT_VOSK_MODEL=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.vosk_model_option1)"`) do set "MSG_VOSK_MODEL_OPTION1=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.vosk_model_option2)"`) do set "MSG_VOSK_MODEL_OPTION2=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.vosk_model_option3)"`) do set "MSG_VOSK_MODEL_OPTION3=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.vosk_model_option4)"`) do set "MSG_VOSK_MODEL_OPTION4=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.vosk_model_option5)"`) do set "MSG_VOSK_MODEL_OPTION5=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.skipping_vosk)"`) do set "MSG_SKIPPING_VOSK=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.downloading_vosk)"`) do set "MSG_DOWNLOADING_VOSK=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.extracting_vosk)"`) do set "MSG_EXTRACTING_VOSK=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.vosk_exists)"`) do set "MSG_VOSK_EXISTS=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.installing_dependencies)"`) do set "MSG_INSTALLING_DEPENDENCIES=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.dependencies_success)"`) do set "MSG_DEPENDENCIES_SUCCESS=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.config_updating)"`) do set "MSG_CONFIG_UPDATING=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.config_updated)"`) do set "MSG_CONFIG_UPDATED=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.config_not_found)"`) do set "MSG_CONFIG_NOT_FOUND=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.update_config_reminder)"`) do set "MSG_UPDATE_CONFIG_REMINDER=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.setup_complete)"`) do set "MSG_SETUP_COMPLETE=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.git_not_installed)"`) do set "MSG_GIT_NOT_INSTALLED=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.git_installing)"`) do set "MSG_GIT_INSTALLING=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.git_installed)"`) do set "MSG_GIT_INSTALLED=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.git_already_installed)"`) do set "MSG_GIT_ALREADY_INSTALLED=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.initializing_git)"`) do set "MSG_INITIALIZING_GIT=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.git_error1)"`) do set "MSG_GIT_ERROR1=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.git_error2)"`) do set "MSG_GIT_ERROR2=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.git_error3)"`) do set "MSG_GIT_ERROR3=%%A"
for /f "usebackq delims=" %%A in (`powershell -NoProfile -Command "((Get-Content -Raw '%SETUP_MSG_FILE%' | ConvertFrom-Json).%LANGUAGE%.git_error4)"`) do set "MSG_GIT_ERROR4=%%A"

REM ================================================
REM Jarvis - Marvel Rivals AI Assistant Setup Script
REM Modularized by ifBars (based on Patchi's Mark 2)
REM ================================================
cls
echo ================================================
echo %MSG_WELCOME%
echo ================================================

REM Check if Python is installed
echo %MSG_CHECKING_PYTHON%
python --version >nul 2>&1
if errorlevel 1 (
    echo %MSG_PYTHON_NOT_INSTALLED%
    echo %MSG_DOWNLOADING_PYTHON%
    powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe' -OutFile '%ORIGINAL_PATH%\python_installer.exe'"
    
    echo %MSG_INSTALLING_PYTHON%
    start "" /wait "%ORIGINAL_PATH%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

    REM Manually update PATH in this session (adjust path if necessary)
    set "PYTHON_DIR=C:\Program Files\Python310\"
    set "PATH=%PYTHON_DIR%;%PYTHON_DIR%Scripts\;%PATH%"
    
    echo %MSG_PYTHON_FINISHED%
) else (
    echo %MSG_PYTHON_INSTALLED%
)
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo %MSG_GIT_NOT_INSTALLED%
    echo %MSG_GIT_INSTALLING%
    
    powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.1/Git-2.42.0-64-bit.exe' -OutFile '%ORIGINAL_PATH%\git_installer.exe'"
    start /wait "" "%ORIGINAL_PATH%\git_installer.exe" /VERYSILENT /NORESTART
    echo %MSG_GIT_INSTALLED%

    set "GIT_PATH=C:\Program Files\Git\cmd"
    set "PATH=%GIT_PATH%;%PATH%"
) else (
    echo %MSG_GIT_ALREADY_INSTALLED%
)

REM Check if the current folder is a Git repository
if not exist "%ORIGINAL_PATH%\.git" (
    echo %MSG_INITIALIZING_GIT%
    
    REM Initialize a new Git repository
    git init
    if errorlevel 1 (
        echo %MSG_GIT_ERROR1%
        pause
        exit /b 1
    )
    
    REM Add the remote origin (adjust the URL as needed)
    git remote add origin https://github.com/PatchiPup/Jarvis-Mark-II.git
    if errorlevel 1 (
        echo %MSG_GIT_ERROR2%
        pause
        exit /b 1
    )

    git remote get-url upstream >nul 2>&1
    if %errorlevel%==1 (
        git remote add upstream https://github.com/PatchiPup/Jarvis-Mark-II.git
        git fetch upstream
    )
    
    REM Fetch the repository history from the remote
    git fetch origin
    if errorlevel 1 (
        echo %MSG_GIT_ERROR3%
        pause
        exit /b 1
    )
    
    REM Reset the local repository to the latest state from 'main'
    git reset --hard origin/main
    if errorlevel 1 (
        echo %MSG_GIT_ERROR4%
        pause
        exit /b 1
    )
) else (
    git remote get-url upstream >nul 2>&1
    if %errorlevel%==1 (
        git remote add upstream https://github.com/PatchiPup/Jarvis-Mark-II.git
        git fetch upstream
    )
)

REM Check for George TTS voice on machine
echo %MSG_CHECKING_TTS%
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens\MSTTS_V110_enGB_GeorgeM" >nul 2>&1
if %errorlevel%==0 (
    echo %MSG_TTS_INSTALLED%
) else (
    echo %MSG_TTS_NOT_INSTALLED%
)
echo.

REM Run registry copy command for TTS (requires admin privileges)
echo %MSG_RUNNING_REGISTRY%
reg copy "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH_OneCore\Voices\Tokens" "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens" /s /f >nul 2>&1
if errorlevel 1 (
    echo %MSG_REGISTRY_WARNING%
) else (
    echo %MSG_REGISTRY_SUCCESS%
)
echo.

REM ====================================================
REM Ask User to Select Speech Engine (vosk or speech_recognition)
REM ====================================================
echo %MSG_SELECT_SPEECH_ENGINE%
echo %MSG_VOSK_CHOICE%
echo %MSG_SPEECH_RECOGNITION_CHOICE%
choice /c:12 /m "%MSG_ENTER_CHOICE%"
set "ENGINE_CHOICE=%errorlevel%"

if "%ENGINE_CHOICE%"=="1" (
    set "SPEECH_ENGINE=vosk"
    goto VoskModelSelection
) else (
    set "SPEECH_ENGINE=speech_recognition"
    goto Dependencies
)

:VoskModelSelection
echo.
echo %MSG_VOSK_SELECTED%
echo.
REM ====================================================
REM VOSK Model Download Section with Selection Menu
REM ====================================================
echo %MSG_SELECT_VOSK_MODEL%
echo %MSG_VOSK_MODEL_OPTION1%
echo %MSG_VOSK_MODEL_OPTION2%
echo %MSG_VOSK_MODEL_OPTION3%
echo %MSG_VOSK_MODEL_OPTION4%
echo %MSG_VOSK_MODEL_OPTION5%
choice /c:12345 /m "%MSG_ENTER_CHOICE%"
set "MODEL_CHOICE=%errorlevel%"

if "%MODEL_CHOICE%"=="5" (
    echo %MSG_SKIPPING_VOSK%
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
    echo %MSG_DOWNLOADING_VOSK%
    powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri '%VOSK_MODEL_URL%' -OutFile '%ORIGINAL_PATH%\%VOSK_MODEL_FOLDER%.zip'"
    
    echo %MSG_EXTRACTING_VOSK%
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
    echo %MSG_VOSK_EXISTS%
)
goto Dependencies

:Dependencies
echo.
REM Install Python dependencies
echo %MSG_INSTALLING_DEPENDENCIES%
start /wait "Installing pip dependencies" cmd /c "python -m pip install --upgrade pip && pip install --upgrade setuptools wheel && pip install -r "%ORIGINAL_PATH%\requirements.txt" || pause"
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
) else (
    echo %MSG_DEPENDENCIES_SUCCESS%
)
echo.

REM Update config.ini file if it exists
if exist "%ORIGINAL_PATH%\config.ini" (
    echo %MSG_CONFIG_UPDATING%
    REM Update base_dir to the ORIGINAL_PATH (no trailing slash now)
    powershell -Command "(Get-Content '%ORIGINAL_PATH%\config.ini') -replace '^base_dir\s*=.*$', 'base_dir = %ORIGINAL_PATH%' | Set-Content '%ORIGINAL_PATH%\config.ini'"
    
    REM Update speech engine setting
    powershell -Command "(Get-Content '%ORIGINAL_PATH%\config.ini') -replace '^engine\s*=.*$', 'engine = %SPEECH_ENGINE%' | Set-Content '%ORIGINAL_PATH%\config.ini'"
    
    REM Only update model_path if a VOSK model was downloaded (i.e. VOSK_MODEL_FOLDER is defined)
    if defined VOSK_MODEL_FOLDER (
        set "VOSK_MODEL=%VOSK_MODEL_FOLDER%"
        powershell -Command "(Get-Content '%ORIGINAL_PATH%\config.ini') -replace '^model_path\s*=.*$', 'model_path = !VOSK_MODEL!' | Set-Content '%ORIGINAL_PATH%\config.ini'"
    )
    echo %MSG_CONFIG_UPDATED%
) else (
    echo %MSG_CONFIG_NOT_FOUND%
)

REM Remind user to update config.ini file
echo %MSG_UPDATE_CONFIG_REMINDER%
pause

echo ================================================
echo %MSG_SETUP_COMPLETE%
echo ================================================
pause
