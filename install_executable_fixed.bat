@echo off
REM Installation script for FindingExcellence

echo ===== FindingExcellence Quick Installer =====
echo.
echo This will create an executable for FindingExcellence.
echo You only need to run this once.
echo.

REM Check for Python using py launcher first (most reliable on Windows)
echo Checking for Python installation...
py --version > NUL 2>&1

if %ERRORLEVEL% equ 0 (
    echo Found Python using py launcher
    set PYTHON_CMD=py
    goto :found_python
)

REM Fallback to direct python command
where python > NUL 2>&1
if %ERRORLEVEL% equ 0 (
    echo Found Python in PATH
    set PYTHON_CMD=python
    goto :found_python
)

REM Try to find Python in common installation locations
echo Python not found in PATH. Looking for Python in Program Files...

if exist "C:\Program Files\Python*" (
    for /d %%i in ("C:\Program Files\Python*") do (
        if exist "%%i\python.exe" (
            set PYTHON_CMD="%%i\python.exe"
            goto :found_python
        )
    )
)

if exist "C:\Program Files (x86)\Python*" (
    for /d %%i in ("C:\Program Files (x86)\Python*") do (
        if exist "%%i\python.exe" (
            set PYTHON_CMD="%%i\python.exe"
            goto :found_python
        )
    )
)

REM Check in user AppData directories - common for user-based installations
if exist "%LOCALAPPDATA%\Programs\Python\Python*" (
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        if exist "%%i\python.exe" (
            set PYTHON_CMD="%%i\python.exe"
            goto :found_python
        )
    )
)

echo Python installation not found automatically.
echo.
echo Please enter the full path to your Python executable (e.g., C:\Path\To\Python\python.exe):
echo Or just type 'py' if you have the Python launcher installed:
set /p PYTHON_CMD="> "

if "%PYTHON_CMD%"=="py" (
    py --version > NUL 2>&1
    if %ERRORLEVEL% neq 0 (
        echo Python launcher not working. Please try again.
        pause
        exit /b 1
    )
    goto :found_python
)

if not exist "%PYTHON_CMD%" (
    echo The specified file does not exist. Please try again with a valid path.
    pause
    exit /b 1
)

:found_python
echo Using Python: %PYTHON_CMD%

REM Check Python version
%PYTHON_CMD% -c "import sys; print('Python', sys.version_info.major, '.', sys.version_info.minor, sep=''); exit(0 if sys.version_info.major >= 3 and sys.version_info.minor >= 6 else 1)" > NUL 2>&1
if %ERRORLEVEL% neq 0 (
    echo This application requires Python 3.6 or higher.
    echo Please install a compatible Python version.
    pause
    exit /b 1
)

REM Install required packages
echo Installing required packages...
%PYTHON_CMD% -m pip install -r build_resources\requirements.txt

if %ERRORLEVEL% neq 0 (
    echo Failed to install required packages.
    echo Please make sure you have internet access and pip is working correctly.
    pause
    exit /b 1
)

REM Build the executable directly (instead of calling build.bat)
echo.
echo Building the executable...

REM Set directories
set PROJECT_DIR=%~dp0
set BUILD_DIR=%PROJECT_DIR%build_resources
set OUTPUT_DIR=%BUILD_DIR%\output
set ICON_DIR=%BUILD_DIR%\icons
set DIST_DIR=%PROJECT_DIR%dist

REM Create necessary directories
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
if not exist "%DIST_DIR%" mkdir "%DIST_DIR%"

REM Check for icon file
if exist "%ICON_DIR%\app_icon.ico" (
    echo Building with custom FindingExcellence logo...
    %PYTHON_CMD% -m PyInstaller --onefile --windowed --icon="%ICON_DIR%\app_icon.ico" --distpath="%OUTPUT_DIR%" --workpath="%BUILD_DIR%\build" --name=FindingExcellence main.py
) else (
    echo Building without custom icon...
    %PYTHON_CMD% -m PyInstaller --onefile --windowed --distpath="%OUTPUT_DIR%" --workpath="%BUILD_DIR%\build" --name=FindingExcellence main.py
)

if %ERRORLEVEL% neq 0 (
    echo Build process failed. Please check the error messages above.
    pause
    exit /b 1
)

REM Copy to dist folder
if exist "%OUTPUT_DIR%\FindingExcellence.exe" (
    copy "%OUTPUT_DIR%\FindingExcellence.exe" "%DIST_DIR%\"
    echo.
    echo ✅ Installation complete!
    echo The executable is now available in the dist folder.
    echo.
    echo ⭐ Your FindingExcellence.exe now has your custom logo!
    echo Location: %DIST_DIR%\FindingExcellence.exe
) else (
    echo.
    echo ❌ Build failed! Executable not found.
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
pause
exit /b 0
