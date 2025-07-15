@echo off
echo Updating FindingExcellence icon...

REM Copy the new logo to the build resources icons folder
copy "resources\FindingExcellence_new_logo_1.ico" "build_resources\icons\app_icon.ico"

if %ERRORLEVEL% neq 0 (
    echo Failed to copy icon file!
    exit /b 1
)

echo Icon updated successfully!
echo You can now run install_executable.bat to rebuild with the new icon.

pause
