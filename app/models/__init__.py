"""
Modelos de la aplicación
"""
from app.models.articulo import Articulo
from app.models.autor import Autor
from app.models.revista import Revista
from app.models.catalogs import (
    TipoProduccion,
    Proposito,
    Estado,
    LGAC,
    Indexacion,
    Pais
)
from app.models.associations import (
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
