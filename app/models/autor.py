"""
Modelo de Autor.
Representa a los autores de artículos académicos.
"""
from datetime import datetime
from app import db


class Autor(db.Model):
    """
    Modelo para representar autores de artículos.
    Un autor puede pertenecer a múltiples artículos (relación N:N).
    """
    __tablename__ = 'autores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=True, unique=True)
    
    # Número de registro institucional (para miembros del CA)
    registro = db.Column(db.String(50), nullable=True)
    
    # Indica si es miembro activo del Cuerpo Académico
    es_miembro_ca = db.Column(db.Boolean, nullable=False, default=False)
    
    # Estado del registro
    activo = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Autor {self.nombre_completo}>'
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del autor."""
        return f"{self.nombre} {self.apellidos}"
    
    @property
    def nombre_formato_cita(self):
        """Retorna el nombre en formato de cita: Apellidos, N."""
        inicial = self.nombre[0].upper() if self.nombre else ''
        return f"{self.apellidos}, {inicial}."
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'nombre_completo': self.nombre_completo,
            'email': self.email,
            'registro': self.registro,
            'es_miembro_ca': self.es_miembro_ca,
            'activo': self.activo
        }
    
    @staticmethod
    def buscar_por_nombre(nombre, apellidos):
        """
        Busca un autor por nombre y apellidos.
        Útil para evitar duplicados al importar.
        """
        return Autor.query.filter(
            db.func.lower(Autor.nombre) == db.func.lower(nombre),
            db.func.lower(Autor.apellidos) == db.func.lower(apellidos)
        ).first()
