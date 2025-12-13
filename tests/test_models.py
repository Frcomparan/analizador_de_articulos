"""
Tests básicos para modelos y relaciones.
Ejecutar desde la raíz del proyecto: python -m pytest tests/test_models.py
"""
import pytest
from datetime import datetime, date
from app import create_app, db
from app.models import (
    Articulo, Autor, Revista, TipoProduccion, Estado, 
    LGAC, Proposito, Indexacion, Pais
)
from app.models.relations import ArticuloAutor, RevistaIndexacion


@pytest.fixture
def app():
    """Crea la aplicación para testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de prueba."""
    return app.test_client()


@pytest.fixture
def init_database(app):
    """Inicializa la base de datos con datos de prueba."""
    with app.app_context():
        # Crear catálogos básicos
        tipo = TipoProduccion(nombre='Artículo científico', activo=True)
        estado = Estado(nombre='Publicado', color='#28a745', activo=True)
        lgac = LGAC(nombre='LGAC de prueba', activo=True)
        proposito = Proposito(nombre='Investigación básica', activo=True)
        pais = Pais(nombre='México', codigo_iso='MEX', activo=True)
        indexacion = Indexacion(nombre='Scopus', acronimo='Scopus', prestigio=5, activo=True)
        
        db.session.add_all([tipo, estado, lgac, proposito, pais, indexacion])
        db.session.commit()
        
        yield db
        
        db.session.rollback()


# === Tests de Modelo Articulo ===

def test_crear_articulo_basico(init_database):
    """Test: Crear un artículo con campos obligatorios."""
    tipo = TipoProduccion.query.first()
    estado = Estado.query.first()
    
    articulo = Articulo(
        titulo='Test Article',
        tipo_produccion_id=tipo.id,
        estado_id=estado.id,
        anio_publicacion=2024
    )
    
    db.session.add(articulo)
    db.session.commit()
    
    assert articulo.id is not None
    assert articulo.titulo == 'Test Article'
    assert articulo.tipo.nombre == 'Artículo científico'
    assert articulo.estado.nombre == 'Publicado'


def test_articulo_relaciones(init_database):
    """Test: Verificar que las relaciones funcionan correctamente."""
    tipo = TipoProduccion.query.first()
    estado = Estado.query.first()
    lgac = LGAC.query.first()
    proposito = Proposito.query.first()
    
    articulo = Articulo(
        titulo='Article with Relations',
        tipo_produccion_id=tipo.id,
        estado_id=estado.id,
        lgac_id=lgac.id,
        proposito_id=proposito.id,
        anio_publicacion=2024
    )
    
    db.session.add(articulo)
    db.session.commit()
    
    assert articulo.lgac.nombre == 'LGAC de prueba'
    assert articulo.proposito.nombre == 'Investigación básica'


def test_articulo_validaciones(init_database):
    """Test: Validaciones del modelo Articulo."""
    tipo = TipoProduccion.query.first()
    estado = Estado.query.first()
    
    # DOI inválido
    articulo = Articulo(
        titulo='Test Validations',
        tipo_produccion_id=tipo.id,
        estado_id=estado.id,
        doi='invalid-doi',
        anio_publicacion=2024
    )
    
    assert not articulo.validar_doi()
    
    # DOI válido
    articulo.doi = '10.1234/test.2024.001'
    assert articulo.validar_doi()
    
    # ISSN válido
    articulo.issn = '1234-5678'
    assert articulo.validar_issn()
    
    # Año válido
    assert articulo.validar_anio()
    
    # Páginas válidas
    articulo.pagina_inicio = 10
    articulo.pagina_fin = 20
    assert articulo.validar_paginas()
    
    # Páginas inválidas
    articulo.pagina_inicio = 20
    articulo.pagina_fin = 10
    assert not articulo.validar_paginas()


def test_articulo_to_dict(init_database):
    """Test: Método to_dict del artículo."""
    tipo = TipoProduccion.query.first()
    estado = Estado.query.first()
    
    articulo = Articulo(
        titulo='Test Dict',
        tipo_produccion_id=tipo.id,
        estado_id=estado.id,
        anio_publicacion=2024,
        doi='10.1234/test'
    )
    
    db.session.add(articulo)
    db.session.commit()
    
    data = articulo.to_dict()
    
    assert data['titulo'] == 'Test Dict'
    assert data['anio_publicacion'] == 2024
    assert data['doi'] == '10.1234/test'
    assert data['tipo_produccion'] == 'Artículo científico'


# === Tests de Modelo Autor ===

def test_crear_autor(init_database):
    """Test: Crear un autor."""
    autor = Autor(
        nombre='Francisco',
        apellidos='Pérez García',
        email='francisco@test.com',
        es_miembro_ca=True
    )
    
    db.session.add(autor)
    db.session.commit()
    
    assert autor.id is not None
    assert autor.nombre_completo == 'Francisco Pérez García'


def test_autor_normalizar_nombre(init_database):
    """Test: Normalización de nombres."""
    autor = Autor(
        nombre='José María',
        apellidos='García-López'
    )
    
    autor.actualizar_nombre_normalizado()
    
    assert autor.nombre_normalizado == 'jose maria garcia lopez'


