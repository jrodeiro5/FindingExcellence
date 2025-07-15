@echo off
echo Converting PNG logo to ICO format for FindingExcellence...
echo.

REM Get the Python path from the parent directory setup
if "%PYTHON_PATH%"=="" (
    echo Attempting to find Python...
    python convert_icon.py
) else (
    echo Using specified Python path: %PYTHON_PATH%
    "%PYTHON_PATH%" convert_icon.py
)

pause
