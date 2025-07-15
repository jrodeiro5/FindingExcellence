@echo off
echo ===== FindingExcellence Diagnostic Build Script =====
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

REM Check for Python
echo Checking for Python...
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    set PYTHON_CMD=python
) else (
    echo Python not found in PATH. Trying alternative locations...
    if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
        set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    ) else if exist "C:\Python313\python.exe" (
        set PYTHON_CMD="C:\Python313\python.exe"
    ) else (
        echo ERROR: Python not found! Please install Python 3.13 or add it to PATH.
        pause
        exit /b 1
    )
)

echo Using Python: %PYTHON_CMD%
%PYTHON_CMD% --version

REM Check for icon file
echo.
echo Checking for icon file...
if exist "%ICON_DIR%\app_icon.ico" (
    echo ✓ Icon file found: %ICON_DIR%\app_icon.ico
) else (
    echo ⚠ Icon file not found, will build without custom icon
)

REM Install/check PyInstaller
echo.
echo Checking PyInstaller...
%PYTHON_CMD% -c "import PyInstaller; print('PyInstaller version:', PyInstaller.__version__)" 2>nul
if %ERRORLEVEL% neq 0 (
    echo Installing PyInstaller...
    %PYTHON_CMD% -m pip install pyinstaller
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to install PyInstaller!
        pause
        exit /b 1
    )
)

REM Install other requirements
echo.
echo Installing requirements...
%PYTHON_CMD% -m pip install pandas openpyxl xlrd tkcalendar

REM Build with PyInstaller
echo.
echo Building executable...
cd "%PROJECT_DIR%"

if exist "%ICON_DIR%\app_icon.ico" (
    echo Building with custom icon...
    %PYTHON_CMD% -m PyInstaller --onefile --windowed --icon="%ICON_DIR%\app_icon.ico" --distpath="%OUTPUT_DIR%" --workpath="%BUILD_DIR%\build" --name=FindingExcellence main.py
) else (
    echo Building without custom icon...
    %PYTHON_CMD% -m PyInstaller --onefile --windowed --distpath="%OUTPUT_DIR%" --workpath="%BUILD_DIR%\build" --name=FindingExcellence main.py
)

if %ERRORLEVEL% neq 0 (
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
    echo You can now run FindingExcellence.exe with your custom logo!
) else (
    echo.
    echo ❌ ERROR: Executable not found after build!
    echo Something went wrong during the build process.
)

echo.
pause
