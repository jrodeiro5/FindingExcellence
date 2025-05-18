@echo off
REM Build script for FindingExcellence executable

echo ===== FindingExcellence Build Script =====
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

echo Checking for PyInstaller...
"%PYTHON_PATH%" -c "import PyInstaller" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo PyInstaller not found. Installing required packages...
    "%PYTHON_PATH%" -m pip install -r "%BUILD_DIR%\requirements.txt"
    if %ERRORLEVEL% neq 0 (
        echo Failed to install required packages. Aborting.
        exit /b 1
    )
)

REM Check if we need to convert SVG to ICO
if not exist "%ICON_DIR%\app_icon.ico" (
    echo Converting SVG icon to ICO...
    echo Note: This requires Inkscape and ImageMagick. If not installed, the executable will be built without an icon.
    
    where inkscape >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo Inkscape not found. Skipping icon conversion.
    ) else (
        where magick >nul 2>&1
        if %ERRORLEVEL% neq 0 (
            echo ImageMagick not found. Skipping icon conversion.
        ) else (
            inkscape -w 256 -h 256 "%ICON_DIR%\app_icon.svg" -o "%ICON_DIR%\app_icon_256.png"
            magick convert "%ICON_DIR%\app_icon_256.png" -define icon:auto-resize=256,128,64,48,32,16 "%ICON_DIR%\app_icon.ico"
            echo Icon conversion complete.
        )
    )
)

echo.
echo Building executable with PyInstaller...
cd "%BUILD_DIR%"

"%PYTHON_PATH%" -m PyInstaller FindingExcellence.spec --distpath="%OUTPUT_DIR%" --workpath="%BUILD_DIR%\build" --clean

if %ERRORLEVEL% neq 0 (
    echo Build failed!
    exit /b 1
)

echo.
echo Creating distribution package...
xcopy /E /I /Y "%OUTPUT_DIR%\*" "%DIST_DIR%"

echo.
echo Build completed successfully!
echo Executable is available at: %OUTPUT_DIR%\FindingExcellence.exe
echo Distribution package is available at: %DIST_DIR%

exit /b 0
