# 📊 Sincronización con Notion - Guía de Configuración

Esta guía te ayudará a sincronizar automáticamente tus proyectos de AerocarWiki a Notion.

## 📋 Requisitos Previos

Tu base de datos de Notion debe tener estas **2 propiedades** (tal como las tienes):

| Propiedad | Tipo en Notion | Descripción |
|-----------|----------------|-------------|
| **Nombre del Proyecto** | Title | Título del proyecto |
| **Descripción** | Text | Descripción general del proyecto |

✅ Ya tienes el cliente "AEROCAR" configurado, así que solo necesitas estas dos propiedades.

---

## 🔧 Configuración Paso a Paso

### Paso 1: Crear Integración de Notion

1. Ve a: **https://www.notion.so/my-integrations**
2. Click en **"+ New integration"**
3. Configura:
   - **Name:** AerocarWiki Sync
   - **Associated workspace:** Tu workspace de Notion
   - **Type:** Internal Integration
   - **Capabilities:**
     - ✅ Read content
     - ✅ Update content
     - ✅ Insert content
4. Click en **"Submit"**
5. **Copia el token** que aparece (empieza con `secret_...`)

### Paso 2: Conectar la Base de Datos

1. Abre tu base de datos "Proyectos IA AEROCAR" en Notion
2. Click en los **tres puntos (···)** en la esquina superior derecha
3. Scroll hasta abajo y click en **"+ Add connections"**
4. Busca y selecciona **"AerocarWiki Sync"**
5. Click en **"Confirm"**

### Paso 3: Obtener el ID de la Base de Datos

**Opción A - Desde la URL:**

Tu URL de Notion es algo como:
```
https://notion.so/2809c2c6ea0780a8b4ed38fc16d7600?v=2809c2c6ea07...
```

El ID de la base de datos es la parte antes del `?v=`:
```
2809c2c6ea0780a8b4ed38fc16d7600
```

**Opción B - Copiar link:**

1. Click en los **tres puntos (···)** de tu base de datos
2. Click en **"Copy link to database"**
3. El ID está entre `.so/` y `?v=`

### Paso 4: Configurar Variables de Entorno

1. Crea un archivo `.env` en la raíz del proyecto:

```bash
# Desde la terminal en la carpeta del proyecto
cp env.example .env
```

2. Edita el archivo `.env` con tus datos:

```bash
# Token de integración de Notion (del Paso 1)
NOTION_TOKEN=secret_tu_token_aqui

# ID de la base de datos (del Paso 3)
NOTION_DATABASE_ID=2809c2c6ea0780a8b4ed38fc16d7600
```

⚠️ **IMPORTANTE:** El archivo `.env` está en `.gitignore` por seguridad. **NUNCA** lo subas a Git.

### Paso 5: Instalar Dependencias

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar nuevas dependencias
pip install -r requirements.txt
```

---

## 🚀 Uso

### Sincronizar Todos los Proyectos

```bash
# Desde la raíz del proyecto
python3 sync_to_notion.py
```

El script:
- ✅ Lee todos los archivos `.md` de la carpeta `docs/`
- ✅ Extrae el **Nombre del Proyecto** y la **Descripción**
- ✅ Crea páginas nuevas si no existen
- ✅ Actualiza páginas existentes (compara por nombre)
- ✅ Muestra progreso en tiempo real

### Salida Esperada

```
🚀 Iniciando sincronización con Notion...

✅ Base de datos de Notion configurada correctamente

📁 Proyectos encontrados: 29

✅ Creado: Calculadora de Carga Aérea
✅ Creado: Implementación de API de Clima
✅ Actualizado: Registro de Vuelos por Proyecto
...

✨ Sincronización completada: 29/29 proyectos
```

---

## 🔄 Automatizar Sincronización

### Opción 1: Script Manual

Crea un script `sync_and_deploy.sh`:

```bash
#!/bin/bash

echo "🔄 Sincronizando con Notion..."
python3 sync_to_notion.py

if [ $? -eq 0 ]; then
    echo "✅ Sincronización exitosa"
    echo ""
    echo "📤 ¿Desplegar a GitHub Pages? (s/n)"
    read -r response
    if [[ "$response" =~ ^[Ss]$ ]]; then
        ./deploy.sh
    fi
else
    echo "❌ Error en sincronización"
    exit 1
fi
```

Luego usa:
```bash
chmod +x sync_and_deploy.sh
./sync_and_deploy.sh
```

### Opción 2: GitHub Actions (Automático)

Puedes configurar GitHub Actions para sincronizar automáticamente cada vez que hagas push.

---

## 🛠️ Verificación y Solución de Problemas

### Verificar Propiedades de Notion

El script automáticamente verifica las propiedades. Si hay un error, verás:

```
❌ Propiedades faltantes en Notion: Descripción

📋 Propiedades actuales en tu base de datos:
   - Nombre del Proyecto: title
   - Estado: select
   - Prioridad: select
```

**Solución:** Agrega la propiedad faltante en Notion.

### Error: "NOTION_TOKEN no está configurado"

- Verifica que el archivo `.env` existe
- Verifica que `NOTION_TOKEN` está correctamente escrito
- El token debe empezar con `secret_`

### Error: "not authorized"

- Verifica que agregaste la integración a tu base de datos (Paso 2)
- Verifica que los permisos de la integración incluyen Read, Update, Insert

### Proyectos No Aparecen

El script ignora estos archivos especiales:
- `index.md`
- `tags.md`
- `indice-de-proyectos.md`

---

## 📊 Estructura de Datos

El script extrae:

```markdown
# Nombre del Proyecto    ← Se usa como "Nombre del Proyecto"

## Requerimientos:
### Descripción General
Se requiere crear...   ← Se usa como "Descripción"
```

---

## 🔒 Seguridad

✅ El archivo `.env` está en `.gitignore`  
✅ Nunca compartas tu `NOTION_TOKEN`  
✅ Si expones el token accidentalmente, revócalo inmediatamente en https://www.notion.so/my-integrations  

---

## 💡 Tips

1. **Prueba primero con pocos proyectos:** Comenta algunos archivos para probar
2. **Backup de Notion:** Haz un backup antes de la primera sincronización
3. **Nombres únicos:** Asegúrate de que no haya proyectos con el mismo nombre
4. **Límite de caracteres:** La descripción se trunca a 2000 caracteres (límite de Notion)

---

## ❓ Preguntas Frecuentes

**¿Qué pasa si edito en Notion?**
- Los cambios en Notion se sobrescribirán en la próxima sincronización
- La wiki es la "fuente de verdad"

**¿Puedo sincronizar solo algunos proyectos?**
- Sí, modifica el script para filtrar por carpeta o nombre

**¿Se eliminarán proyectos de Notion?**
- No, el script solo crea y actualiza, nunca elimina

---

**🎯 ¿Necesitas ayuda?** Contacta al equipo de TI de Aerocar.

