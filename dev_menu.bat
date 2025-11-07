@echo off
REM Script de desarrollo para FindingExcellence
REM Menú principal para todas las tareas de desarrollo

:MENU
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    FindingExcellence - Menu Desarrollo          ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo ¿Qué deseas hacer?
echo.
echo   1. 🔧 Configurar entorno virtual (primera vez)
echo   2. ▶️  Ejecutar aplicación (con venv)
echo   3. 📦 Crear ejecutable (build)
echo   4. 🧪 Activar entorno para desarrollo
echo   5. 📋 Ver estado del proyecto
echo   6. 🔄 Actualizar dependencias
echo   7. 🗑️  Limpiar archivos temporales
echo   8. ❌ Salir
echo.
set /p choice="Selecciona una opción (1-8): "

if "%choice%"=="1" goto SETUP_VENV
if "%choice%"=="2" goto RUN_APP
if "%choice%"=="3" goto BUILD_APP
if "%choice%"=="4" goto ACTIVATE_ENV
if "%choice%"=="5" goto PROJECT_STATUS
if "%choice%"=="6" goto UPDATE_DEPS
if "%choice%"=="7" goto CLEAN_PROJECT
if "%choice%"=="8" goto EXIT

echo Opción inválida. Presiona cualquier tecla para continuar...
pause >nul
goto MENU

:SETUP_VENV
echo.
echo 🔧 Configurando entorno virtual...
call setup_venv.bat
echo.
echo ✓ Configuración completada. Presiona cualquier tecla para continuar...
pause >nul
goto MENU

:RUN_APP
echo.
echo ▶️ Ejecutando aplicación...
if not exist "finding_excellence_env" (
    echo ERROR: Entorno virtual no encontrado.
    echo Por favor ejecuta la opción 1 primero.
    pause
    goto MENU
)
call finding_excellence_env\Scripts\activate.bat && python main.py
pause
goto MENU

:BUILD_APP
echo.
echo 📦 Creando ejecutable...
call build_with_venv.bat
echo.
echo ✓ Build completado. Presiona cualquier tecla para continuar...
pause >nul
goto MENU

:ACTIVATE_ENV
echo.
echo 🧪 Activando entorno de desarrollo...
call activate_venv.bat
goto MENU

:PROJECT_STATUS
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                     Estado del Proyecto                         ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Verificar Python
echo 🐍 Python Global:
python --version 2>nul
if %ERRORLEVEL% neq 0 (
    echo   ❌ No encontrado en PATH
) else (
    echo   ✓ Disponible
)

echo.
REM Verificar venv
echo 🔧 Entorno Virtual:
if exist "finding_excellence_env" (
    echo   ✓ Configurado: finding_excellence_env
    call finding_excellence_env\Scripts\activate.bat
    if defined VIRTUAL_ENV (
        echo   📍 Ubicación: %VIRTUAL_ENV%
        echo   🐍 Python venv:
        python --version
        echo   📦 Librerías principales:
        python -c "import pandas; print(f'   - pandas: {pandas.__version__}')" 2>nul
        python -c "import openpyxl; print(f'   - openpyxl: {openpyxl.__version__}')" 2>nul  
        python -c "import PyInstaller; print(f'   - PyInstaller: {PyInstaller.__version__}')" 2>nul
        call deactivate
    )
) else (
    echo   ❌ No configurado (ejecuta opción 1)
)

echo.
REM Verificar archivos principales
echo 📁 Archivos del Proyecto:
if exist "main.py" (echo   ✓ main.py) else (echo   ❌ main.py)
if exist "build_resources\FindingExcellence.spec" (echo   ✓ build_resources\FindingExcellence.spec) else (echo   ❌ FindingExcellence.spec)
if exist "core\content_search.py" (echo   ✓ core\content_search.py) else (echo   ❌ content_search.py)

echo.
REM Verificar builds
echo 🏗️ Builds:
if exist "dist\FindingExcellence.exe" (
    echo   ✓ Ejecutable disponible: dist\FindingExcellence.exe
    for %%I in ("dist\FindingExcellence.exe") do echo   📅 Fecha: %%~tI
    for %%I in ("dist\FindingExcellence.exe") do echo   📏 Tamaño: %%~zI bytes
) else (
    echo   ❌ No hay ejecutable (usar opción 3 para crear)
)

echo.
echo Presiona cualquier tecla para volver al menú...
pause >nul
goto MENU

:UPDATE_DEPS
echo.
echo 🔄 Actualizando dependencias...
if not exist "finding_excellence_env" (
    echo ERROR: Entorno virtual no encontrado.
    echo Por favor ejecuta la opción 1 primero.
    pause
    goto MENU
)
call finding_excellence_env\Scripts\activate.bat
pip install --upgrade pip
pip install --upgrade -r build_resources\requirements_venv.txt
call deactivate
echo.
echo ✓ Dependencias actualizadas. Presiona cualquier tecla para continuar...
pause >nul
goto MENU

:CLEAN_PROJECT
echo.
echo 🗑️ Limpiando archivos temporales...
echo.
echo Eliminando:
if exist "__pycache__" (
    echo   - __pycache__ folders
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
)
if exist "*.pyc" (
    echo   - .pyc files  
    del /s /q "*.pyc" 2>nul
)
if exist "build_resources\build" (
    echo   - build folder
    rd /s /q "build_resources\build"
)
if exist "build_resources\output" (
    echo   - output folder
    rd /s /q "build_resources\output"
)
if exist "*.log" (
    echo   - log files
    del /q "*.log" 2>nul
)
echo.
echo ✓ Limpieza completada. Presiona cualquier tecla para continuar...
pause >nul
goto MENU

:EXIT
echo.
echo ¡Hasta luego! 👋
timeout /t 2 /nobreak >nul
exit /b 0
