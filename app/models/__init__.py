"""
Modelos de la aplicación.
Se importan todos los modelos aquí para facilitar el acceso 
y asegurar que SQLAlchemy los registre correctamente.
"""
# Primero importamos los catálogos (sin dependencias)
from app.models.catalogs import (
    TipoProduccion,
    Proposito,
    Estado,
    LGAC,
    Indexacion,
    Pais
)

# Luego los modelos principales
from app.models.autor import Autor
from app.models.revista import Revista
from app.models.articulo import Articulo

# Finalmente las relaciones N:N
from app.models.relations import (
    ArticuloAutor,
    ArticuloIndexacion,
    RevistaIndexacion
)

__all__ = [
    'Articulo',
    'Autor',
    'Revista',
    'TipoProduccion',
    'Proposito',
    'Estado',
    'LGAC',
    'Indexacion',
    'Pais',
    'ArticuloAutor',
    'ArticuloIndexacion',
    'RevistaIndexacion'
]
