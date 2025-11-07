@echo off
REM Script de activación rápida del entorno virtual
REM FindingExcellence

set PROJECT_DIR=%~dp0
set VENV_NAME=finding_excellence_env
set VENV_PATH=%PROJECT_DIR%%VENV_NAME%

if not exist "%VENV_PATH%" (
    echo ERROR: Entorno virtual no encontrado en: %VENV_PATH%
    echo.
    echo Para crearlo ejecuta: setup_venv.bat
    pause
    exit /b 1
)

echo Activando entorno virtual FindingExcellence...
call %VENV_PATH%\Scripts\activate.bat

echo.
echo ✓ Entorno virtual activado
echo Python: %VIRTUAL_ENV%
echo.
echo Comandos disponibles:
echo   python main.py          - Ejecutar aplicación
echo   pip list                - Ver librerías instaladas  
echo   deactivate              - Desactivar entorno
echo   build_with_venv.bat     - Crear ejecutable
echo.

REM Mantener la ventana abierta para trabajar
cmd /k
