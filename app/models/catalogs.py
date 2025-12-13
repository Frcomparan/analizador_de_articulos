"""
Modelos de catálogos del sistema.
Incluye: TipoProduccion, Proposito, Estado, LGAC, Indexacion, Pais
"""
from datetime import datetime
from app import db


class TipoProduccion(db.Model):
    """
    Catálogo de tipos de producción académica.
    Ejemplos: Artículo científico, Review, Conference paper, etc.
    """
    __tablename__ = 'tipos_produccion'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relación con artículos
    articulos = db.relationship('Articulo', back_populates='tipo', lazy='dynamic')
    
    def __repr__(self):
        return f'<TipoProduccion {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activo': self.activo
        }


class Proposito(db.Model):
    """
    Catálogo de propósitos del artículo.
    Ejemplos: Investigación básica, Investigación aplicada, Divulgación, etc.
    """
    __tablename__ = 'propositos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relación con artículos
    articulos = db.relationship('Articulo', back_populates='proposito', lazy='dynamic')
    
    def __repr__(self):
        return f'<Proposito {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activo': self.activo
        }


class Estado(db.Model):
    """
    Catálogo de estados del artículo.
    Ejemplos: En preparación, Enviado, En revisión, Aceptado, Publicado, Rechazado
    """
    __tablename__ = 'estados'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(20), nullable=True)  # Color hexadecimal para badges
    activo = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relación con artículos
    articulos = db.relationship('Articulo', back_populates='estado', lazy='dynamic')
    
    def __repr__(self):
        return f'<Estado {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'color': self.color,
            'activo': self.activo
        }


class LGAC(db.Model):
    """
    Líneas de Generación y Aplicación del Conocimiento.
    Específicas del Cuerpo Académico.
    """
    __tablename__ = 'lgac'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relación con artículos
    articulos = db.relationship('Articulo', back_populates='lgac', lazy='dynamic')
    
    def __repr__(self):
        return f'<LGAC {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'activo': self.activo
        }


class Indexacion(db.Model):
    """
    Catálogo de bases de datos de indexación.
    Ejemplos: Scopus, Web of Science, SciELO, Latindex, etc.
    """
    __tablename__ = 'indexaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    acronimo = db.Column(db.String(20), nullable=True)  # WoS, JCR, etc.
    url = db.Column(db.String(255), nullable=True)
    prestigio = db.Column(db.Integer, nullable=True)  # 1-5, donde 5 es máximo
    activo = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Indexacion {self.acronimo or self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'acronimo': self.acronimo,
            'url': self.url,
            'prestigio': self.prestigio,
            'activo': self.activo
        }


class Pais(db.Model):
    """
    Catálogo de países.
    Se usa para indicar el país de publicación de revistas.
    """
    __tablename__ = 'paises'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    codigo_iso = db.Column(db.String(3), nullable=True, unique=True)  # ISO 3166-1 alpha-3
    activo = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relación con revistas
    revistas = db.relationship('Revista', backref='pais', lazy='dynamic')
    
    def __repr__(self):
        return f'<Pais {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'codigo_iso': self.codigo_iso,
            'activo': self.activo
        }
