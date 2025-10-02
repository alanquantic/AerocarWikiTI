#!/usr/bin/env python3
"""
Script para convertir archivos Markdown de Obsidian a formato MkDocs Material.
Maneja enlaces [[wikilinks]], frontmatter YAML, y estructura de carpetas.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List


class ObsidianToMkDocsConverter:
    def __init__(self, source_dir: str, output_dir: str):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.file_map: Dict[str, str] = {}  # Mapa de títulos a rutas
        
    def normalize_filename(self, filename: str) -> str:
        """Convierte nombre de archivo a formato URL-friendly."""
        # Remover _ al inicio
        name = filename.replace('_', '')
        # Convertir a minúsculas y reemplazar espacios
        name = name.lower()
        name = name.replace(' ', '-')
        # Remover caracteres especiales
        name = re.sub(r'[^\w\-.]', '', name)
        return name
    
    def normalize_path(self, path: str) -> str:
        """Normaliza rutas de carpetas."""
        return path.lower().replace(' ', '-')
    
    def extract_title(self, content: str, filename: str) -> str:
        """Extrae el título del archivo."""
        # Buscar título H1
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        
        # Si no hay H1, usar el nombre del archivo sin extensión
        return filename.replace('_', '').replace('.md', '').strip()
    
    def build_file_map(self):
        """Construye un mapa de todos los archivos MD y sus rutas relativas."""
        print("📋 Construyendo mapa de archivos...")
        
        for md_file in self.source_dir.rglob('*.md'):
            if md_file.is_file():
                # Leer contenido para extraer título
                try:
                    content = md_file.read_text(encoding='utf-8')
                    title = self.extract_title(content, md_file.stem)
                    
                    # Calcular ruta relativa
                    rel_path = md_file.relative_to(self.source_dir)
                    
                    # Normalizar la ruta de salida
                    parts = list(rel_path.parts)
                    normalized_parts = [self.normalize_path(p) if i < len(parts) - 1 
                                      else self.normalize_filename(p) 
                                      for i, p in enumerate(parts)]
                    
                    new_rel_path = '/'.join(normalized_parts)
                    
                    # Guardar en el mapa con múltiples claves
                    self.file_map[title] = new_rel_path
                    self.file_map[md_file.stem] = new_rel_path
                    self.file_map[md_file.stem.replace('_', '')] = new_rel_path
                    
                except Exception as e:
                    print(f"⚠️  Error procesando {md_file}: {e}")
        
        print(f"✅ Se encontraron {len(set(self.file_map.values()))} archivos únicos")
    
    def convert_wikilinks(self, content: str, current_file_path: str) -> str:
        """Convierte [[wikilinks]] de Obsidian a enlaces Markdown estándar."""
        
        def replace_link(match):
            link_text = match.group(1)
            display_text = link_text
            
            # Manejar [[link|display text]]
            if '|' in link_text:
                link_text, display_text = link_text.split('|', 1)
            
            link_text = link_text.strip()
            display_text = display_text.strip()
            
            # Buscar el archivo en el mapa
            if link_text in self.file_map:
                target_path = self.file_map[link_text]
                
                # Calcular ruta relativa desde el archivo actual
                current_dir = str(Path(current_file_path).parent)
                if current_dir == '.':
                    relative_path = target_path
                else:
                    # Contar niveles hacia arriba
                    levels_up = len(Path(current_dir).parts)
                    prefix = '../' * levels_up
                    relative_path = prefix + target_path
                
                return f"[{display_text}]({relative_path})"
            else:
                # Si no se encuentra, dejar como texto
                return f"**{display_text}**"
        
        # Convertir todos los wikilinks
        content = re.sub(r'\[\[([^\]]+)\]\]', replace_link, content)
        return content
    
    def process_frontmatter(self, content: str) -> tuple:
        """Procesa el frontmatter YAML y devuelve (frontmatter, contenido)."""
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(frontmatter_pattern, content, re.DOTALL)
        
        if match:
            frontmatter = match.group(1)
            content_without_fm = content[match.end():]
            return frontmatter, content_without_fm
        
        return '', content
    
    def convert_file(self, source_file: Path):
        """Convierte un archivo individual de Obsidian a MkDocs."""
        try:
            # Leer contenido
            content = source_file.read_text(encoding='utf-8')
            
            # Procesar frontmatter
            frontmatter, content = self.process_frontmatter(content)
            
            # Calcular ruta de salida
            rel_path = source_file.relative_to(self.source_dir)
            parts = list(rel_path.parts)
            normalized_parts = [self.normalize_path(p) if i < len(parts) - 1 
                              else self.normalize_filename(p) 
                              for i, p in enumerate(parts)]
            
            output_path = self.output_dir / Path(*normalized_parts)
            
            # Convertir wikilinks
            content = self.convert_wikilinks(content, str(Path(*normalized_parts)))
            
            # Asegurar que hay un título H1
            if not re.search(r'^#\s+', content, re.MULTILINE):
                title = self.extract_title(content, source_file.stem)
                content = f"# {title}\n\n{content}"
            
            # Reconstruir el archivo
            if frontmatter:
                final_content = f"---\n{frontmatter}\n---\n\n{content}"
            else:
                final_content = content
            
            # Crear directorio de salida
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Escribir archivo
            output_path.write_text(final_content, encoding='utf-8')
            
            print(f"✅ {source_file.name} → {output_path.relative_to(self.output_dir)}")
            
        except Exception as e:
            print(f"❌ Error convirtiendo {source_file}: {e}")
    
    def create_index_files(self):
        """Crea archivos index.md para cada sección."""
        sections = {
            'automatizacion': 'Automatización',
            'aerolink': 'AeroLink',
            'gobernanza': 'Gobernanza',
            'ciberseguridad': 'Ciberseguridad',
            'infraestructura': 'Infraestructura'
        }
        
        for folder, title in sections.items():
            index_path = self.output_dir / folder / 'index.md'
            index_path.parent.mkdir(parents=True, exist_ok=True)
            
            content = f"""# {title}

