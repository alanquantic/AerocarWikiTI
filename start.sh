#!/bin/bash

# Script de inicio rápido para AerocarWiki

echo "🚀 Iniciando AerocarWiki..."
echo ""

# Activar entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias si es necesario
if ! command -v mkdocs &> /dev/null; then
    echo "📚 Instalando dependencias..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Servidor listo!"
echo "📖 Abre tu navegador en: http://127.0.0.1:8000"
echo "⏹️  Presiona Ctrl+C para detener el servidor"
echo ""

# Iniciar servidor
mkdocs serve

