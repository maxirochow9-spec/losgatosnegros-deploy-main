@echo off
REM Instalación rápida de Los Gatos Negros - Windows

echo ========================================
echo Los Gatos Negros - Instalación Rápida
echo ========================================
echo.

REM 1. Crear entorno virtual
echo [1/5] Creando entorno virtual...
python -m venv venv
if errorlevel 1 goto error

REM 2. Activar entorno virtual
echo [2/5] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 goto error

REM 3. Instalar dependencias
echo [3/5] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 goto error

REM 4. Aplicar migraciones
echo [4/5] Aplicando migraciones...
python manage.py migrate
if errorlevel 1 goto error

REM 5. Ejecutar servidor
echo [5/5] Iniciando servidor...
echo.
echo ========================================
echo Servidor iniciado en: http://localhost:8000
echo ========================================
echo.
python manage.py runserver
goto end

:error
echo.
echo ERROR: Algo salió mal durante la instalación.
echo Por favor, verifica los mensajes de error arriba.
pause
exit /b 1

:end
pause
