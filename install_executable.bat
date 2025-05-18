@echo off
REM Installation script for FindingExcellence

echo ===== FindingExcellence Quick Installer =====
echo.
echo This will create an executable for FindingExcellence.
echo You only need to run this once.
echo.

REM First, try to find Python using the PATH environment
echo Checking for Python installation...
where python > NUL 2>&1

if %ERRORLEVEL% neq 0 (
    echo Python not found in PATH. Looking for Python in Program Files...
    
    REM Try to find Python in common installation locations
    if exist "C:\Program Files\Python*" (
        for /d %%i in ("C:\Program Files\Python*") do (
            if exist "%%i\python.exe" (
                set PYTHON_PATH=%%i\python.exe
                goto :found_python
            )
        )
    )
    
    if exist "C:\Program Files (x86)\Python*" (
        for /d %%i in ("C:\Program Files (x86)\Python*") do (
            if exist "%%i\python.exe" (
                set PYTHON_PATH=%%i\python.exe
                goto :found_python
            )
        )
    )
    
    REM Check in user AppData directories - common for user-based installations
    if exist "%LOCALAPPDATA%\Programs\Python\Python*" (
        for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
            if exist "%%i\python.exe" (
                set PYTHON_PATH=%%i\python.exe
                goto :found_python
            )
        )
    )
    
    echo Python installation not found automatically.
    echo.
    echo Please enter the full path to your Python executable (e.g., C:\Path\To\Python\python.exe):
    set /p PYTHON_PATH="> "
    
    if not exist "!PYTHON_PATH!" (
        echo The specified file does not exist. Please try again with a valid path.
        pause
        exit /b 1
    )
) else (
    set PYTHON_PATH=python
)

:found_python
echo Using Python: %PYTHON_PATH%

REM Check Python version
"%PYTHON_PATH%" -c "import sys; print('Python', sys.version_info.major, '.', sys.version_info.minor, sep=''); exit(0 if sys.version_info.major >= 3 and sys.version_info.minor >= 6 else 1)" > NUL 2>&1
if %ERRORLEVEL% neq 0 (
    echo This application requires Python 3.6 or higher.
    echo Please install a compatible Python version.
    pause
    exit /b 1
)

REM Install required packages
echo Installing required packages...
"%PYTHON_PATH%" -m pip install -r build_resources\requirements.txt

if %ERRORLEVEL% neq 0 (
    echo Failed to install required packages.
    echo Please make sure you have internet access and pip is working correctly.
    pause
    exit /b 1
)

REM Build the executable
echo.
echo Building the executable...
call build_resources\build.bat

if %ERRORLEVEL% neq 0 (
    echo Build process failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo The executable is now available in the dist folder.
echo.

pause
exit /b 0
