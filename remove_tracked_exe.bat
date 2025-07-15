@echo off
echo === Removing Executables and Build Artifacts from Git Tracking ===
echo.

echo Removing deleted files from git tracking...
git add "./dist/FindingExcellence.exe" 2>nul
git add "dist/FindingExcellence.exe" 2>nul

echo Removing build artifacts that shouldn't be tracked...
git rm --cached "build_resources/output/FindingExcellence.exe" 2>nul
git rm --cached -r "build_resources/build/" 2>nul
git rm --cached "FindingExcellence.spec" 2>nul

echo Staging all other deletions...
git add -u

echo.
echo Checking current status...
git status --short

echo.
echo Ready to commit the cleanup!
pause