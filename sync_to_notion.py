#!/usr/bin/env python3
"""
Script para sincronizar proyectos de AerocarWiki a Notion.
Sincroniza: Nombre del proyecto y Descripción.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class NotionSync:
    def __init__(self):
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.database_id = os.getenv('NOTION_DATABASE_ID')
        
        if not self.notion_token:
            raise ValueError("❌ NOTION_TOKEN no está configurado en .env")
        if not self.database_id:
            raise ValueError("❌ NOTION_DATABASE_ID no está configurado en .env")
        
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.base_url = "https://api.notion.com/v1"
    
    def extract_project_info(self, md_file: Path) -> Optional[Dict]:
        """Extrae nombre y descripción de un archivo MD."""
        try:
            content = md_file.read_text(encoding='utf-8')
            
            # Extraer título (primera línea con #)
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if not title_match:
                return None
            
            title = title_match.group(1).strip()
            # Limpiar caracteres especiales del título
            title = title.replace('_', '').strip()
            
            # Extraer descripción general
            desc_match = re.search(
                r'###\s+Descripción General\s*\n(.+?)(?:\n###|\n##|\Z)', 
                content, 
                re.DOTALL
            )
            
            description = ""
            if desc_match:
                description = desc_match.group(1).strip()
                # Limpiar la descripción
                description = re.sub(r'\n+', ' ', description)
                description = description.strip()
            
            # Si no hay descripción, usar un texto por defecto
            if not description:
                description = "Proyecto de TI - Aerocar"
            
            return {
                'title': title,
                'description': description,
                'file_path': str(md_file.relative_to(Path('docs')))
            }
        
        except Exception as e:
            print(f"⚠️  Error procesando {md_file.name}: {e}")
            return None
    
    def get_all_projects(self) -> List[Dict]:
        """Escanea todos los archivos MD y extrae la información."""
        projects = []
        docs_path = Path('docs')
        
        # Excluir archivos especiales
        exclude_files = {'index.md', 'tags.md', 'indice-de-proyectos.md'}
        
        for md_file in docs_path.rglob('*.md'):
            if md_file.name in exclude_files:
                continue
            
            project_info = self.extract_project_info(md_file)
            if project_info:
                projects.append(project_info)
        
        return projects
    
    def check_database_properties(self) -> bool:
        """Verifica que la base de datos tenga las propiedades correctas."""
        try:
            url = f"{self.base_url}/databases/{self.database_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            properties = data.get('properties', {})
            
            # Verificar propiedades requeridas
            required_props = {
                'Nombre del Proyecto': ['title'],
                'Descripción': ['rich_text'],
            }
            
            missing = []
            for prop_name, prop_types in required_props.items():
                if prop_name not in properties:
                    missing.append(prop_name)
                    continue
                
                prop_type = properties[prop_name].get('type')
                if prop_type not in prop_types:
                    print(f"⚠️  '{prop_name}' existe pero es tipo '{prop_type}' (esperado: {prop_types})")
            
            if missing:
                print(f"❌ Propiedades faltantes en Notion: {', '.join(missing)}")
                print("\n📋 Propiedades actuales en tu base de datos:")
                for name, prop in properties.items():
                    print(f"   - {name}: {prop.get('type')}")
                return False
            
            print("✅ Base de datos de Notion configurada correctamente")
            return True
        
        except Exception as e:
            print(f"❌ Error verificando base de datos: {e}")
            return False
    
    def project_exists(self, project_title: str) -> Optional[str]:
        """Verifica si un proyecto ya existe en Notion."""
        try:
            url = f"{self.base_url}/databases/{self.database_id}/query"
            
            payload = {
                "filter": {
                    "property": "Nombre del Proyecto",
                    "title": {
                        "equals": project_title
                    }
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            results = response.json().get('results', [])
            if results:
                return results[0]['id']
            return None
        
        except Exception as e:
            print(f"⚠️  Error buscando proyecto '{project_title}': {e}")
            return None
    
    def create_or_update_project(self, project: Dict) -> bool:
        """Crea o actualiza un proyecto en Notion."""
        try:
            # Verificar si existe
            page_id = self.project_exists(project['title'])
            
            # Preparar datos
            notion_data = {
                "properties": {
                    "Nombre del Proyecto": {
                        "title": [
                            {
                                "text": {
                                    "content": project['title']
                                }
                            }
                        ]
                    },
                    "Descripción": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": project['description'][:2000]  # Límite de Notion
                                }
                            }
                        ]
                    }
                }
            }
            
            if page_id:
                # Actualizar página existente
                url = f"{self.base_url}/pages/{page_id}"
                response = requests.patch(url, headers=self.headers, json=notion_data)
                response.raise_for_status()
                print(f"✅ Actualizado: {project['title']}")
            else:
                # Crear nueva página
                notion_data["parent"] = {"database_id": self.database_id}
                url = f"{self.base_url}/pages"
                response = requests.post(url, headers=self.headers, json=notion_data)
                response.raise_for_status()
                print(f"✅ Creado: {project['title']}")
            
            return True
        
        except Exception as e:
            print(f"❌ Error con '{project['title']}': {e}")
            if hasattr(e, 'response'):
                print(f"   Respuesta: {e.response.text}")
            return False
    
    def sync_all(self):
        """Sincroniza todos los proyectos a Notion."""
        print("🚀 Iniciando sincronización con Notion...\n")
        
        # Verificar configuración
        if not self.check_database_properties():
            print("\n❌ Por favor, configura tu base de datos de Notion correctamente.")
            print("\n📋 Necesitas estas propiedades:")
            print("   - Nombre del Proyecto (tipo: Title)")
            print("   - Descripción (tipo: Text)")
            return
        
        print()
        
        # Obtener proyectos
        projects = self.get_all_projects()
        print(f"📁 Proyectos encontrados: {len(projects)}\n")
        
        # Sincronizar
        success_count = 0
        for project in projects:
            if self.create_or_update_project(project):
                success_count += 1
        
        print(f"\n✨ Sincronización completada: {success_count}/{len(projects)} proyectos")


def main():
    """Función principal."""
    try:
        syncer = NotionSync()
        syncer.sync_all()
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()

