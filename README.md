# 📚 AerocarWiki TI

Wiki profesional del departamento de TI de Aerocar, construida con **MkDocs Material**.

## 🌟 Características

- ✅ **Diseño profesional y moderno** con tema Material Design
- ✅ **Modo oscuro/claro** configurable
- ✅ **Búsqueda integrada** con sugerencias
- ✅ **Navegación por pestañas** y menú lateral
- ✅ **Responsive** - funciona perfecto en móvil
- ✅ **Compatible con Notion** - los archivos MD se pueden importar fácilmente
- ✅ **GitHub Pages** - deploy automático gratis
- ✅ **Conversión automática** desde Obsidian

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.8 o superior
- Git

### Instalación

1. **Clonar el repositorio:**
```bash
git clone git@github.com:alanquantic/AerocarWikiTI.git
cd AerocarWikiTI
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Convertir archivos de Obsidian a MkDocs:**
```bash
python convert_obsidian_to_mkdocs.py
```

4. **Ejecutar servidor local:**
```bash
mkdocs serve
```

5. **Abrir en navegador:**
```
http://127.0.0.1:8000
```

## 📝 Agregar o Editar Contenido

### Opción 1: Editar directamente en `docs/`

1. Edita archivos en la carpeta `docs/`
2. Los cambios se reflejarán automáticamente si tienes `mkdocs serve` corriendo

### Opción 2: Editar en Obsidian y reconvertir

1. Edita tus archivos en la carpeta `Proyectos 2/` con Obsidian (gratis)
2. Ejecuta el script de conversión:
```bash
python convert_obsidian_to_mkdocs.py
```

## 🌐 Deploy a GitHub Pages

### Configuración Inicial (una sola vez)

1. **Crear repositorio en GitHub:**
```bash
git init
git add .
git commit -m "Initial commit: AerocarWiki"
git branch -M main
git remote add origin git@github.com:alanquantic/AerocarWikiTI.git
git push -u origin main
```

2. **Habilitar GitHub Pages:**
   - Ve a tu repositorio en GitHub
   - Settings → Pages
   - Source: **Deploy from a branch**
   - Branch: **gh-pages** / **(root)**
   - Guarda los cambios

3. **El deploy automático ya está configurado** mediante GitHub Actions (`.github/workflows/deploy.yml`)

### Publicar Cambios

Cada vez que hagas push a `main`, se desplegará automáticamente:

```bash
# 1. Convertir archivos si editaste en Obsidian
python convert_obsidian_to_mkdocs.py

# 2. Hacer commit y push
git add .
git commit -m "Actualización de contenido"
git push origin main
```

Espera 1-2 minutos y tu wiki estará actualizada en:
```
https://alanquantic.github.io/AerocarWikiTI/
```

## 📤 Exportar a Notion

Los archivos Markdown en `docs/` son 100% compatibles con Notion:

1. **Abrir Notion**
2. **Crear una nueva página** o seleccionar una existente
3. **Menú (···) → Import**
4. **Seleccionar "Markdown & CSV"**
5. **Subir archivos** de la carpeta `docs/`

Notion importará todo el contenido con el formato correcto.

## 📂 Estructura del Proyecto

```
AerocarWikiTI/
├── docs/                          # Archivos MD convertidos (MkDocs)
│   ├── index.md                  # Página principal
│   ├── indice-proyectos.md       # Índice general
│   ├── automatizacion/           # Sección Automatización
│   ├── aerolink/                 # Sección AeroLink
│   ├── ciberseguridad/          # Sección Ciberseguridad
│   ├── gobernanza/              # Sección Gobernanza
│   ├── infraestructura/         # Sección Infraestructura
│   └── stylesheets/
│       └── extra.css            # Estilos personalizados
├── Proyectos 2/                  # Archivos originales de Obsidian
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions para deploy automático
├── mkdocs.yml                    # Configuración de MkDocs
├── requirements.txt              # Dependencias Python
├── convert_obsidian_to_mkdocs.py # Script de conversión
└── README.md                     # Este archivo
```

## 🛠️ Comandos Útiles

```bash
# Servidor local con recarga automática
mkdocs serve

# Servidor accesible desde otros dispositivos en la red
mkdocs serve -a 0.0.0.0:8000

# Construir sitio estático
mkdocs build

# Deploy manual a GitHub Pages (no necesario con Actions)
mkdocs gh-deploy

# Limpiar archivos generados
rm -rf site/
```

## 🎨 Personalización

### Cambiar Colores

Edita `mkdocs.yml`:

```yaml
theme:
  palette:
    primary: indigo    # Cambiar color principal
    accent: blue       # Cambiar color de acento
```

Colores disponibles: `red`, `pink`, `purple`, `deep-purple`, `indigo`, `blue`, `light-blue`, `cyan`, `teal`, `green`, `light-green`, `lime`, `yellow`, `amber`, `orange`, `deep-orange`

### Cambiar Logo

1. Agrega tu logo en `docs/assets/logo.png`
2. En `mkdocs.yml`:
```yaml
theme:
  logo: assets/logo.png
```

### CSS Personalizado

Edita `docs/stylesheets/extra.css` para ajustar estilos.

## 🔍 Búsqueda Avanzada

- Presiona `/` para abrir búsqueda rápida
- Búsqueda en español con separación inteligente
- Sugerencias automáticas mientras escribes
- Resaltado de resultados

## 📱 Características Mobile

- Navegación tipo hamburger
- Tabla de contenidos colapsable
- Búsqueda optimizada
- Interfaz táctil

## ❓ FAQ

### ¿Puedo usar Obsidian gratuitamente para editar?

Sí, Obsidian es gratis para uso personal. Solo es de pago su servicio de publicación (Obsidian Publish), pero aquí usamos GitHub Pages que es gratis.

### ¿Cómo agrego un nuevo proyecto?

1. Crea el archivo MD en `Proyectos 2/[Categoría]/`
2. Ejecuta `python convert_obsidian_to_mkdocs.py`
3. Actualiza la navegación en `mkdocs.yml` si quieres
4. Haz commit y push

### ¿Los enlaces entre páginas funcionan?

Sí, el script convierte automáticamente los `[[wikilinks]]` de Obsidian a enlaces MD estándar.

### ¿Puedo usar diagramas?

Sí, MkDocs Material soporta:
- Diagramas Mermaid
- Bloques de código con sintaxis highlighting
- Tablas
- Imágenes

## 📞 Soporte

Para dudas o problemas, contacta al equipo de TI de Aerocar.

## 📄 Licencia

© 2025 Aerocar - Departamento de TI. Todos los derechos reservados.

---

**🎯 Hecho con ❤️ usando MkDocs Material**