def test_autor_validaciones(init_database):
    """Test: Validaciones del modelo Autor."""
    # ORCID válido
    autor = Autor(
        nombre='Test',
        apellidos='Author',
        orcid='0000-0002-1825-0097'
    )
    
    assert autor.validar_orcid()
    
    # ORCID inválido
    autor.orcid = 'invalid-orcid'
    assert not autor.validar_orcid()
    
    # Email válido
    autor.email = 'test@example.com'
    assert autor.validar_email()
    
    # Email inválido
    autor.email = 'invalid-email'
    assert not autor.validar_email()


# === Tests de Relaciones N:N ===

def test_articulo_autores(init_database):
    """Test: Relación N:N entre Artículo y Autor."""
    tipo = TipoProduccion.query.first()
    estado = Estado.query.first()
    
    # Crear artículo
    articulo = Articulo(
        titulo='Test Authors',
        tipo_produccion_id=tipo.id,
        estado_id=estado.id,
        anio_publicacion=2024
    )
    db.session.add(articulo)
    db.session.commit()
    
    # Crear autores
    autor1 = Autor(nombre='Juan', apellidos='Pérez')
    autor2 = Autor(nombre='María', apellidos='García')
    autor3 = Autor(nombre='Pedro', apellidos='López')
    
    db.session.add_all([autor1, autor2, autor3])
    db.session.commit()
    
    # Agregar autores al artículo
    articulo.agregar_autor(autor1, orden=1, es_corresponsal=True)
    articulo.agregar_autor(autor2, orden=2)
    articulo.agregar_autor(autor3, orden=3)
    db.session.commit()
    
    # Verificar
    assert len(list(articulo.articulo_autores)) == 3
    
    primer_autor = articulo.articulo_autores[0]
    assert primer_autor.autor.nombre == 'Juan'
    assert primer_autor.orden == 1
    assert primer_autor.es_corresponsal == True


def test_revista_indexaciones(init_database):
    """Test: Relación N:N entre Revista e Indexación."""
    pais = Pais.query.first()
    indexacion = Indexacion.query.first()
    
    # Crear revista
    revista = Revista(
        nombre='Test Journal',
        issn='1234-5678',
        pais_id=pais.id
    )
    db.session.add(revista)
    db.session.commit()
    
    # Agregar indexación
    ri = RevistaIndexacion(
        revista_id=revista.id,
        indexacion_id=indexacion.id,
        anio_indexacion=2020
    )
    db.session.add(ri)
    db.session.commit()
    
    # Verificar
    assert len(list(revista.revista_indexaciones)) == 1
    assert revista.revista_indexaciones[0].indexacion.nombre == 'Scopus'


def test_busqueda_articulos(init_database):
    """Test: Método de búsqueda avanzada."""
    tipo = TipoProduccion.query.first()
    estado = Estado.query.first()
    lgac = LGAC.query.first()
    
    # Crear varios artículos
    art1 = Articulo(titulo='Python para Data Science', tipo_produccion_id=tipo.id,
                    estado_id=estado.id, anio_publicacion=2023, lgac_id=lgac.id)
    art2 = Articulo(titulo='Machine Learning Basics', tipo_produccion_id=tipo.id,
                    estado_id=estado.id, anio_publicacion=2024)
    art3 = Articulo(titulo='Deep Learning with Python', tipo_produccion_id=tipo.id,
                    estado_id=estado.id, anio_publicacion=2024, lgac_id=lgac.id)
    
    db.session.add_all([art1, art2, art3])
    db.session.commit()
    
    # Buscar por query
    resultados = Articulo.buscar(query='Python').all()
    assert len(resultados) == 2
    
    # Buscar por año
    resultados = Articulo.buscar(anio=2024).all()
    assert len(resultados) == 2
    
    # Buscar por LGAC
    resultados = Articulo.buscar(lgac_id=lgac.id).all()
    assert len(resultados) == 2
    
    # Buscar combinado
    resultados = Articulo.buscar(query='Python', anio=2024).all()
    assert len(resultados) == 1
    assert resultados[0].titulo == 'Deep Learning with Python'


def test_articulo_completitud(init_database):
    """Test: Cálculo de completitud del artículo."""
    tipo = TipoProduccion.query.first()
    # Crear un estado que no sea "Publicado" para no requerir campos adicionales
    estado = Estado(nombre='En preparación', activo=True)
    db.session.add(estado)
    db.session.commit()
    
    articulo = Articulo(
        titulo='Test Completitud',
        tipo_produccion_id=tipo.id,
        estado_id=estado.id,
        anio_publicacion=2024
    )
    
    db.session.add(articulo)
    db.session.commit()
    
    # Sin autores, debe estar incompleto
    completo = articulo.calcular_completitud()
    assert not completo
    assert articulo.completo == False
    
    # Agregar autor
    autor = Autor(nombre='Test', apellidos='Author')
    db.session.add(autor)
    db.session.commit()
    
    articulo.agregar_autor(autor)
    db.session.commit()
    
    # Ahora debe estar completo
    completo = articulo.calcular_completitud()
    assert completo
    assert articulo.completo == True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
