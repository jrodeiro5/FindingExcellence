@echo off
echo ===== Repository Cleanup Script =====
echo Removing build artifacts and executables from git tracking...
echo.

REM Delete build artifacts
if exist "dist" (
    echo Removing dist folder...
    rmdir /s /q "dist"
)

if exist "build" (
    echo Removing build folder...
    rmdir /s /q "build"
)

if exist "build_resources\build" (
    echo Removing build_resources\build folder...
    rmdir /s /q "build_resources\build"
)

if exist "build_resources\output" (
    echo Removing build_resources\output folder...
    rmdir /s /q "build_resources\output"
)

REM Remove spec files
del *.spec 2>nul
del build_resources\*.spec 2>nul

echo.
echo ✅ Cleanup complete!
echo.
echo Next steps:
echo 1. Run: git add -A
echo 2. Run: git commit -m "clean: Remove all build artifacts and executables"
echo 3. Build new executable when needed
echo 4. Create GitHub release with the executable
echo.
pause