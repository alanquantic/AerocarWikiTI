# 🎉 ¡Tu AerocarWiki está lista!

## 🌐 Ver tu Wiki Ahora

**Tu wiki ya está corriendo en:** 
```
http://127.0.0.1:8000
```

Ábrela en tu navegador para verla en acción.

---

## 📋 Próximos Pasos

### 1️⃣ Publicar en GitHub (Primera vez)

```bash
# Inicializar Git (si aún no está hecho)
git init
git add .
git commit -m "🎉 AerocarWiki inicial con MkDocs Material"

# Conectar con GitHub
git branch -M main
git remote add origin git@github.com:alanquantic/AerocarWikiTI.git
git push -u origin main
```

### 2️⃣ Habilitar GitHub Pages

1. Ve a tu repositorio en GitHub: https://github.com/alanquantic/AerocarWikiTI
2. Click en **Settings** (Configuración)
3. En el menú lateral, click en **Pages**
4. En **Source**, selecciona: **Deploy from a branch**
5. En **Branch**, selecciona: **gh-pages** / **(root)**
6. Click en **Save**

**¡Listo!** En 1-2 minutos tu wiki estará disponible en:
```
https://alanquantic.github.io/AerocarWikiTI/
```

---

## 🔄 Workflow de Trabajo

### Opción A: Editar archivos directamente en `docs/`

```bash
# 1. Edita archivos en la carpeta docs/
# 2. Los cambios se reflejan automáticamente en http://127.0.0.1:8000

# 3. Cuando estés listo, despliega:
./deploy.sh
```

### Opción B: Editar en Obsidian (Gratis) y reconvertir

```bash
# 1. Edita tus archivos en "Proyectos 2/" usando Obsidian
# 2. Reconvierte a MkDocs:
python3 convert_obsidian_to_mkdocs.py

# 3. Despliega:
./deploy.sh
```

---

## 🛠️ Comandos Útiles

### Iniciar el servidor local
```bash
./start.sh
# O manualmente:
source venv/bin/activate
mkdocs serve
```

### Desplegar a GitHub Pages
```bash
./deploy.sh
```

### Reconvertir archivos de Obsidian
```bash
python3 convert_obsidian_to_mkdocs.py
```

### Construir sitio estático
```bash
source venv/bin/activate
mkdocs build
```

---

## 📤 Exportar a Notion

Tus archivos Markdown son 100% compatibles con Notion:

1. Abre **Notion**
2. Crea una **nueva página** o selecciona una existente
3. Click en el menú **(...)**  → **Import**
4. Selecciona **"Markdown & CSV"**
5. Sube archivos de la carpeta **`docs/`**

✅ Notion importará todo con el formato correcto.

---

## 🎨 Personalización

### Cambiar colores

Edita `mkdocs.yml` líneas 11-12:

```yaml
theme:
  palette:
    - scheme: default
      primary: blue      # ← Cambia este
      accent: indigo     # ← Y este
```

**Colores disponibles:** `red`, `pink`, `purple`, `indigo`, `blue`, `cyan`, `teal`, `green`, `amber`, `orange`

### Agregar logo

1. Coloca tu logo en `docs/assets/logo.png`
2. En `mkdocs.yml`, agrega:
```yaml
theme:
  logo: assets/logo.png
```

### Estilos personalizados

Edita `docs/stylesheets/extra.css`

---

## 📁 Estructura del Proyecto

```
AerocarWikiTI/
├── docs/                    ← Archivos Markdown convertidos
│   ├── index.md            ← Página principal
│   ├── automatizacion/
│   ├── aerolink/
│   ├── ciberseguridad/
│   ├── gobernanza/
│   └── infraestructura/
│
├── Proyectos 2/            ← Archivos originales de Obsidian
│
├── mkdocs.yml              ← Configuración de MkDocs
├── requirements.txt        ← Dependencias Python
│
├── convert_obsidian_to_mkdocs.py  ← Script de conversión
├── start.sh                       ← Iniciar servidor (rápido)
├── deploy.sh                      ← Desplegar a GitHub
│
└── README.md               ← Documentación completa
```

---

## 🔍 Características

✅ **Búsqueda avanzada** - Presiona `/` en cualquier momento  
✅ **Modo oscuro/claro** - Toggle en la esquina superior  
✅ **Responsive** - Funciona perfecto en móvil  
✅ **Navegación por pestañas** - Organización intuitiva  
✅ **Deploy automático** - GitHub Actions configurado  
✅ **Compatible con Notion** - Importa/exporta fácilmente  

---

## ❓ FAQ

**¿Tengo que pagar por Obsidian?**  
No, Obsidian es gratis para uso personal. Solo pagas si quieres Obsidian Publish (que no necesitas porque usas GitHub Pages gratis).

**¿Cómo agrego un nuevo proyecto?**  
1. Crea el archivo `.md` en `Proyectos 2/[Categoría]/`
2. Ejecuta `python3 convert_obsidian_to_mkdocs.py`
3. Ejecuta `./deploy.sh`

**¿Los enlaces [[wikilinks]] funcionan?**  
Sí, el script los convierte automáticamente a enlaces Markdown estándar.

**¿Puedo usar diagramas?**  
Sí, MkDocs Material soporta diagramas Mermaid, tablas, código con highlighting, etc.

---

## 🎯 Hecho

✅ Wiki profesional con MkDocs Material  
✅ 29 archivos convertidos de Obsidian  
✅ Navegación organizada por categorías  
✅ Búsqueda en español integrada  
✅ GitHub Actions para deploy automático  
✅ Scripts de utilidad (`start.sh`, `deploy.sh`)  
✅ Compatible con Notion para importar/exportar  
✅ Modo oscuro/claro  
✅ Responsive design  

---

**🚀 ¡Disfruta tu nueva wiki!**

Si tienes dudas, revisa el `README.md` completo o contacta al equipo de TI.

