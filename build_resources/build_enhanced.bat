@echo off
REM FindingExcellence - Build Script (standalone, no external dependencies)
REM Uso: doble clic o ejecutar desde cualquier terminal.
REM Requisito: Python 3.8+ instalado y en el PATH del sistema.

setlocal enabledelayedexpansion

echo ===== FindingExcellence Build Script =====
echo.

REM --- Detectar Python automaticamente ---
echo Buscando Python en el sistema...
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python no encontrado en el PATH.
    echo Instala Python 3.8+ desde https://www.python.org y asegurate de marcar
    echo la opcion "Add Python to PATH" durante la instalacion.
    pause
    exit /b 1
)

REM Capturar la ruta de Python
for /f "tokens=*" %%i in ('where python') do (
    set PYTHON_PATH=%%i
    goto :python_found
)

:python_found
echo Python encontrado en: %PYTHON_PATH%

REM Verificar version de Python (requiere 3.8+)
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Se requiere Python 3.8 o superior.
    python --version
    pause
    exit /b 1
)
python --version

echo.

REM --- Directorios ---
set BUILD_DIR=%~dp0
REM Quitar barra final si la hay
if "%BUILD_DIR:~-1%"=="\" set BUILD_DIR=%BUILD_DIR:~0,-1%

set PROJECT_DIR=%BUILD_DIR%\..
set WORK_DIR=%BUILD_DIR%\build
set DIST_DIR=%PROJECT_DIR%\dist
set ICON_DIR=%BUILD_DIR%\icons
set ICON_PATH=%ICON_DIR%\app_icon.ico

REM Crear directorios necesarios
if not exist "%DIST_DIR%" mkdir "%DIST_DIR%"

REM --- Actualizar pip ---
echo Actualizando pip...
python -m pip install --upgrade pip --quiet
echo.

REM --- Instalar / actualizar dependencias ---
echo Instalando dependencias desde requirements.txt...
python -m pip install --upgrade -r "%BUILD_DIR%\requirements.txt"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Fallo al instalar dependencias.
    pause
    exit /b 1
)
echo.

REM --- Verificar PyInstaller ---
python -c "import PyInstaller; print('PyInstaller', PyInstaller.__version__)" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: PyInstaller no disponible tras la instalacion.
    pause
    exit /b 1
)

REM --- Limpiar builds anteriores ---
echo Limpiando builds anteriores...
if exist "%WORK_DIR%" rmdir /s /q "%WORK_DIR%"
if exist "%DIST_DIR%\FindingExcellence" rmdir /s /q "%DIST_DIR%\FindingExcellence"

REM --- Verificar icono ---
if not exist "%ICON_PATH%" (
    echo Aviso: No se encontro el icono en %ICON_PATH%
    echo El ejecutable se generara sin icono personalizado.
    set ICON_FLAG=
) else (
    set ICON_FLAG=--icon="%ICON_PATH%"
)

echo.
echo Construyendo ejecutable con PyInstaller ^(modo --onedir^)...
echo Esto puede tardar unos minutos...
echo.

REM --- Ejecutar PyInstaller directamente con flags (sin depender del .spec para el modo) ---
REM Se usa el .spec para hiddenimports pero se sobreescribe distpath y workpath
cd /d "%PROJECT_DIR%"

python -m PyInstaller "%BUILD_DIR%\FindingExcellence.spec" ^
    --distpath="%DIST_DIR%" ^
    --workpath="%WORK_DIR%" ^
    --clean ^
    --log-level=WARN

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: El build ha fallado. Revisa los mensajes anteriores.
    pause
    exit /b 1
)

REM --- Verificar resultado ---
echo.
if exist "%DIST_DIR%\FindingExcellence\FindingExcellence.exe" (
    echo ==============================================
    echo  Build completado correctamente ^(--onedir^)
    echo ==============================================
    echo.
    echo Ejecutable: %DIST_DIR%\FindingExcellence\FindingExcellence.exe
    echo.
    echo Comparte la carpeta completa: %DIST_DIR%\FindingExcellence\
    echo ^(el usuario solo necesita hacer doble clic en FindingExcellence.exe^)
    echo.
    echo NOTA: Algunos antivirus pueden marcar el exe como sospechoso.
    echo Esto es un falso positivo comun con builds de PyInstaller.
) else if exist "%DIST_DIR%\FindingExcellence.exe" (
    echo ==============================================
    echo  Build completado correctamente ^(--onefile^)
    echo ==============================================
    echo.
    echo Ejecutable: %DIST_DIR%\FindingExcellence.exe
) else (
    echo ERROR: No se encontro el ejecutable tras el build.
    echo Revisa el log de PyInstaller arriba para mas detalles.
    pause
    exit /b 1
)

echo.
pause
exit /b 0
