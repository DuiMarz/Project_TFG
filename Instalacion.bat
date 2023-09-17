@echo off

rem Obtener la ubicación del directorio del script actual
for %%i in ("%~dp0.") do set "SCRIPT_DIR=%%~fi"

rem Crear un nuevo entorno virtual en el mismo directorio
python -m venv "%SCRIPT_DIR%"

rem Activar el entorno virtual
call "%SCRIPT_DIR%\Scripts\activate"

rem Instalar dependencias desde el archivo requirements.txt
pip install -r "%SCRIPT_DIR%\requirements.txt"

echo Entorno virtual creado y dependencias instaladas.

rem Ejecutar tu aplicación, si es necesario
python "%SCRIPT_DIR%\GUI.py"

rem Desactivar el entorno virtual al finalizar
deactivate