Bienvenido a la sección de **{title}**.

Navega por las diferentes categorías usando el menú lateral.
"""
            index_path.write_text(content, encoding='utf-8')
            print(f"📄 Creado {index_path.relative_to(self.output_dir)}")
    
    def create_main_index(self):
        """Crea el index.md principal."""
        index_path = self.output_dir / 'index.md'
        
        content = """# AerocarWiki TI

Bienvenido a la wiki del departamento de TI de Aerocar.

## 📚 Secciones

### 🤖 Automatización
Proyectos de automatización de procesos empresariales.

- **Pagos**: Gestión y seguimiento de pagos
- **Cobranza**: Procesos de facturación
- **Ventas**: Análisis y alta de clientes

### ✈️ AeroLink
Sistema integral de gestión logística y operativa.

- **Comercial**: Herramientas de cotización y seguimiento
- **Logística**: Seguimiento aéreo y terrestre
- **Contabilidad**: Procesos contables

### 🔐 Gobernanza
Implementación de políticas y herramientas de gobierno de TI.

### 🛡️ Ciberseguridad
Capacitación, monitoreo y optimización de seguridad.

### 🏗️ Infraestructura
Proyectos de infraestructura tecnológica.

---

💡 **Tip**: Usa la búsqueda (presiona `/`) para encontrar rápidamente cualquier proyecto.
"""
        
        index_path.write_text(content, encoding='utf-8')
        print(f"📄 Creado {index_path.relative_to(self.output_dir)}")
    
    def create_tags_page(self):
        """Crea la página de tags."""
        tags_path = self.output_dir / 'tags.md'
        
        content = """# Tags

Esta página muestra todos los tags utilizados en la wiki.

[TAGS]
"""
        
        tags_path.write_text(content, encoding='utf-8')
        print(f"📄 Creado {tags_path.relative_to(self.output_dir)}")
    
    def convert_all(self):
        """Ejecuta la conversión completa."""
        print("🚀 Iniciando conversión de Obsidian a MkDocs...\n")
        
        # Limpiar directorio de salida
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Construir mapa de archivos
        self.build_file_map()
        print()
        
        # Convertir archivos
        print("📝 Convirtiendo archivos...")
        for md_file in self.source_dir.rglob('*.md'):
            if md_file.is_file():
                self.convert_file(md_file)
        print()
        
        # Crear archivos especiales
        print("📋 Creando archivos especiales...")
        self.create_main_index()
        self.create_index_files()
        self.create_tags_page()
        print()
        
        # Copiar assets si existen
        if (self.source_dir / 'assets').exists():
            print("🖼️  Copiando assets...")
            shutil.copytree(
                self.source_dir / 'assets',
                self.output_dir / 'assets',
                dirs_exist_ok=True
            )
        
        print("✨ ¡Conversión completada exitosamente!")


def main():
    """Función principal."""
    # Rutas
    source_dir = "Proyectos 2"
    output_dir = "docs"
    
    # Convertir
    converter = ObsidianToMkDocsConverter(source_dir, output_dir)
    converter.convert_all()


if __name__ == "__main__":
    main()

