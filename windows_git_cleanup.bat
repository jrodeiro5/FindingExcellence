@echo off
echo ===== WINDOWS GIT REPOSITORY CLEANUP =====
echo This will reset your repository to a clean state
echo.

echo Current repository size:
git count-objects -vH

echo.
echo OPTION 1: Reset to clean commit (RECOMMENDED)
echo This will go back to your search improvements commit before large files
echo.
set /p choice1="Do you want to reset to clean state? (y/n): "
if /i "%choice1%"=="y" (
    echo Resetting to commit ade7c8f...
    git reset --hard ade7c8f64160ba780d32f1d0901907a99bc90c8b
    echo.
    echo ✅ Repository reset to clean state!
    echo Your search improvements are preserved.
    goto end
)

echo.
echo OPTION 2: Nuclear option - Fresh repository
echo This will completely restart the repository
echo.
set /p choice2="Do you want to start fresh repository? (y/n): "
if /i "%choice2%"=="y" (
    echo Backing up important files...
    copy "core\file_search.py" "..\file_search_backup.py"
    copy "ui\main_window.py" "..\main_window_backup.py"  
    copy "build_with_py_launcher.bat" "..\build_backup.bat"
    
    echo Deleting git history...
    rmdir /s /q .git
    
    echo Creating fresh repository...
    git init
    git add .gitignore core/ ui/ build_with_py_launcher.bat README.md
    git commit -m "feat: Clean repository with search responsiveness improvements"
    
    echo ✅ Fresh repository created!
    echo Your files are backed up in parent directory.
    goto end
)

echo No changes made.

:end
echo.
echo New repository size:
git count-objects -vH
echo.
pause