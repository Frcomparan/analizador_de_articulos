"""
Modelo de Artículo.
Modelo principal del sistema que representa una producción académica.
"""
from datetime import datetime
from app import db


class Articulo(db.Model):
    """
    Modelo principal para representar artículos/producciones académicas.
    Contiene todos los campos necesarios para el Excel del CA.
    """
    __tablename__ = 'articulos'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # === Información básica del artículo ===
    titulo = db.Column(db.String(500), nullable=False)
    titulo_revista = db.Column(db.String(300), nullable=True)  # Puede diferir de revista.nombre
    
    # === Clasificación y tipo ===
    tipo_produccion_id = db.Column(db.Integer, db.ForeignKey('tipos_produccion.id'), 
                                    nullable=False)
    proposito_id = db.Column(db.Integer, db.ForeignKey('propositos.id'), nullable=True)
    lgac_id = db.Column(db.Integer, db.ForeignKey('lgac.id'), nullable=True)
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=False)
    
    # === Fechas ===
    anio_publicacion = db.Column(db.Integer, nullable=True)
    fecha_publicacion = db.Column(db.Date, nullable=True)
    fecha_aceptacion = db.Column(db.Date, nullable=True)
    
    # === Datos de la publicación ===
    revista_id = db.Column(db.Integer, db.ForeignKey('revistas.id'), nullable=True)
    volumen = db.Column(db.String(20), nullable=True)
    numero = db.Column(db.String(20), nullable=True)
    pagina_inicio = db.Column(db.Integer, nullable=True)
    pagina_fin = db.Column(db.Integer, nullable=True)
    
    # === Identificadores ===
    doi = db.Column(db.String(100), nullable=True, unique=True)
    url = db.Column(db.String(500), nullable=True)  # Dirección electrónica del artículo
    issn = db.Column(db.String(20), nullable=True)  # ISSN de la revista (cache)
    
    # === Campos específicos para congresos ===
    nombre_congreso = db.Column(db.String(300), nullable=True)
    
    # === Campos para el CA ===
    para_curriculum = db.Column(db.Boolean, nullable=False, default=True)
    
    # === Indicadores ===
    factor_impacto = db.Column(db.Float, nullable=True)
    quartil = db.Column(db.String(5), nullable=True)  # Q1, Q2, Q3, Q4
    citas = db.Column(db.Integer, nullable=True, default=0)
    
    # === Estado del registro ===
    completo = db.Column(db.Boolean, nullable=False, default=False)
    campos_faltantes = db.Column(db.Text, nullable=True)  # JSON con lista de campos faltantes
    
    # === Archivo fuente ===
    archivo_origen = db.Column(db.String(255), nullable=True)
    
    # === Metadatos ===
    activo = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Articulo {self.titulo[:50]}...>'
    
    @property
    def paginas(self):
        """Retorna el rango de páginas formateado."""
        if self.pagina_inicio and self.pagina_fin:
            return f"{self.pagina_inicio}-{self.pagina_fin}"
        elif self.pagina_inicio:
            return str(self.pagina_inicio)
        return None
    
    @property
    def num_paginas(self):
        """Calcula el número de páginas del artículo."""
        if self.pagina_inicio and self.pagina_fin:
            return self.pagina_fin - self.pagina_inicio + 1
        return None
    
    @property
    def es_conference_paper(self):
        """Indica si es un artículo de conferencia."""
        if self.tipo:
            return 'conference' in self.tipo.nombre.lower() or 'congreso' in self.tipo.nombre.lower()
        return False
    
    def to_dict(self, include_relations=False):
        """
        Convierte el artículo a diccionario.
        
        Args:
            include_relations: Si es True, incluye autores e indexaciones.
        """
        data = {
            'id': self.id,
            'titulo': self.titulo,
            'titulo_revista': self.titulo_revista,
            'tipo_produccion_id': self.tipo_produccion_id,
            'tipo_produccion': self.tipo.nombre if self.tipo else None,
            'proposito_id': self.proposito_id,
            'proposito': self.proposito.nombre if self.proposito else None,
            'lgac_id': self.lgac_id,
            'lgac': self.lgac.nombre if self.lgac else None,
            'estado_id': self.estado_id,
            'estado': self.estado.nombre if self.estado else None,
            'anio_publicacion': self.anio_publicacion,
            'fecha_publicacion': self.fecha_publicacion.isoformat() if self.fecha_publicacion else None,
            'fecha_aceptacion': self.fecha_aceptacion.isoformat() if self.fecha_aceptacion else None,
            'revista_id': self.revista_id,
            'revista': self.revista.nombre if self.revista else None,
            'volumen': self.volumen,
            'numero': self.numero,
            'paginas': self.paginas,
            'pagina_inicio': self.pagina_inicio,
            'pagina_fin': self.pagina_fin,
            'doi': self.doi,
            'url': self.url,
            'issn': self.issn,
            'nombre_congreso': self.nombre_congreso,
            'para_curriculum': self.para_curriculum,
            'factor_impacto': self.factor_impacto,
            'quartil': self.quartil,
            'citas': self.citas,
            'completo': self.completo,
            'campos_faltantes': self.campos_faltantes,
            'archivo_origen': self.archivo_origen,
            'activo': self.activo
        }
        
        if include_relations:
            data['autores'] = [aa.autor.to_dict() for aa in self.articulo_autores]
            # Las indexaciones se obtienen de la revista
            if self.revista:
                data['indexaciones'] = [ri.indexacion.to_dict() 
                                         for ri in self.revista.revista_indexaciones]
        
        return data
    
    def calcular_completitud(self):
        """
        Calcula si el artículo tiene todos los campos obligatorios.
        Retorna True si está completo, False si faltan campos.
        Actualiza el campo campos_faltantes con la lista de campos faltantes.
        """
        import json
        
        campos_obligatorios = [
            ('titulo', 'Título'),
            ('tipo_produccion_id', 'Tipo de producción'),
            ('estado_id', 'Estado'),
            ('anio_publicacion', 'Año de publicación'),
        ]
        
        # Campos adicionales obligatorios para artículos publicados
        if self.estado and self.estado.nombre.lower() == 'publicado':
            campos_obligatorios.extend([
                ('revista_id', 'Revista'),
                ('volumen', 'Volumen'),
                ('numero', 'Número'),
                ('pagina_inicio', 'Página inicio'),
                ('pagina_fin', 'Página fin'),
            ])
        
        # Si es conference paper, el nombre del congreso es obligatorio
        if self.es_conference_paper:
            campos_obligatorios.append(('nombre_congreso', 'Nombre del congreso'))
        
        faltantes = []
        for campo, nombre in campos_obligatorios:
            valor = getattr(self, campo, None)
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                faltantes.append(nombre)
        
        # Verificar que tenga al menos un autor
        if not hasattr(self, 'articulo_autores') or not self.articulo_autores:
            faltantes.append('Autores')
        
        self.campos_faltantes = json.dumps(faltantes, ensure_ascii=False) if faltantes else None
        self.completo = len(faltantes) == 0
        
        return self.completo
    
    def to_excel_row(self):
        """
        Convierte el artículo al formato de fila para Excel del CA.
        Retorna un diccionario con las columnas del Excel.
        """
        autores_lista = [aa.autor.nombre_completo for aa in self.articulo_autores] if hasattr(self, 'articulo_autores') else []
        
        # Obtener indexaciones de la revista
        indexaciones_lista = []
        if self.revista and hasattr(self.revista, 'revista_indexaciones'):
            indexaciones_lista = [ri.indexacion.nombre for ri in self.revista.revista_indexaciones]
        
        return {
            'Título del artículo': self.titulo,
            'Tipo de producción': self.tipo.nombre if self.tipo else '',
            'Estado': self.estado.nombre if self.estado else '',
            'Propósito': self.proposito.nombre if self.proposito else '',
            'LGAC': self.lgac.nombre if self.lgac else '',
            'Autores': ', '.join(autores_lista),
            'Nombre de la revista': self.revista.nombre if self.revista else self.titulo_revista or '',
            'Volumen': self.volumen or '',
            'Número': self.numero or '',
            'Página inicio': self.pagina_inicio or '',
            'Página fin': self.pagina_fin or '',
            'Año de publicación': self.anio_publicacion or '',
            'Fecha de publicación': self.fecha_publicacion.strftime('%d/%m/%Y') if self.fecha_publicacion else '',
            'ISSN': self.issn or (self.revista.issn if self.revista else ''),
            'País de la revista': self.revista.pais.nombre if self.revista and self.revista.pais else '',
            'DOI': self.doi or '',
            'URL': self.url or '',
            'Indexaciones': ', '.join(indexaciones_lista),
            'Factor de impacto': self.factor_impacto or '',
            'Quartil': self.quartil or '',
            'Nombre del congreso': self.nombre_congreso or '',
            'Para currículum CA': 'Sí' if self.para_curriculum else 'No'
        }
