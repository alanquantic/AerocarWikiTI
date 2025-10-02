#!/bin/bash

# Script para desplegar a GitHub Pages

echo "🚀 Preparando despliegue de AerocarWiki..."
echo ""

# Verificar si hay cambios sin commit
if [[ -n $(git status -s) ]]; then
    echo "⚠️  Hay cambios sin commit. Por favor, haz commit antes de desplegar."
    echo ""
    git status -s
    echo ""
    read -p "¿Quieres hacer commit ahora? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        read -p "Mensaje del commit: " commit_msg
        git add .
        git commit -m "$commit_msg"
    else
        echo "❌ Despliegue cancelado."
        exit 1
    fi
fi

echo "📦 Construyendo sitio..."
source venv/bin/activate
mkdocs build --clean --strict

if [ $? -eq 0 ]; then
    echo "✅ Sitio construido exitosamente!"
    echo ""
    echo "📤 Haciendo push a GitHub..."
    git push origin main
    
    echo ""
    echo "⏳ Espera 1-2 minutos para que GitHub Actions despliegue tu sitio."
    echo "🌐 Tu wiki estará disponible en: https://alanquantic.github.io/AerocarWikiTI/"
else
    echo "❌ Error al construir el sitio. Revisa los mensajes de error arriba."
    exit 1
fi

