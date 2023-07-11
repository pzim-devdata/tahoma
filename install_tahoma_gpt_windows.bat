@echo off

Set-ExecutionPolicy RemoteSigned

REM Function to download a file from URL
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%1', '%2')"

REM Ask if the user wants to install venv
set /p install_venv="Do you want to install venv? (Yes/No): "

REM Check user's response
if /I "%install_venv%"=="Yes" (
  python -m pip install virtualenv
) else (
  echo "Venv was not installed."
)

REM Ask for the installation directory path
echo.
set /p install_dir="Enter the installation directory path (Or press Enter to install in C:\tahoma-gpt): "
if "%install_dir%"=="" set "install_dir=C:\tahoma-gpt"

REM Create the installation directory and navigate into it
mkdir "%install_dir%"
cd /d "%install_dir%"

REM Download files from GitHub
call :download_file "https://github.com/pzim-devdata/tahoma/raw/main/requirements_tahoma-gpt.txt" "requirements_tahoma-gpt.txt"
call :download_file "https://github.com/pzim-devdata/tahoma/raw/main/tahoma-gpt.py" "tahoma-gpt.py"
call :download_file "https://github.com/pzim-devdata/tahoma/raw/main/tahoma_chatgpt.bat" "tahoma_chatgpt.bat"
call :download_file "https://raw.githubusercontent.com/pzim-devdata/tahoma/main/tahoma-gpt.png" "tahoma-chatgpt.png"

REM Install venv
python -m venv env

REM Activate the virtual environment
call env\Scripts\activate.bat

REM Ask if the user wants to install Tahoma
echo.
echo "Be careful to ensure that there are no multiple versions of Tahoma already installed on your computer."
set /p install_tahoma="Do you want to install Tahoma? (Yes/No): "

REM Check user's response
if /I "%install_tahoma%"=="Yes" (
  REM Install Tahoma
  python -m pip install -U tahoma

  REM Configure Tahoma
  echo.
  tahoma -c

  REM Get the list of devices
  echo.
  tahoma -g

  timeout /t 6
)

REM Install dependencies
python -m pip install -r requirements_tahoma-gpt.txt

REM Ask for the OpenAI API key
echo.
echo "To get the OpenAI API key, please visit the OpenAI website: https://platform.openai.com/apps"
set /p openai_api_key="Enter the OpenAI API key: "

REM Modify the tahoma-gpt.py file with the API key
powershell -Command "(gc tahoma-gpt.py) -replace 'openai.api_key =.*', 'openai.api_key = ''%openai_api_key%''' | Out-File -encoding ASCII tahoma-gpt.py"

REM Ask if the user wants to create a desktop shortcut for Tahoma-GPT
set /p response="Do you want to create a desktop shortcut for Tahoma-GPT? (Yes/No): "
set response=%response:~0,1%

if /I "%response%"=="Y" (
  REM Get the desktop directory path
  for /f "skip=2 tokens=2,*" %%A in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop') do set "desktop_dir=%%B"

  if defined desktop_dir (
    echo [Desktop Entry]> "%desktop_dir%\tahoma-gpt.desktop"
    echo Name=Tahoma-GPT>> "%desktop_dir%\tahoma-gpt.desktop"
    echo Comment=Shortcut to run Tahoma-GPT>> "%desktop_dir%\tahoma-gpt.desktop"
    echo Icon="%CD%\tahoma-chatgpt.png">> "%desktop_dir%\tahoma-gpt.desktop"
    echo Exec="%CD%\tahoma_chatgpt.bat">> "%desktop_dir%\tahoma-gpt.desktop"

    echo The desktop shortcut for Tahoma-GPT has been created successfully.
  ) else (
    echo Could not find the Desktop directory, unable to install the shortcut.
  )
)

REM Execute the tahoma-gpt.py script
python tahoma-gpt.py

REM Deactivate the virtual environment
call env\Scripts\deactivate.bat

exit /b

REM Function to download a file from URL
:download_file
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%~1', '%~2')"
exit /b
