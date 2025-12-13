"""
Configuración compartida para tests.
"""
import pytest
from app import create_app, db
from app.models import (
    TipoProduccion, Estado, LGAC, Proposito, 
    Pais, Indexacion
)


@pytest.fixture
def app():
    """Crea la aplicación para testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Desactiva CSRF para tests
    app.config['SECRET_KEY'] = 'test-secret-key'
    
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
def db_session(app):
    """Sesión de base de datos para testing."""
    with app.app_context():
        yield db.session


@pytest.fixture
def catalogs(app, db_session):
    """Crea catálogos básicos para testing."""
    # Tipo de producción
    tipo = TipoProduccion.query.filter_by(nombre='Artículo científico').first()
    if not tipo:
        tipo = TipoProduccion(nombre='Artículo científico', activo=True)
        db_session.add(tipo)
        
    tipo_conf = TipoProduccion.query.filter_by(nombre='Conference paper').first()
    if not tipo_conf:
        tipo_conf = TipoProduccion(nombre='Conference paper', activo=True)
        db_session.add(tipo_conf)
        
    # Estado
    estado_pub = Estado.query.filter_by(nombre='Publicado').first()
    if not estado_pub:
        estado_pub = Estado(nombre='Publicado', color='#28a745', activo=True)
        db_session.add(estado_pub)
        
    estado_env = Estado.query.filter_by(nombre='Enviado').first()
    if not estado_env:
        estado_env = Estado(nombre='Enviado', color='#ffc107', activo=True)
        db_session.add(estado_env)
        
    # LGAC
    lgac = LGAC.query.filter_by(nombre='LGAC de prueba').first()
    if not lgac:
        lgac = LGAC(nombre='LGAC de prueba', activo=True)
        db_session.add(lgac)
        
    # Propósito
    proposito = Proposito.query.filter_by(nombre='Investigación básica').first()
    if not proposito:
        proposito = Proposito(nombre='Investigación básica', activo=True)
        db_session.add(proposito)
        
    # País
    pais = Pais.query.filter_by(nombre='México').first()
    if not pais:
        pais = Pais(nombre='México', codigo_iso='MEX', activo=True)
        db_session.add(pais)
        
    # Indexación
    indexacion = Indexacion.query.filter_by(nombre='Scopus').first()
    if not indexacion:
        indexacion = Indexacion(nombre='Scopus', acronimo='Scopus', prestigio=5, activo=True)
        db_session.add(indexacion)
    
    db_session.commit()
    
    return {
        'tipo': tipo,
        'estado': estado_pub,
        'lgac': lgac,
        'proposito': proposito,
        'pais': pais,
        'indexacion': indexacion
    }


@pytest.fixture
def init_database(app):
    """Inicializa la base de datos con datos de prueba (compatibilidad con test_models.py)."""
    with app.app_context():
        # Crear catálogos básicos (get_or_create para evitar duplicados)
        tipo = TipoProduccion.query.filter_by(nombre='Artículo científico').first()
        if not tipo:
            tipo = TipoProduccion(nombre='Artículo científico', activo=True)
            db.session.add(tipo)
            
        estado = Estado.query.filter_by(nombre='Publicado').first()
        if not estado:
            estado = Estado(nombre='Publicado', color='#28a745', activo=True)
            db.session.add(estado)
            
        lgac = LGAC.query.filter_by(nombre='LGAC de prueba').first()
        if not lgac:
            lgac = LGAC(nombre='LGAC de prueba', activo=True)
            db.session.add(lgac)
            
        proposito = Proposito.query.filter_by(nombre='Investigación básica').first()
        if not proposito:
            proposito = Proposito(nombre='Investigación básica', activo=True)
            db.session.add(proposito)
            
        pais = Pais.query.filter_by(nombre='México').first()
        if not pais:
            pais = Pais(nombre='México', codigo_iso='MEX', activo=True)
            db.session.add(pais)
            
        indexacion = Indexacion.query.filter_by(nombre='Scopus').first()
        if not indexacion:
            indexacion = Indexacion(nombre='Scopus', acronimo='Scopus', prestigio=5, activo=True)
            db.session.add(indexacion)
        
        db.session.commit()
        
        yield db
        
        db.session.rollback()
