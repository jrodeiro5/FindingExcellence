@echo off
REM FindingExcellence - Developer launcher
REM Creates venv if needed, installs dependencies, runs the app

setlocal enabledelayedexpansion

REM Get script directory (project root)
set "SCRIPT_DIR=%~dp0"
set "VENV=%SCRIPT_DIR%venv"

REM Create venv if it doesn't exist
if not exist "!VENV!\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv "!VENV!"
    if errorlevel 1 (
        echo.
        echo ERROR: Python not found in PATH
        echo Please install Python 3.8+ and add it to your PATH
        echo Download from: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    echo Virtual environment created.
)

REM Activate venv
call "!VENV!\Scripts\activate.bat"
if errorlevel 1 (
    echo ERROR: Could not activate virtual environment
    pause
    exit /b 1
)

REM Install/update dependencies
echo Installing dependencies...
python -m pip install -q --upgrade pip
python -m pip install -q -r build_resources\requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Run the app
echo.
echo Starting FindingExcellence...
echo.
python main.py

REM If app crashed, show error
if errorlevel 1 (
    echo.
    echo ERROR: Application exited with error
    echo Check finding_excellence.log for details
    pause
)

endlocal
