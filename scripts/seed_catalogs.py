"""
Script para poblar los catálogos iniciales del sistema.
Ejecutar después de crear las tablas de la base de datos.

Uso:
    flask seed-catalogs
    o
    python scripts/seed_catalogs.py
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import (
    TipoProduccion, Proposito, Estado, LGAC, Indexacion, Pais
)


def seed_tipos_produccion():
    """Pobla el catálogo de tipos de producción académica."""
    tipos = [
        {'nombre': 'Arbitrado', 'descripcion': "Artículo revisado por pares"},
        {'nombre': 'Divulgación y Difusión', 'descripcion': "Artículo de divulgación científica"},
        {'nombre': 'Indexado', 'descripcion': "Artículo en revista indexada"},
        {'nombre': 'Memorias en extenso', 'descripcion': "Artículo completo en memorias de congresos"},
    ]
    
    for t in tipos:
        if not TipoProduccion.query.filter_by(nombre=t['nombre']).first():
            db.session.add(TipoProduccion(**t))
    
    print(f"✓ Tipos de producción: {len(tipos)} registros")


def seed_propositos():
    """Pobla el catálogo de propósitos del artículo."""
    propositos = [
        {'nombre': 'Investigación aplicada', 'descripcion': 'Investigación orientada a resolver problemas específicos'},
        {'nombre': 'Desarrollo tecnológico', 'descripcion': 'Desarrollo de nuevas tecnologías o mejoras'},
    ]
    
    for p in propositos:
        if not Proposito.query.filter_by(nombre=p['nombre']).first():
            db.session.add(Proposito(**p))
    
    print(f"✓ Propósitos: {len(propositos)} registros")


def seed_estados():
    """Pobla el catálogo de estados del artículo."""
    estados = [
        {'nombre': 'Aceptado', 'color': "#80108f"},            # Verde claro
        {'nombre': 'Publicado', 'color': '#28a745'},           # Verde
    ]
    
    for e in estados:
        if not Estado.query.filter_by(nombre=e['nombre']).first():
            db.session.add(Estado(**e))
    
    print(f"✓ Estados: {len(estados)} registros")


def seed_lgac():
    """
    Pobla el catálogo de LGAC.
    NOTA: Estas son líneas de ejemplo. Deben personalizarse según el CA específico.
    """
    lgacs = [
        {'nombre': 'Tecnologías emergentes y desarrollo web', 
         'descripcion': 'Estudio y aplicación de nuevas tecnologías en el desarrollo de aplicaciones web.'},
    ]
    
    for l in lgacs:
        if not LGAC.query.filter_by(nombre=l['nombre']).first():
            db.session.add(LGAC(**l))
    
    print(f"✓ LGAC: {len(lgacs)} registros (PERSONALIZAR según el CA)")


def seed_indexaciones():
    """Pobla el catálogo de bases de datos de indexación."""
    indexaciones = [
        {'nombre': 'Web of Science', 'acronimo': 'WoS', 'prestigio': 5,
         'url': 'https://www.webofscience.com'},
        {'nombre': 'Scopus', 'acronimo': 'Scopus', 'prestigio': 5,
         'url': 'https://www.scopus.com'},
        {'nombre': 'Journal Citation Reports', 'acronimo': 'JCR', 'prestigio': 5,
         'url': 'https://jcr.clarivate.com'},
        {'nombre': 'SciELO', 'acronimo': 'SciELO', 'prestigio': 4,
         'url': 'https://scielo.org'},
        {'nombre': 'Latindex Catálogo 2.0', 'acronimo': 'Latindex', 'prestigio': 3,
         'url': 'https://www.latindex.org'},
        {'nombre': 'DOAJ', 'acronimo': 'DOAJ', 'prestigio': 3,
         'url': 'https://doaj.org'},
        {'nombre': 'Redalyc', 'acronimo': 'Redalyc', 'prestigio': 3,
         'url': 'https://www.redalyc.org'},
        {'nombre': 'CONACYT (Padrón)', 'acronimo': 'CONACYT', 'prestigio': 4,
         'url': 'https://www.conacyt.gob.mx'},
        {'nombre': 'PubMed', 'acronimo': 'PubMed', 'prestigio': 5,
         'url': 'https://pubmed.ncbi.nlm.nih.gov'},
        {'nombre': 'IEEE Xplore', 'acronimo': 'IEEE', 'prestigio': 4,
         'url': 'https://ieeexplore.ieee.org'},
        {'nombre': 'ACM Digital Library', 'acronimo': 'ACM', 'prestigio': 4,
         'url': 'https://dl.acm.org'},
        {'nombre': 'SpringerLink', 'acronimo': 'Springer', 'prestigio': 4,
         'url': 'https://link.springer.com'},
        {'nombre': 'EBSCO', 'acronimo': 'EBSCO', 'prestigio': 3,
         'url': 'https://www.ebsco.com'},
    ]
    
    for i in indexaciones:
        if not Indexacion.query.filter_by(nombre=i['nombre']).first():
            db.session.add(Indexacion(**i))
    
    print(f"✓ Indexaciones: {len(indexaciones)} registros")


def seed_paises():
    """Pobla el catálogo de países más comunes en publicaciones académicas."""
    paises = [
        {'nombre': 'México', 'codigo_iso': 'MEX'},
        {'nombre': 'Estados Unidos', 'codigo_iso': 'USA'},
        {'nombre': 'España', 'codigo_iso': 'ESP'},
        {'nombre': 'Reino Unido', 'codigo_iso': 'GBR'},
        {'nombre': 'Alemania', 'codigo_iso': 'DEU'},
        {'nombre': 'Francia', 'codigo_iso': 'FRA'},
        {'nombre': 'Italia', 'codigo_iso': 'ITA'},
        {'nombre': 'Brasil', 'codigo_iso': 'BRA'},
        {'nombre': 'Argentina', 'codigo_iso': 'ARG'},
        {'nombre': 'Chile', 'codigo_iso': 'CHL'},
        {'nombre': 'Colombia', 'codigo_iso': 'COL'},
        {'nombre': 'Perú', 'codigo_iso': 'PER'},
        {'nombre': 'Canadá', 'codigo_iso': 'CAN'},
        {'nombre': 'Países Bajos', 'codigo_iso': 'NLD'},
        {'nombre': 'Suiza', 'codigo_iso': 'CHE'},
        {'nombre': 'China', 'codigo_iso': 'CHN'},
        {'nombre': 'Japón', 'codigo_iso': 'JPN'},
        {'nombre': 'Australia', 'codigo_iso': 'AUS'},
        {'nombre': 'India', 'codigo_iso': 'IND'},
        {'nombre': 'Cuba', 'codigo_iso': 'CUB'},
    ]
    
    for p in paises:
        if not Pais.query.filter_by(nombre=p['nombre']).first():
            db.session.add(Pais(**p))
    
    print(f"✓ Países: {len(paises)} registros")


def seed_all():
    """Ejecuta todos los seeds en orden."""
    print("\n=== Poblando catálogos iniciales ===\n")
    
    seed_tipos_produccion()
    seed_propositos()
    seed_estados()
    seed_lgac()
    seed_indexaciones()
    seed_paises()
    
    db.session.commit()
    print("\n✓ Todos los catálogos han sido poblados correctamente.")
    print("  NOTA: Recuerda personalizar las LGAC según tu Cuerpo Académico.\n")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_all()
