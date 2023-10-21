@echo off

REM Specify Python installation directory
set PYTHON_INSTALL_DIR="C:\Path\To\Your\Python"

REM Install Python
msiexec /i https://www.python.org/ftp/python/3.x.x/python-3.x.x-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 TargetDir=%PYTHON_INSTALL_DIR%
powershell -Command "& { Invoke-WebRequest %DOWNLOAD_URL% -OutFile %DOWNLOAD_DEST% -ProgressPreference SilentlyContinue }"

REM Add Python and pip to the system PATH
setx PATH "%PATH%;%PYTHON_INSTALL_DIR%;%PYTHON_INSTALL_DIR%\Scripts" /M

REM Install required Python packages using pip
pip install selenium

REM Specify ChromeDriver version
set CHROMEDRIVER_VERSION="91.0.4472.101"

REM Download ChromeDriver
curl -O "https://chromedriver.storage.googleapis.com/%CHROMEDRIVER_VERSION%/chromedriver_win64.zip"
powershell -Command "& { Invoke-WebRequest %DOWNLOAD_URL% -OutFile %DOWNLOAD_DEST% -ProgressPreference SilentlyContinue }"

REM Unzip the downloaded file
tar -xvf chromedriver_win32.zip

REM Move the ChromeDriver executable to the Python Scripts directory
move chromedriver.exe %PYTHON_INSTALL_DIR%\Scripts

REM Clean up downloaded files
del chromedriver_win32.zip

REM Create a virtual environment and install additional dependencies if needed
REM Uncomment the lines below and add your additional dependencies

REM python -m venv %PYTHON_INSTALL_DIR%\venv
REM %PYTHON_INSTALL_DIR%\Scripts\activate
REM pip install <additional_dependency_1>
REM pip install <additional_dependency_2>

REM Optionally, deactivate the virtual environment if created
REM deactivate
echo Download and install completed.
