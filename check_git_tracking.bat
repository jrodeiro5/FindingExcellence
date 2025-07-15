@echo off
echo === Checking Git Tracked Files ===
echo.

echo Checking for .exe files tracked by git:
git ls-files | findstr /i "\.exe"
if %ERRORLEVEL% neq 0 (
    echo ✅ No .exe files are tracked by git
) else (
    echo ❌ PROBLEM: .exe files are still tracked!
)

echo.
echo Checking for build/dist files tracked by git:
git ls-files | findstr /i "build\|dist"
if %ERRORLEVEL% neq 0 (
    echo ✅ No build/dist files are tracked by git
) else (
    echo ❌ PROBLEM: build/dist files are still tracked!
)

echo.
echo Checking for .spec files tracked by git:
git ls-files | findstr /i "\.spec"
if %ERRORLEVEL% neq 0 (
    echo ✅ No .spec files are tracked by git
) else (
    echo ❌ PROBLEM: .spec files are still tracked!
)

echo.
echo === Git Status Summary ===
git status --porcelain | findstr /i "\.exe\|build\|dist\|\.spec"

echo.
pause