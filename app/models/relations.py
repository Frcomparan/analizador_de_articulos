"""
Modelos de relaciones N:N (tablas intermedias).
Incluye: ArticuloAutor, ArticuloIndexacion, RevistaIndexacion
"""
from datetime import datetime
from app import db


class ArticuloAutor(db.Model):
    """
    Tabla intermedia para la relación N:N entre Artículos y Autores.
    Incluye el orden del autor en el artículo y si es autor corresponsal.
    """
    __tablename__ = 'articulo_autor'
    
    id = db.Column(db.Integer, primary_key=True)
    articulo_id = db.Column(db.Integer, db.ForeignKey('articulos.id'), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autores.id'), nullable=False)
    
    # Orden del autor en la lista de autores (1 = primer autor)
    orden = db.Column(db.Integer, nullable=False, default=1)
    
    # Indica si es el autor corresponsal
    es_corresponsal = db.Column(db.Boolean, nullable=False, default=False)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relaciones
    articulo = db.relationship('Articulo', backref=db.backref('articulo_autores', 
                                                               lazy='dynamic',
                                                               order_by='ArticuloAutor.orden'))
    autor = db.relationship('Autor', backref=db.backref('articulo_autores', lazy='dynamic'))
    
    # Constraint único para evitar duplicados
    __table_args__ = (
        db.UniqueConstraint('articulo_id', 'autor_id', name='uq_articulo_autor'),
    )
    
    def __repr__(self):
        return f'<ArticuloAutor art={self.articulo_id} aut={self.autor_id} ord={self.orden}>'


class RevistaIndexacion(db.Model):
    """
    Tabla intermedia para la relación N:N entre Revistas e Indexaciones.
    Una revista puede estar indexada en múltiples bases de datos.
    """
    __tablename__ = 'revista_indexacion'
    
    id = db.Column(db.Integer, primary_key=True)
    revista_id = db.Column(db.Integer, db.ForeignKey('revistas.id'), nullable=False)
    indexacion_id = db.Column(db.Integer, db.ForeignKey('indexaciones.id'), nullable=False)
    
    # Año en que se indexó (opcional)
    anio_indexacion = db.Column(db.Integer, nullable=True)
    
    # Estado de la indexación (puede haber sido removida)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relaciones
    revista = db.relationship('Revista', backref=db.backref('revista_indexaciones', 
                                                             lazy='dynamic'))
    indexacion = db.relationship('Indexacion', backref=db.backref('revista_indexaciones', 
                                                                    lazy='dynamic'))
    
    # Constraint único para evitar duplicados
    __table_args__ = (
        db.UniqueConstraint('revista_id', 'indexacion_id', name='uq_revista_indexacion'),
    )
    
    def __repr__(self):
        return f'<RevistaIndexacion rev={self.revista_id} idx={self.indexacion_id}>'


class ArticuloIndexacion(db.Model):
    """
    Tabla intermedia para la relación N:N entre Artículos e Indexaciones.
    Permite asignar indexaciones directamente a artículos (independiente de la revista).
    Útil cuando un artículo tiene indexaciones específicas diferentes a las de la revista.
    """
    __tablename__ = 'articulo_indexacion'
    
    id = db.Column(db.Integer, primary_key=True)
    articulo_id = db.Column(db.Integer, db.ForeignKey('articulos.id'), nullable=False)
    indexacion_id = db.Column(db.Integer, db.ForeignKey('indexaciones.id'), nullable=False)
    
    # Fecha en que se verificó la indexación
    fecha_verificacion = db.Column(db.Date, nullable=True)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relaciones
    articulo = db.relationship('Articulo', backref=db.backref('articulo_indexaciones', 
                                                               lazy='dynamic'))
    indexacion = db.relationship('Indexacion', backref=db.backref('articulo_indexaciones', 
                                                                    lazy='dynamic'))
    
    # Constraint único para evitar duplicados
    __table_args__ = (
        db.UniqueConstraint('articulo_id', 'indexacion_id', name='uq_articulo_indexacion'),
    )
    
    def __repr__(self):
        return f'<ArticuloIndexacion art={self.articulo_id} idx={self.indexacion_id}>'
