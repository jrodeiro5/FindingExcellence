@echo off
echo ===== FindingExcellence Logo Setup =====
echo.

REM Set directories
set PROJECT_DIR=%~dp0
set RESOURCES_DIR=%PROJECT_DIR%resources
set BUILD_ICONS_DIR=%PROJECT_DIR%build_resources\icons

echo Setting up your new FindingExcellence logo...
echo.

REM Check if resources folder exists
if not exist "%RESOURCES_DIR%" (
    echo Error: Resources folder not found at %RESOURCES_DIR%
    exit /b 1
)

REM Check if new logo ICO file exists
if not exist "%RESOURCES_DIR%\FindingExcellence_new_logo_1.ico" (
    echo Error: New logo ICO file not found in resources folder
    exit /b 1
)

REM Create build icons directory if it doesn't exist
if not exist "%BUILD_ICONS_DIR%" mkdir "%BUILD_ICONS_DIR%"

echo Copying logo files...

REM Copy the ICO file to build resources (as primary icon)
copy "%RESOURCES_DIR%\FindingExcellence_new_logo_1.ico" "%BUILD_ICONS_DIR%\app_icon.ico"
if %ERRORLEVEL% neq 0 (
    echo Failed to copy ICO file!
    exit /b 1
)

REM Also copy with descriptive name for future reference
copy "%RESOURCES_DIR%\FindingExcellence_new_logo_1.ico" "%BUILD_ICONS_DIR%\FindingExcellence_new_logo.ico"

REM Copy other formats for completeness
if exist "%RESOURCES_DIR%\FindingExcellence_new_logo.png" (
    copy "%RESOURCES_DIR%\FindingExcellence_new_logo.png" "%BUILD_ICONS_DIR%\"
)

if exist "%RESOURCES_DIR%\FindingExcellence_new_logo.svg" (
    copy "%RESOURCES_DIR%\FindingExcellence_new_logo.svg" "%BUILD_ICONS_DIR%\"
)

echo.
echo ✓ Logo files copied successfully!
echo ✓ Your new logo is now ready to be used in the build process
echo.
echo Next steps:
echo 1. Run 'install_executable.bat' to rebuild the application with your new logo
echo 2. The new executable will have your custom FindingExcellence logo!
echo.

pause
