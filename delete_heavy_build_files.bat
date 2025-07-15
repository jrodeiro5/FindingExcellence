@echo off
echo === REMOVING HEAVY BUILD ARTIFACTS ===
echo This will delete ~145MB of PyInstaller build files
echo.

echo Calculating current size...
for /f "tokens=3" %%a in ('dir "build" /s /-c ^| findstr /c:" bytes"') do set build_size=%%a
echo Current build folder size: %build_size% bytes
echo.

echo Deleting heavy build artifacts...
if exist "build\FindingExcellence" (
    echo Removing build\FindingExcellence\ (72+ MB)...
    rmdir /s /q "build\FindingExcellence"
)

if exist "build\main" (
    echo Removing build\main\ (72+ MB)...
    rmdir /s /q "build\main"
)

if exist "build_resources\build" (
    echo Removing build_resources\build\...
    rmdir /s /q "build_resources\build"
)

if exist "build_resources\output" (
    echo Removing build_resources\output\...
    rmdir /s /q "build_resources\output"
)

echo.
echo ✅ Heavy build artifacts removed!
echo.

echo Checking git status...
git status --short | findstr /i "build\|\.exe\|\.pkg"

echo.
echo === SUMMARY ===
echo - Deleted ~145MB of PyInstaller build artifacts
echo - Removed executable files from build directories  
echo - Repository should now be much cleaner
echo.
echo Next: Run git add -A and commit the cleanup
pause