@echo off
REM Script de build con entorno virtual aislado
REM FindingExcellence - Build con venv

echo ===== Build FindingExcellence (con venv) =====
echo.

set PROJECT_DIR=%~dp0
set VENV_NAME=finding_excellence_env
set VENV_PATH=%PROJECT_DIR%%VENV_NAME%
set BUILD_DIR=%PROJECT_DIR%build_resources
set OUTPUT_DIR=%BUILD_DIR%\output
set DIST_DIR=%PROJECT_DIR%dist

REM Verificar que existe el entorno virtual
if not exist "%VENV_PATH%" (
    echo ERROR: Entorno virtual no encontrado: %VENV_PATH%
    echo.
    echo Por favor ejecuta primero: setup_venv.bat
    pause
    exit /b 1
)

REM Crear directorios necesarios
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
if not exist "%DIST_DIR%" mkdir "%DIST_DIR%"

REM Activar entorno virtual
echo Activando entorno virtual...
call %VENV_PATH%\Scripts\activate.bat

if not defined VIRTUAL_ENV (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo ✓ Entorno virtual activado: %VIRTUAL_ENV%

REM Verificar Python en venv
echo Verificando Python en venv...
python --version
echo Ubicación Python: 
where python

REM Verificar PyInstaller
echo Verificando PyInstaller...
python -c "import PyInstaller; print(f'PyInstaller {PyInstaller.__version__}')"
if %ERRORLEVEL% neq 0 (
    echo ERROR: PyInstaller no disponible en el venv
    echo Ejecutando instalación...
    python -m pip install -r build_resources\requirements_venv.txt
    if %ERRORLEVEL% neq 0 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

REM Limpiar builds anteriores
echo Limpiando builds anteriores...
if exist "%BUILD_DIR%\build" rmdir /s /q "%BUILD_DIR%\build"
if exist "%OUTPUT_DIR%" rmdir /s /q "%OUTPUT_DIR%"
if exist "%DIST_DIR%\*" del /q "%DIST_DIR%\*"
mkdir "%OUTPUT_DIR%"

REM Mostrar información del entorno
echo.
echo Información del entorno:
echo - Proyecto: %PROJECT_DIR%
echo - Venv: %VIRTUAL_ENV%
echo - Output: %OUTPUT_DIR%
echo.

REM Ejecutar PyInstaller
echo Ejecutando PyInstaller...
cd "%BUILD_DIR%"

python -m PyInstaller FindingExcellence.spec ^
    --distpath="%OUTPUT_DIR%" ^
    --workpath="%BUILD_DIR%\build" ^
    --clean ^
    --log-level=INFO

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Build falló
    echo Revisa el output anterior para detalles del error
    pause
    exit /b 1
)

REM Verificar ejecutable creado
if not exist "%OUTPUT_DIR%\FindingExcellence.exe" (
    echo ERROR: Ejecutable no encontrado después del build
    pause
    exit /b 1
)

REM Copiar a carpeta dist
echo.
echo Copiando a carpeta de distribución...
xcopy /E /I /Y "%OUTPUT_DIR%\*" "%DIST_DIR%\"

REM Crear documentación de la build
echo.
echo Generando información de build...
echo FindingExcellence Build Info > "%DIST_DIR%\BUILD_INFO.txt"
echo ========================== >> "%DIST_DIR%\BUILD_INFO.txt"
echo Build Date: %DATE% %TIME% >> "%DIST_DIR%\BUILD_INFO.txt"
echo Python Version: >> "%DIST_DIR%\BUILD_INFO.txt"
python --version >> "%DIST_DIR%\BUILD_INFO.txt" 2>&1
echo. >> "%DIST_DIR%\BUILD_INFO.txt"
echo Installed Packages: >> "%DIST_DIR%\BUILD_INFO.txt"
python -m pip list >> "%DIST_DIR%\BUILD_INFO.txt"

REM Crear README para distribución
echo.
echo Creando README...
echo FindingExcellence - Excel File Search Tool > "%DIST_DIR%\README.txt"
echo ============================================== >> "%DIST_DIR%\README.txt"
echo. >> "%DIST_DIR%\README.txt"
echo USAGE: >> "%DIST_DIR%\README.txt"
echo   Double-click FindingExcellence.exe to run >> "%DIST_DIR%\README.txt"
echo. >> "%DIST_DIR%\README.txt"
echo SYSTEM REQUIREMENTS: >> "%DIST_DIR%\README.txt"
echo   - Windows 7 SP1 or later >> "%DIST_DIR%\README.txt"
echo   - 64-bit operating system >> "%DIST_DIR%\README.txt"
echo   - 100MB free disk space >> "%DIST_DIR%\README.txt"
echo. >> "%DIST_DIR%\README.txt"
echo The application searches Excel files in Desktop and Downloads folders. >> "%DIST_DIR%\README.txt"
echo No installation required - this is a portable application. >> "%DIST_DIR%\README.txt"
echo. >> "%DIST_DIR%\README.txt"
echo Built with isolated environment on: %DATE% >> "%DIST_DIR%\README.txt"

echo.
echo ===============================================
echo ✓ BUILD COMPLETADO EXITOSAMENTE
echo ===============================================
echo.
echo Archivos generados:
echo   📁 Ejecutable: %DIST_DIR%\FindingExcellence.exe
echo   📄 README: %DIST_DIR%\README.txt  
echo   📄 Build Info: %DIST_DIR%\BUILD_INFO.txt
echo.
echo El ejecutable fue creado con un entorno aislado.
echo Las versiones están garantizadas y no cambiarán.
echo.
echo ¡Listo para distribución!
echo.
pause

REM Desactivar entorno virtual
deactivate
