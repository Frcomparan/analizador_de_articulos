"""
Formularios Flask-WTF
"""
from .article_form import ArticleForm, ArticleSearchForm, ArticleAuthorForm
from .utils import (
    populate_form_choices,
    populate_tipo_produccion_choices,
    populate_proposito_choices,
    populate_lgac_choices,
    populate_estado_choices,
    populate_revista_choices,
    populate_autor_choices,
    validate_articulo_data
)

__all__ = [
    'ArticleForm',
    'ArticleSearchForm',
    'ArticleAuthorForm',
    'populate_form_choices',
    'populate_tipo_produccion_choices',
    'populate_proposito_choices',
    'populate_lgac_choices',
    'populate_estado_choices',
    'populate_revista_choices',
    'populate_autor_choices',
    'validate_articulo_data'
]
