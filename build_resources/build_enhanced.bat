@echo off
REM Enhanced build script for FindingExcellence executable with security improvements

echo ===== FindingExcellence Enhanced Build Script =====
echo.

REM Set directories
set BUILD_DIR=%~dp0
set PROJECT_DIR=%BUILD_DIR%\..
set OUTPUT_DIR=%BUILD_DIR%\output
set ICON_DIR=%BUILD_DIR%\icons
set DIST_DIR=%PROJECT_DIR%\dist

REM Create necessary directories if they don't exist
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
if not exist "%DIST_DIR%" mkdir "%DIST_DIR%"

echo Checking for Python...
REM Get the Python path from the parent script
if "%PYTHON_PATH%"=="" (
    echo PYTHON_PATH variable not set. Please run this script through install_executable.bat
    exit /b 1
)

if not exist "%PYTHON_PATH%" (
    echo Python not found at: %PYTHON_PATH%
    exit /b 1
)

echo Checking Python version (requires 3.8+)...
"%PYTHON_PATH%" -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'); exit(0 if (sys.version_info.major == 3 and sys.version_info.minor >= 8) else 1)"
if %ERRORLEVEL% neq 0 (
    echo This application requires Python 3.8 or higher.
    exit /b 1
)

echo Upgrading pip to latest version...
"%PYTHON_PATH%" -m pip install --upgrade pip

echo Installing/upgrading required packages to latest secure versions...
"%PYTHON_PATH%" -m pip install --upgrade -r "%BUILD_DIR%\requirements.txt"
if %ERRORLEVEL% neq 0 (
    echo Failed to install required packages. Aborting.
    exit /b 1
)

echo Verifying PyInstaller installation...
"%PYTHON_PATH%" -c "import PyInstaller; print(f'PyInstaller version: {PyInstaller.__version__}')" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo PyInstaller verification failed. Aborting.
    exit /b 1
)

REM Clean any previous builds
echo Cleaning previous builds...
if exist "%BUILD_DIR%\build" rmdir /s /q "%BUILD_DIR%\build"
if exist "%OUTPUT_DIR%" rmdir /s /q "%OUTPUT_DIR%"
mkdir "%OUTPUT_DIR%"

REM Check if we need to convert SVG to ICO
if not exist "%ICON_DIR%\app_icon.ico" (
    echo Warning: Icon file not found. The executable will be built without a custom icon.
    echo You can add app_icon.ico to the icons folder for a custom icon.
)

echo.
echo Building executable with PyInstaller (this may take a few minutes)...
cd "%BUILD_DIR%"

"%PYTHON_PATH%" -m PyInstaller FindingExcellence.spec ^
    --distpath="%OUTPUT_DIR%" ^
    --workpath="%BUILD_DIR%\build" ^
    --clean ^
    --log-level=INFO

if %ERRORLEVEL% neq 0 (
    echo Build failed!
    echo Check the output above for errors.
    pause
    exit /b 1
)

echo.
echo Verifying built executable...
if not exist "%OUTPUT_DIR%\FindingExcellence.exe" (
    echo ERROR: Executable not found after build!
    exit /b 1
)

echo.
echo Creating distribution package...
if exist "%DIST_DIR%\*" del /q "%DIST_DIR%\*"
xcopy /E /I /Y "%OUTPUT_DIR%\*" "%DIST_DIR%"

REM Create a simple README for the distribution
echo Creating README for distribution...
echo FindingExcellence - Excel File Finder > "%DIST_DIR%\README.txt"
echo. >> "%DIST_DIR%\README.txt"
echo Double-click FindingExcellence.exe to run the application. >> "%DIST_DIR%\README.txt"
echo No installation required. >> "%DIST_DIR%\README.txt"
echo. >> "%DIST_DIR%\README.txt"
echo System Requirements: >> "%DIST_DIR%\README.txt"
echo - Windows 7 or later >> "%DIST_DIR%\README.txt"
echo - 50MB available disk space >> "%DIST_DIR%\README.txt"
echo. >> "%DIST_DIR%\README.txt"
echo For support or questions, refer to the documentation. >> "%DIST_DIR%\README.txt"

echo.
echo ==============================================
echo Build completed successfully!
echo ==============================================
echo Executable location: %OUTPUT_DIR%\FindingExcellence.exe
echo Distribution package: %DIST_DIR%
echo.
echo You can now share the contents of the dist folder with users.
echo.
echo Security note: Some antivirus software may flag PyInstaller executables
echo as suspicious. This is a false positive common with PyInstaller builds.
echo.
pause
exit /b 0
