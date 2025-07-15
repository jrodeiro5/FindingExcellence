@echo off
echo === COMPREHENSIVE GIT CLEANUP ===
echo This will remove all executables and build artifacts from git tracking
echo.

echo Step 1: Staging deleted executable files...
git add "dist/FindingExcellence.exe"
echo.

echo Step 2: Removing build artifacts from git tracking...
git rm --cached "build_resources/output/FindingExcellence.exe" 2>nul
git rm --cached -r "build_resources/build/" 2>nul
git rm --cached "FindingExcellence.spec" 2>nul
git rm --cached "main.spec" 2>nul
echo.

echo Step 3: Staging all updated files...
git add -u
echo.

echo Step 4: Current git status:
git status --short
echo.

echo Step 5: Files still tracked by git (checking for problems):
echo Checking for .exe files:
git ls-files | findstr /i "\.exe"
if %ERRORLEVEL% neq 0 echo   ✅ No .exe files tracked

echo Checking for build files:  
git ls-files | findstr /i "build_resources.*build\|build_resources.*output"
if %ERRORLEVEL% neq 0 echo   ✅ No build artifacts tracked

echo.
echo === READY TO COMMIT ===
echo If everything looks good above, the next step is to commit these changes.
pause