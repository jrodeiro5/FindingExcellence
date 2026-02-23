@echo off
REM FindingExcellence - Distribution build script
REM Creates isolated build venv, installs dependencies, runs PyInstaller

setlocal enabledelayedexpansion

REM Get script directory (project root)
set "SCRIPT_DIR=%~dp0"
set "BUILD_VENV=%SCRIPT_DIR%build_venv"

REM Create build venv if it doesn't exist
if not exist "!BUILD_VENV!\Scripts\python.exe" (
    echo Creating build virtual environment...
    python -m venv "!BUILD_VENV!"
    if errorlevel 1 (
        echo.
        echo ERROR: Python not found in PATH
        echo Please install Python 3.8+ and add it to your PATH
        echo Download from: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    echo Build virtual environment created.
)

REM Activate build venv
call "!BUILD_VENV!\Scripts\activate.bat"
if errorlevel 1 (
    echo ERROR: Could not activate build virtual environment
    pause
    exit /b 1
)

REM Install/update dependencies
echo Installing build dependencies...
python -m pip install -q --upgrade pip
python -m pip install -q -r build_resources\requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Clean previous build
if exist "build" rmdir /s /q "build" 2>nul
if exist "dist" rmdir /s /q "dist" 2>nul
mkdir "dist"

REM Run PyInstaller from project root
echo.
echo Running PyInstaller...
echo.
python -m PyInstaller build_resources\FindingExcellence.spec ^
    --distpath=dist ^
    --workpath=build ^
    --clean ^
    --log-level=INFO

if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    echo Check output above for details
    pause
    exit /b 1
)

echo.
echo.
echo ============================================================
echo Build complete! Executable created at:
echo   %SCRIPT_DIR%dist\FindingExcellence\
echo ============================================================
echo.
pause

REM Deactivate venv
deactivate

endlocal
