"""
Formularios para gestión de catálogos.
Un formulario por cada tipo de catálogo del sistema.
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SelectField, BooleanField, 
    IntegerField, SubmitField
)
from wtforms.validators import DataRequired, Optional, Length, Email, URL, NumberRange
from app.models import Pais


class TipoProduccionForm(FlaskForm):
    """Formulario para Tipos de Producción."""
    nombre = StringField(
        'Nombre',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'Ej: Artículo científico'}
    )
    descripcion = TextAreaField(
        'Descripción',
        validators=[Optional(), Length(max=500)],
        render_kw={'placeholder': 'Descripción del tipo de producción', 'rows': 3}
    )
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')


class PropositoForm(FlaskForm):
    """Formulario para Propósitos."""
    nombre = StringField(
        'Nombre',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'Ej: Investigación básica'}
    )
    descripcion = TextAreaField(
        'Descripción',
        validators=[Optional(), Length(max=500)],
        render_kw={'placeholder': 'Descripción del propósito', 'rows': 3}
    )
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')


class EstadoForm(FlaskForm):
    """Formulario para Estados."""
    nombre = StringField(
        'Nombre',
        validators=[DataRequired(), Length(max=50)],
        render_kw={'placeholder': 'Ej: En revisión'}
    )
    color = StringField(
        'Color (hex)',
        validators=[Optional(), Length(max=20)],
        render_kw={'placeholder': '#007bff', 'type': 'color'}
    )
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')


class LGACForm(FlaskForm):
    """Formulario para LGACs."""
    nombre = StringField(
        'Nombre',
        validators=[DataRequired(), Length(max=200)],
        render_kw={'placeholder': 'Ej: LGAC 1 - Inteligencia Artificial'}
    )
    descripcion = TextAreaField(
        'Descripción',
        validators=[Optional(), Length(max=500)],
        render_kw={'placeholder': 'Descripción de la LGAC', 'rows': 3}
    )
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')


class IndexacionForm(FlaskForm):
    """Formulario para Indexaciones."""
    nombre = StringField(
        'Nombre',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'Ej: Web of Science'}
    )
    acronimo = StringField(
        'Acrónimo',
        validators=[Optional(), Length(max=20)],
        render_kw={'placeholder': 'Ej: WoS'}
    )
    url = StringField(
        'URL',
        validators=[Optional(), URL(), Length(max=255)],
        render_kw={'placeholder': 'https://...'}
    )
    prestigio = IntegerField(
        'Nivel de prestigio (1-5)',
        validators=[Optional(), NumberRange(min=1, max=5)],
        render_kw={'placeholder': '5 = Máximo prestigio'}
    )
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')


class PaisForm(FlaskForm):
    """Formulario para Países."""
    nombre = StringField(
        'Nombre',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'Ej: México'}
    )
    codigo_iso = StringField(
        'Código ISO',
        validators=[Optional(), Length(max=3)],
        render_kw={'placeholder': 'MEX'}
    )
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')


class AutorForm(FlaskForm):
    """Formulario para Autores."""
    nombre = StringField(
        'Nombre(s)',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'Juan'}
    )
    apellidos = StringField(
        'Apellidos',
        validators=[DataRequired(), Length(max=150)],
        render_kw={'placeholder': 'Pérez García'}
    )
    email = StringField(
        'Email',
        validators=[Optional(), Email(), Length(max=100)],
        render_kw={'placeholder': 'juan.perez@ejemplo.com'}
    )
    orcid = StringField(
        'ORCID',
        validators=[Optional(), Length(max=19)],
        render_kw={'placeholder': '0000-0002-1234-5678'}
    )
    registro = StringField(
        'Registro/ID Institucional',
        validators=[Optional(), Length(max=50)],
        render_kw={'placeholder': 'Registro o matrícula'}
    )
    es_miembro_ca = BooleanField('Miembro del Cuerpo Académico', default=False)
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')


class RevistaForm(FlaskForm):
    """Formulario para Revistas."""
    nombre = StringField(
        'Nombre de la revista',
        validators=[DataRequired(), Length(max=300)],
        render_kw={'placeholder': 'Ej: Nature'}
    )
    issn = StringField(
        'ISSN',
        validators=[Optional(), Length(max=20)],
        render_kw={'placeholder': '1234-5678'}
    )
    issn_electronico = StringField(
        'ISSN Electrónico',
        validators=[Optional(), Length(max=20)],
        render_kw={'placeholder': '1234-5679'}
    )
    editorial = StringField(
        'Editorial',
        validators=[Optional(), Length(max=200)],
        render_kw={'placeholder': 'Nombre de la editorial'}
    )
    pais_id = SelectField(
        'País',
        coerce=int,
        validators=[Optional()]
    )
    url = StringField(
        'URL',
        validators=[Optional(), URL(), Length(max=500)],
        render_kw={'placeholder': 'https://...'}
    )
    area_tematica = StringField(
        'Área temática',
        validators=[Optional(), Length(max=200)],
        render_kw={'placeholder': 'Ej: Ciencias Computacionales'}
    )
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')
    
    def __init__(self, *args, **kwargs):
        super(RevistaForm, self).__init__(*args, **kwargs)
        # Poblar opciones de países
        self.pais_id.choices = [(0, 'Seleccione un país')] + [
            (p.id, p.nombre) for p in Pais.query.filter_by(activo=True).order_by(Pais.nombre).all()
        ]


# Mapeo de catálogos a formularios
CATALOG_FORMS = {
    'tipos_produccion': TipoProduccionForm,
    'propositos': PropositoForm,
    'estados': EstadoForm,
    'lgac': LGACForm,
    'indexaciones': IndexacionForm,
    'paises': PaisForm,
    'autores': AutorForm,
    'revistas': RevistaForm
}


def get_catalog_form(catalog_name: str, **kwargs):
    """
    Factory para obtener el formulario apropiado según el catálogo.
    
    Args:
        catalog_name: Nombre del catálogo
        **kwargs: Argumentos para el formulario
        
    Returns:
        Instancia del formulario o None si no existe
    """
    form_class = CATALOG_FORMS.get(catalog_name)
    if form_class:
        return form_class(**kwargs)
    return None
