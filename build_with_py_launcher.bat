@echo off
echo ===== FindingExcellence Build Script (Python Launcher) =====
echo.

REM Set directories
set PROJECT_DIR=%~dp0
set BUILD_DIR=%PROJECT_DIR%build_resources
set OUTPUT_DIR=%BUILD_DIR%\output
set ICON_DIR=%BUILD_DIR%\icons
set DIST_DIR=%PROJECT_DIR%dist

echo Project Directory: %PROJECT_DIR%
echo Build Directory: %BUILD_DIR%
echo Icons Directory: %ICON_DIR%
echo.

REM Create necessary directories
if not exist "%OUTPUT_DIR%" (
    echo Creating output directory...
    mkdir "%OUTPUT_DIR%"
)
if not exist "%DIST_DIR%" (
    echo Creating dist directory...
    mkdir "%DIST_DIR%"
)

REM Check for Python using py launcher
echo Checking for Python using py launcher...
py --version 2>nul
if errorlevel 1 (
    echo ERROR: Python launcher py not found!
    echo Please install Python from python.org or Microsoft Store
    pause
    exit /b 1
)

echo Using Python launcher: py
py --version

REM Check for icon file
echo.
echo Checking for icon file...
set ICON_FILE=
if exist "%ICON_DIR%\app_icon.ico" (
    echo ✓ Icon file found: %ICON_DIR%\app_icon.ico
    set ICON_FILE=%ICON_DIR%\app_icon.ico
    goto icon_found
)
if exist "%ICON_DIR%\FindingExcellence_new_logo.ico" (
    echo ✓ Icon file found: %ICON_DIR%\FindingExcellence_new_logo.ico
    set ICON_FILE=%ICON_DIR%\FindingExcellence_new_logo.ico
    goto icon_found
)
if exist "%PROJECT_DIR%resources\FindingExcellence_new_logo_1.ico" (
    echo ✓ Icon file found: %PROJECT_DIR%resources\FindingExcellence_new_logo_1.ico
    set ICON_FILE=%PROJECT_DIR%resources\FindingExcellence_new_logo_1.ico
    goto icon_found
)
echo ⚠ Icon file not found, will build without custom icon
:icon_found

REM Install/check PyInstaller
echo.
echo Checking PyInstaller...
py -c "import PyInstaller; print('PyInstaller version:', PyInstaller.__version__)" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    py -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller!
        pause
        exit /b 1
    )
)

REM Install requirements from requirements.txt
echo.
echo Installing requirements from requirements.txt...
if exist "%BUILD_DIR%\requirements.txt" (
    py -m pip install -r "%BUILD_DIR%\requirements.txt"
    if errorlevel 1 (
        echo ERROR: Failed to install requirements!
        pause
        exit /b 1
    )
) else (
    echo ⚠ requirements.txt not found, installing basic requirements...
    py -m pip install pandas openpyxl xlrd tkcalendar
)

REM Clean previous builds
echo.
echo Cleaning previous builds...
if exist "%BUILD_DIR%\build" (
    echo Removing old build directory...
    rmdir /s /q "%BUILD_DIR%\build"
)
if exist "%OUTPUT_DIR%\FindingExcellence.exe" (
    echo Removing old executable...
    del "%OUTPUT_DIR%\FindingExcellence.exe"
)

REM Build with PyInstaller
echo.
echo Building executable...
cd "%PROJECT_DIR%"

if not "%ICON_FILE%"=="" (
    echo Building with custom icon: %ICON_FILE%
    py -m PyInstaller --onefile --windowed --icon="%ICON_FILE%" --add-data "%ICON_DIR%;icons" --distpath="%OUTPUT_DIR%" --workpath="%BUILD_DIR%\build" --name=FindingExcellence main.py
) else (
    echo Building without custom icon...
    py -m PyInstaller --onefile --windowed --add-data "%ICON_DIR%;icons" --distpath="%OUTPUT_DIR%" --workpath="%BUILD_DIR%\build" --name=FindingExcellence main.py
)

if errorlevel 1 (
    echo.
    echo ❌ BUILD FAILED!
    echo Check the error messages above for details.
    pause
    exit /b 1
)

REM Copy to dist folder
echo.
echo Copying executable to dist folder...
if exist "%OUTPUT_DIR%\FindingExcellence.exe" (
    copy "%OUTPUT_DIR%\FindingExcellence.exe" "%DIST_DIR%\"
    echo.
    echo ✅ BUILD SUCCESSFUL!
    echo.
    echo Executable created at: %OUTPUT_DIR%\FindingExcellence.exe
    echo Copied to: %DIST_DIR%\FindingExcellence.exe
    echo.
    echo File size:
    dir "%DIST_DIR%\FindingExcellence.exe" | findstr FindingExcellence.exe
    echo.
    echo You can now run FindingExcellence.exe with your improved search responsiveness!
) else (
    echo.
    echo ❌ ERROR: Executable not found after build!
    echo Something went wrong during the build process.
    echo Check the build output above for details.
)

echo.
echo Build completed at: %date% %time%
pause