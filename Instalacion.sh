#!/bin/bash

# Ruta al directorio donde se encuentra este script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Crear un nuevo entorno virtual
python3 -m venv "$SCRIPT_DIR"

# Activar el entorno virtual
source "$SCRIPT_DIR/bin/activate"

# Instalar dependencias desde el archivo requirements.txt
pip install -r "$SCRIPT_DIR/requirements.txt"

echo "Entorno virtual creado y dependencias instaladas."

# Ejecutar tu aplicación, si es necesario
# python "$SCRIPT_DIR/main.py"

# Desactivar el entorno virtual al finalizar
deactivate