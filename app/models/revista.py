"""
Modelo de Revista.
Representa las revistas donde se publican los artículos.
"""
from datetime import datetime
from app import db


class Revista(db.Model):
    """
    Modelo para representar revistas académicas.
    Una revista puede tener múltiples artículos publicados.
    """
    __tablename__ = 'revistas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(300), nullable=False)
    
    # Identificadores únicos de la revista
    issn = db.Column(db.String(20), nullable=True, unique=True)
    issn_electronico = db.Column(db.String(20), nullable=True)
    
    # Editorial y país
    editorial = db.Column(db.String(200), nullable=True)
    pais_id = db.Column(db.Integer, db.ForeignKey('paises.id'), nullable=True)
    
    # Sitio web de la revista
    url = db.Column(db.String(500), nullable=True)
    
    # Área temática
    area_tematica = db.Column(db.String(200), nullable=True)
    
    # Estado del registro
    activo = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)
    
    # Relación con artículos
    articulos = db.relationship('Articulo', backref='revista', lazy='dynamic')
    
    # Relación N:N con indexaciones (se define en relations.py)
    
    def __repr__(self):
        return f'<Revista {self.nombre[:50]}>'
    
    @property
    def nombre_con_issn(self):
        """Retorna el nombre de la revista con su ISSN si existe."""
        if self.issn:
            return f"{self.nombre} (ISSN: {self.issn})"
        return self.nombre
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'issn': self.issn,
            'issn_electronico': self.issn_electronico,
            'editorial': self.editorial,
            'pais_id': self.pais_id,
            'pais': self.pais.nombre if self.pais else None,
            'url': self.url,
            'area_tematica': self.area_tematica,
            'activo': self.activo
        }
    
    @staticmethod
    def buscar_por_issn(issn):
        """Busca una revista por su ISSN."""
        if not issn:
            return None
        return Revista.query.filter(
            (Revista.issn == issn) | (Revista.issn_electronico == issn)
        ).first()
    
    @staticmethod
    def buscar_por_nombre(nombre):
        """Busca una revista por nombre (búsqueda parcial)."""
        return Revista.query.filter(
            db.func.lower(Revista.nombre).contains(db.func.lower(nombre))
        ).all()
