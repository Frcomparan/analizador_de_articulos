"""
Controlador genérico para gestión de catálogos.
Proporciona operaciones CRUD reutilizables para todos los catálogos del sistema.
"""
from typing import Tuple, Optional, Dict, Any, List
from app import db
from app.models import (
    TipoProduccion, Proposito, Estado, LGAC, 
    Indexacion, Pais, Autor, Revista
)
from sqlalchemy import or_
import logging

logger = logging.getLogger(__name__)


class CatalogController:
    """
    Controlador genérico para operaciones CRUD de catálogos.
    Usa reflexión para trabajar con cualquier modelo de catálogo.
    """
    
    # Mapeo de nombres a modelos
    CATALOG_MODELS = {
        'tipos_produccion': TipoProduccion,
        'propositos': Proposito,
        'estados': Estado,
        'lgac': LGAC,
        'indexaciones': Indexacion,
        'paises': Pais,
        'autores': Autor,
        'revistas': Revista
    }
    
    # Configuración de cada catálogo
    CATALOG_CONFIG = {
        'tipos_produccion': {
            'display_name': 'Tipos de Producción',
            'singular': 'Tipo de Producción',
            'fields': ['nombre', 'descripcion', 'activo'],
            'search_fields': ['nombre', 'descripcion'],
            'icon': 'bi-file-earmark-text'
        },
        'propositos': {
            'display_name': 'Propósitos',
            'singular': 'Propósito',
            'fields': ['nombre', 'descripcion', 'activo'],
            'search_fields': ['nombre', 'descripcion'],
            'icon': 'bi-bullseye'
        },
        'estados': {
            'display_name': 'Estados',
            'singular': 'Estado',
            'fields': ['nombre', 'color', 'activo'],
            'search_fields': ['nombre'],
            'icon': 'bi-flag'
        },
        'lgac': {
            'display_name': 'Líneas de Generación y Aplicación del Conocimiento',
            'singular': 'LGAC',
            'fields': ['nombre', 'descripcion', 'activo'],
            'search_fields': ['nombre', 'descripcion'],
            'icon': 'bi-diagram-3'
        },
        'indexaciones': {
            'display_name': 'Indexaciones',
            'singular': 'Indexación',
            'fields': ['nombre', 'acronimo', 'url', 'prestigio', 'activo'],
            'search_fields': ['nombre', 'acronimo'],
            'icon': 'bi-bookmark-star'
        },
        'paises': {
            'display_name': 'Países',
            'singular': 'País',
            'fields': ['nombre', 'codigo_iso', 'activo'],
            'search_fields': ['nombre', 'codigo_iso'],
            'icon': 'bi-globe'
        },
        'autores': {
            'display_name': 'Autores',
            'singular': 'Autor',
            'fields': ['nombre', 'apellidos', 'email', 'orcid', 'registro', 'es_miembro_ca', 'activo'],
            'search_fields': ['nombre', 'apellidos', 'email', 'orcid'],
            'icon': 'bi-person'
        },
        'revistas': {
            'display_name': 'Revistas',
            'singular': 'Revista',
            'fields': ['nombre', 'issn', 'issn_electronico', 'editorial', 'pais_id', 'url', 'area_tematica', 'activo'],
            'search_fields': ['nombre', 'issn', 'editorial'],
            'icon': 'bi-journal'
        }
    }
    
    @classmethod
    def get_model(cls, catalog_name: str):
        """Obtiene el modelo de SQLAlchemy para un catálogo."""
        return cls.CATALOG_MODELS.get(catalog_name)
    
    @classmethod
    def get_config(cls, catalog_name: str) -> Dict[str, Any]:
        """Obtiene la configuración de un catálogo."""
        return cls.CATALOG_CONFIG.get(catalog_name, {})
    
    @classmethod
    def get_all(cls, catalog_name: str, page: int = 1, per_page: int = 50, 
                query: str = None, show_inactive: bool = False) -> Tuple[Optional[Any], Optional[str]]:
        """
        Obtiene todos los registros de un catálogo con paginación.
        
        Args:
            catalog_name: Nombre del catálogo
            page: Número de página
            per_page: Registros por página
            query: Búsqueda por texto
            show_inactive: Mostrar registros inactivos
            
        Returns:
            (pagination_object, error_message)
        """
        try:
            model = cls.get_model(catalog_name)
            if not model:
                return None, f"Catálogo '{catalog_name}' no encontrado"
            
            config = cls.get_config(catalog_name)
            search_fields = config.get('search_fields', ['nombre'])
            
            # Construir query
            query_obj = model.query
            
            # Filtro de búsqueda
            if query:
                filters = []
                for field in search_fields:
                    if hasattr(model, field):
                        filters.append(getattr(model, field).ilike(f'%{query}%'))
                if filters:
                    query_obj = query_obj.filter(or_(*filters))
            
            # Filtro de activos/inactivos
            if not show_inactive and hasattr(model, 'activo'):
                query_obj = query_obj.filter(model.activo == True)
            
            # Ordenar por nombre o id
            if hasattr(model, 'nombre'):
                query_obj = query_obj.order_by(model.nombre)
            else:
                query_obj = query_obj.order_by(model.id)
            
            # Paginar
            pagination = query_obj.paginate(page=page, per_page=per_page, error_out=False)
            
            return pagination, None
            
        except Exception as e:
            logger.error(f"Error al obtener catálogo {catalog_name}: {str(e)}")
            return None, str(e)
    
    @classmethod
    def get_by_id(cls, catalog_name: str, id: int) -> Tuple[Optional[Any], Optional[str]]:
        """
        Obtiene un registro específico de un catálogo.
        
        Args:
            catalog_name: Nombre del catálogo
            id: ID del registro
            
        Returns:
            (registro, error_message)
        """
        try:
            model = cls.get_model(catalog_name)
            if not model:
                return None, f"Catálogo '{catalog_name}' no encontrado"
            
            registro = model.query.get(id)
            
            if not registro:
                return None, f"Registro no encontrado"
            
            return registro, None
            
        except Exception as e:
            logger.error(f"Error al obtener registro {id} de {catalog_name}: {str(e)}")
            return None, str(e)
    
    @classmethod
    def create(cls, catalog_name: str, data: Dict[str, Any]) -> Tuple[Optional[Any], Optional[str]]:
        """
        Crea un nuevo registro en un catálogo.
        
        Args:
            catalog_name: Nombre del catálogo
            data: Diccionario con los datos del registro
            
        Returns:
            (registro_creado, error_message)
        """
        try:
            model = cls.get_model(catalog_name)
            if not model:
                return None, f"Catálogo '{catalog_name}' no encontrado"
            
            # Crear instancia
            registro = model(**data)
            
            # Guardar en BD
            db.session.add(registro)
            db.session.commit()
            
            logger.info(f"Registro creado en {catalog_name}: {registro.id}")
            return registro, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al crear registro en {catalog_name}: {str(e)}")
            return None, str(e)
    
    @classmethod
    def update(cls, catalog_name: str, id: int, data: Dict[str, Any]) -> Tuple[Optional[Any], Optional[str]]:
        """
        Actualiza un registro existente.
        
        Args:
            catalog_name: Nombre del catálogo
            id: ID del registro a actualizar
            data: Diccionario con los campos a actualizar
            
        Returns:
            (registro_actualizado, error_message)
        """
        try:
            registro, error = cls.get_by_id(catalog_name, id)
            if error:
                return None, error
            
            # Actualizar campos
            for key, value in data.items():
                if hasattr(registro, key):
                    setattr(registro, key, value)
            
            db.session.commit()
            
            logger.info(f"Registro {id} actualizado en {catalog_name}")
            return registro, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al actualizar registro {id} en {catalog_name}: {str(e)}")
            return None, str(e)
    
    @classmethod
    def delete(cls, catalog_name: str, id: int, soft: bool = True) -> Tuple[bool, Optional[str]]:
        """
        Elimina un registro (lógica o físicamente).
        
        Args:
            catalog_name: Nombre del catálogo
            id: ID del registro a eliminar
            soft: True para eliminación lógica (activo=False), False para física
            
        Returns:
            (success, error_message)
        """
        try:
            registro, error = cls.get_by_id(catalog_name, id)
            if error:
                return False, error
            
            if soft and hasattr(registro, 'activo'):
                # Eliminación lógica
                registro.activo = False
                db.session.commit()
                logger.info(f"Registro {id} desactivado en {catalog_name}")
            else:
                # Eliminación física - Manejo especial para autores
                if catalog_name == 'autores':
                    # Eliminar todas las relaciones con artículos antes de eliminar el autor
                    from app.models.relations import ArticuloAutor
                    articulos_count = ArticuloAutor.query.filter_by(autor_id=id).count()
                    
                    if articulos_count > 0:
                        # Eliminar todas las relaciones articulo_autor
                        ArticuloAutor.query.filter_by(autor_id=id).delete()
                        logger.info(f"Eliminadas {articulos_count} relaciones de autor {id} con artículos")
                
                # Eliminación física
                db.session.delete(registro)
                db.session.commit()
                logger.info(f"Registro {id} eliminado físicamente de {catalog_name}")
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al eliminar registro {id} de {catalog_name}: {str(e)}")
            return False, str(e)
    
    @classmethod
    def toggle_active(cls, catalog_name: str, id: int) -> Tuple[Optional[Any], Optional[str]]:
        """
        Alterna el estado activo/inactivo de un registro.
        
        Args:
            catalog_name: Nombre del catálogo
            id: ID del registro
            
        Returns:
            (registro_actualizado, error_message)
        """
        try:
            registro, error = cls.get_by_id(catalog_name, id)
            if error:
                return None, error
            
            if not hasattr(registro, 'activo'):
                return None, "Este catálogo no soporta activar/desactivar"
            
            registro.activo = not registro.activo
            db.session.commit()
            
            estado = "activado" if registro.activo else "desactivado"
            logger.info(f"Registro {id} {estado} en {catalog_name}")
            return registro, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al cambiar estado de registro {id} en {catalog_name}: {str(e)}")
            return None, str(e)
    
    @classmethod
    def get_catalog_list(cls) -> List[Dict[str, Any]]:
        """
        Obtiene lista de todos los catálogos disponibles con su configuración.
        
        Returns:
            Lista de diccionarios con información de cada catálogo
        """
        catalogs = []
        for name, config in cls.CATALOG_CONFIG.items():
            model = cls.get_model(name)
            count = model.query.count() if model else 0
            active_count = model.query.filter_by(activo=True).count() if model and hasattr(model, 'activo') else count
            
            catalogs.append({
                'name': name,
                'display_name': config.get('display_name'),
                'singular': config.get('singular'),
                'icon': config.get('icon'),
                'count': count,
                'active_count': active_count
            })
        
        return catalogs
