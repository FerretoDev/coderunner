#!/bin/bash

# Script de inicio rápido para Theseus Runner Asset Generator

echo "==========================================="
echo "  THESEUS RUNNER - INICIO RÁPIDO"
echo "==========================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instálalo primero."
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"

# Instalar dependencias
echo ""
echo "📦 Instalando dependencias..."
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error al instalar dependencias"
    exit 1
fi

echo "✓ Dependencias instaladas"

# Generar assets
echo ""
echo "🎨 Generando assets pixel art..."
python3 generate_all.py --scale 2

if [ $? -ne 0 ]; then
    echo "❌ Error al generar assets"
    exit 1
fi

echo ""
echo "==========================================="
echo "✓ ¡TODO LISTO!"
echo "==========================================="
echo ""
echo "Assets generados en: assets/"
echo ""
echo "Opciones disponibles:"
echo "  1. Ver demo:           python3 demo.py"
echo "  2. Regenerar assets:   python3 generate_all.py --scale 2"
echo "  3. Paleta nocturna:    python3 generate_all.py --palette night"
echo "  4. Ver documentación:  cat README.md"
echo ""
