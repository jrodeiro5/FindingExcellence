@echo off
setlocal enabledelayedexpansion

echo ===== CLEAN SLATE SCRIPT =====
echo Starting comprehensive repository cleanup...
echo.

REM 1. Remove all .bat files from the cleanup plan
echo [1/6] Removing cleanup batch files...
for %%f in (
    fix_logo_now.bat
    cleanup_repo.bat
    nuclear_cleanup.bat
    remove_tracked_exe.bat
    windows_git_cleanup.bat
    verify_after_cleanup.bat
    full_verification.bat
    check_git_tracking.bat
    delete_heavy_build_files.bat
    setup_logo.bat
    build_with_diagnostics.bat
    build_with_py_launcher.bat
    build_with_py_launcher.bat.backup
) do (
    if exist "%%f" (
        echo Deleting %%f
        del /q "%%f" 2>nul
    )
)

REM 2. Remove extra .spec files
echo.
echo [2/6] Cleaning up .spec files...
if exist "main.spec" (
    echo Deleting main.spec
    del /q "main.spec" 2>nul
)
if exist "build_resources\FindingExcellence_fixed.spec" (
    echo Deleting build_resources\FindingExcellence_fixed.spec
    del /q "build_resources\FindingExcellence_fixed.spec" 2>nul
)
if exist "build_resources\FindingExcellence_updated.spec" (
    echo Deleting build_resources\FindingExcellence_updated.spec
    del /q "build_resources\FindingExcellence_updated.spec" 2>nul
)

REM 3. Remove Windows shortcuts
echo.
echo [3/6] Removing Windows shortcuts...
if exist "main.py - Acceso directo.lnk" (
    echo Deleting "main.py - Acceso directo.lnk"
    del /q "main.py - Acceso directo.lnk" 2>nul
)

REM 4. Clean up UI backups
echo.
echo [4/6] Cleaning up UI backup files...
if exist "ui" (
    pushd ui
    for %%f in (
        content_search_panel.py.bak
        content_search_panel.py.direct_fix
        content_search_panel.py.full_reset
        content_search_panel.py.indent_fix
        keyboard_shortcuts.py.bak
        main_window.py.backup
        main_window.py.bak
        main_window.py.improved_bak
        results_panel.py.backup
        results_panel.py.bak
        results_panel.py.improved_bak
    ) do (
        if exist "%%f" (
            echo Deleting ui\%%f
            del /q "%%f" 2>nul
        )
    )
    popd
)

REM 5. Clean up core backups
echo.
echo [5/6] Cleaning up core backup files...
if exist "core" (
    if exist "core\file_search.py.backup" (
        echo Deleting core\file_search.py.backup
        del /q "core\file_search.py.backup" 2>nul
    )
    if exist "core\content_search_fixed.py" (
        echo Deleting core\content_search_fixed.py
        del /q "core\content_search_fixed.py" 2>nul
    )
)

REM 6. Create test directory and move debug/test files
echo.
echo [6/6] Organizing test files...
if not exist "test" (
    mkdir test
)

for %%f in (
    advanced_diagnostic.py
    test_search_improvements.py
    verify_improvements.py
    view_structure.py
    clients.json
) do (
    if exist "%%f" (
        echo Moving %%f to test\
        move /y "%%f" "test\\" >nul 2>&1
    )
)

REM 7. Clean up requirements files
echo.
echo [7/7] Cleaning up requirements files...
if exist "requirements_frozen.txt" (
    echo Deleting requirements_frozen.txt
    del /q "requirements_frozen.txt" 2>nul
)
if exist "build_resources\requirements_updated.txt" (
    echo Deleting build_resources\requirements_updated.txt
    del /q "build_resources\requirements_updated.txt" 2>nul
)

echo.
echo ✅ Cleanup complete!
echo.
echo Next steps:
echo 1. Review changes with: git status
echo 2. Add all changes: git add -A
echo 3. Commit: git commit -m "chore: Clean up repository"
echo 4. Push changes: git push
echo.
pause
