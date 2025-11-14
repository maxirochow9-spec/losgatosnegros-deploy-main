#!/bin/bash

# Instalación rápida de Los Gatos Negros - Linux/macOS

echo "========================================"
echo "Los Gatos Negros - Instalación Rápida"
echo "========================================"
echo ""

# 1. Crear entorno virtual
echo "[1/5] Creando entorno virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo crear el entorno virtual"
    exit 1
fi

# 2. Activar entorno virtual
echo "[2/5] Activando entorno virtual..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo activar el entorno virtual"
    exit 1
fi

# 3. Instalar dependencias
echo "[3/5] Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi

# 4. Aplicar migraciones
echo "[4/5] Aplicando migraciones..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron aplicar las migraciones"
    exit 1
fi

# 5. Ejecutar servidor
echo "[5/5] Iniciando servidor..."
echo ""
echo "========================================"
echo "Servidor iniciado en: http://localhost:8000"
echo "========================================"
echo ""
python manage.py runserver
