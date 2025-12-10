# Arquitectura del Sistema - MVC

## Visión General

El sistema utiliza el patrón **MVC (Model-View-Controller)** organizado por **módulos funcionales**, donde cada módulo representa un área específica de la aplicación (artículos, catálogos, reportes, etc.).

```
┌─────────────────────────────────────────────────────────────┐
│                        NAVEGADOR WEB                        │
│                  (HTML, CSS, JavaScript)                    │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP Request/Response
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      FLASK APPLICATION                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    VIEWS LAYER                        │  │
│  │  (Blueprints - Rutas y Endpoints)                     │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐     │  │
│  │  │Articles│  │Catalogs│  │Reports │  │Upload  │     │  │
│  │  │ Routes │  │ Routes │  │ Routes │  │ Routes │     │  │
│  │  └────┬───┘  └────┬───┘  └────┬───┘  └────┬───┘     │  │
│  └───────┼───────────┼───────────┼───────────┼─────────┘  │
│          │           │           │           │             │
│          ▼           ▼           ▼           ▼             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                 CONTROLLERS LAYER                     │  │
│  │  (Lógica de Negocio)                                  │  │
│  │  ┌────────────┐  ┌─────────────┐  ┌────────────┐    │  │
│  │  │  Article   │  │  Catalog    │  │  Report    │    │  │
│  │  │ Controller │  │ Controller  │  │ Controller │    │  │
│  │  └─────┬──────┘  └──────┬──────┘  └─────┬──────┘    │  │
│  └────────┼────────────────┼────────────────┼───────────┘  │
│           │                │                │               │
│           ▼                ▼                ▼               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   SERVICES LAYER                      │  │
│  │  (Servicios Auxiliares)                               │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐     │  │
│  │  │  PDF   │  │ Excel  │  │ Email  │  │Background   │  │
│  │  │Service │  │Service │  │Service │  │ Worker  │     │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘     │  │
│  └───────────────────────────────────────────────────────┘  │
│           │                                                  │
│           ▼                                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    MODELS LAYER                       │  │
│  │  (SQLAlchemy ORM - Entidades de Base de Datos)       │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐     │  │
│  │  │Articulo│  │ Autor  │  │Revista │  │Catálogos    │  │
│  │  │ Model  │  │ Model  │  │ Model  │  │  Models │    │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘     │  │
│  └───────────────────────────┬───────────────────────────┘  │
└────────────────────────────────┬───────────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   DATABASE (SQLite)     │
                    │  articulos.db           │
                    └─────────────────────────┘
```

---

## Estructura de Directorios

```
analizador_articulos/
│
├── app/                              # Aplicación principal
│   ├── __init__.py                   # Factory pattern para crear app
│   │
│   ├── models/                       # MODELOS (M)
│   │   ├── __init__.py
│   │   ├── articulo.py               # Modelo Artículo
│   │   ├── autor.py                  # Modelo Autor
│   │   ├── revista.py                # Modelo Revista
│   │   ├── catalogs.py               # Modelos de catálogos
│   │   └── associations.py           # Tablas de asociación N:N
│   │
│   ├── views/                        # VISTAS (V) - Blueprints
│   │   ├── __init__.py
│   │   ├── main.py                   # Rutas principales (home, about)
│   │   ├── articles.py               # Rutas de artículos
│   │   ├── catalogs.py               # Rutas de catálogos
│   │   ├── reports.py                # Rutas de reportes
│   │   └── uploads.py                # Rutas de subida de archivos
│   │
│   ├── controllers/                  # CONTROLADORES (C)
│   │   ├── __init__.py
│   │   ├── article_controller.py     # Lógica de artículos
│   │   ├── catalog_controller.py     # Lógica de catálogos
│   │   ├── report_controller.py      # Lógica de reportes
│   │   └── upload_controller.py      # Lógica de uploads
│   │
│   ├── services/                     # Servicios auxiliares
│   │   ├── __init__.py
│   │   ├── pdf_service.py            # Extracción de PDFs
│   │   ├── excel_service.py          # Generación de Excel
│   │   ├── validation_service.py     # Validaciones
│   │   ├── background_worker.py      # Tareas en background
│   │   └── file_handler.py           # Manejo de archivos
│   │
│   ├── templates/                    # Templates HTML (Jinja2)
│   │   ├── base.html                 # Template base
│   │   ├── index.html                # Página principal
│   │   │
│   │   ├── articles/                 # Templates de artículos
│   │   │   ├── list.html             # Lista de artículos
│   │   │   ├── form.html             # Formulario crear/editar
│   │   │   ├── detail.html           # Detalle de artículo
│   │   │   └── upload.html           # Upload de PDF
│   │   │
│   │   ├── catalogs/                 # Templates de catálogos
│   │   │   ├── list.html             # Lista genérica
│   │   │   └── form.html             # Formulario genérico
│   │   │
│   │   └── reports/                  # Templates de reportes
│   │       ├── dashboard.html        # Dashboard
│   │       └── export.html           # Exportación
│   │
│   ├── static/                       # Archivos estáticos
│   │   ├── css/
│   │   │   ├── main.css              # Estilos principales
│   │   │   └── forms.css             # Estilos de formularios
│   │   │
│   │   ├── js/
│   │   │   ├── main.js               # JavaScript principal
│   │   │   ├── forms.js              # Validaciones de formularios
│   │   │   └── filters.js            # Filtros dinámicos
│   │   │
│   │   └── images/                   # Imágenes
│   │
│   ├── utils/                        # Utilidades generales
│   │   ├── __init__.py
│   │   ├── validators.py             # Validadores personalizados
│   │   ├── helpers.py                # Funciones auxiliares
│   │   └── constants.py              # Constantes de la app
│   │
│   └── forms/                        # Formularios Flask-WTF
│       ├── __init__.py
│       ├── article_form.py           # Formulario de artículo
│       ├── author_form.py            # Formulario de autor
│       └── catalog_form.py           # Formularios de catálogos
│
├── migrations/                       # Migraciones de BD (Alembic)
│   └── versions/
│
├── uploads/                          # Archivos subidos
│   └── pdfs/
│
├── exports/                          # Archivos exportados
│   └── excel/
│
├── tests/                            # Tests unitarios
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_controllers.py
│   └── test_services.py
│
├── docs/                             # Documentación
│   ├── REQUISITOS.md
│   ├── DATABASE_DESIGN.md
│   └── ARQUITECTURA.md
│
├── config.py                         # Configuración de la app
├── requirements.txt                  # Dependencias
├── run.py                            # Punto de entrada
├── .env.example                      # Variables de entorno ejemplo
├── .gitignore                        # Archivos ignorados por Git
└── README.md                         # Documentación principal
```

---

## Capas del Sistema

### 1. MODELS (Modelos) - Capa de Datos

**Responsabilidad**: Representar la estructura de la base de datos y lógica de persistencia.

**Tecnología**: SQLAlchemy ORM

**Ejemplo**: `app/models/articulo.py`

```python
from app import db
from datetime import datetime

class Articulo(db.Model):
    __tablename__ = 'articulos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(500), nullable=False)
    año = db.Column(db.Integer, nullable=False)

    # Relaciones
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipos_produccion.id'))
    tipo = db.relationship('TipoProduccion', backref='articulos')

    # Métodos del modelo
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'año': self.año
        }

    def __repr__(self):
        return f'<Articulo {self.titulo}>'
```

**Características**:

- Define estructura de tablas
- Relaciones entre entidades
- Métodos auxiliares (to_dict, validaciones)
- No contiene lógica de negocio compleja

---

### 2. VIEWS (Vistas) - Capa de Presentación

**Responsabilidad**: Definir rutas (endpoints) y renderizar templates.

**Tecnología**: Flask Blueprints + Jinja2

**Ejemplo**: `app/views/articles.py`

```python
from flask import Blueprint, render_template, request, redirect, url_for
from app.controllers.article_controller import ArticleController

articles_bp = Blueprint('articles', __name__, url_prefix='/articles')

@articles_bp.route('/')
def list():
    """Lista todos los artículos"""
    filters = request.args.to_dict()
    result = ArticleController.get_all(filters)
    return render_template('articles/list.html', articles=result)

@articles_bp.route('/new', methods=['GET', 'POST'])
def create():
    """Crea un nuevo artículo"""
    if request.method == 'POST':
        data = request.form.to_dict()
        article = ArticleController.create(data)
        return redirect(url_for('articles.detail', id=article.id))
    return render_template('articles/form.html')
```

**Características**:

- Blueprints modulares por funcionalidad
- Maneja requests HTTP
- Delega lógica a Controllers
- Retorna respuestas (HTML, JSON)

---

### 3. CONTROLLERS (Controladores) - Capa de Lógica de Negocio

**Responsabilidad**: Procesar peticiones, aplicar reglas de negocio, coordinar Models y Services.

**Tecnología**: Python puro

**Ejemplo**: `app/controllers/article_controller.py`

```python
from app.models.articulo import Articulo
from app.services.pdf_service import PDFService
from app.services.validation_service import ValidationService
from app import db

class ArticleController:

    @staticmethod
    def create(data):
        """Crea un nuevo artículo"""
        # Validar datos
        ValidationService.validate_article(data)

        # Crear instancia
        article = Articulo(
            titulo=data['titulo'],
            año=data['año']
        )

        # Guardar en BD
        db.session.add(article)
        db.session.commit()

        return article

    @staticmethod
    def get_all(filters=None):
        """Obtiene artículos con filtros"""
        query = Articulo.query.filter_by(deleted_at=None)

        if filters and filters.get('año'):
            query = query.filter_by(año=filters['año'])

        return query.all()

    @staticmethod
    def process_pdf(article_id, pdf_file):
        """Procesa PDF y actualiza artículo"""
        # Extraer metadatos
        metadata = PDFService.extract_metadata(pdf_file)

        # Actualizar artículo
        article = Articulo.query.get(article_id)
        article.titulo = metadata.get('titulo', article.titulo)
        article.doi = metadata.get('doi', article.doi)

        db.session.commit()
        return article
```

**Características**:

- Métodos estáticos (sin estado)
- Valida datos de entrada
- Coordina múltiples Services
- Maneja transacciones de BD
- Lógica de negocio centralizada

---

### 4. SERVICES (Servicios) - Capa de Utilidades

**Responsabilidad**: Funcionalidades específicas y reutilizables.

**Tecnología**: Python + librerías especializadas

**Ejemplo**: `app/services/pdf_service.py`

```python
import PyPDF2
import re

class PDFService:

    @staticmethod
    def extract_metadata(pdf_path):
        """Extrae metadatos de un PDF"""
        metadata = {}

        with open(pdf_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            text = pdf.pages[0].extract_text()

            # Extraer título (primeras líneas)
            lines = text.split('\n')
            metadata['titulo'] = lines[0] if lines else None

            # Extraer DOI
            doi_pattern = r'10\.\d{4,}/[\S]+'
            doi_match = re.search(doi_pattern, text)
            if doi_match:
                metadata['doi'] = doi_match.group()

            # Extraer año
            year_pattern = r'\b(19|20)\d{2}\b'
            year_match = re.search(year_pattern, text)
            if year_match:
                metadata['año'] = int(year_match.group())

        return metadata
```

**Otros servicios**:

- `ExcelService`: Generación de reportes Excel
- `ValidationService`: Validaciones complejas
- `BackgroundWorker`: Tareas en segundo plano
- `FileHandler`: Gestión de archivos subidos

---

### 5. TEMPLATES (Plantillas HTML)

**Responsabilidad**: Presentación visual al usuario.

**Tecnología**: Jinja2

**Ejemplo**: `app/templates/articles/list.html`

```html
{% extends "base.html" %} {% block title %}Artículos{% endblock %} {% block
content %}
<div class="container">
  <h1>Lista de Artículos</h1>

  <!-- Filtros -->
  <form method="GET" class="mb-4">
    <input type="number" name="año" placeholder="Año" />
    <button type="submit">Filtrar</button>
  </form>

  <!-- Tabla -->
  <table class="table">
    <thead>
      <tr>
        <th>Título</th>
        <th>Año</th>
        <th>Estado</th>
        <th>Acciones</th>
      </tr>
    </thead>
    <tbody>
      {% for article in articles %}
      <tr>
        <td>{{ article.titulo }}</td>
        <td>{{ article.año }}</td>
        <td>
          <span
            class="badge"
            style="background-color: {{ article.estado.color }}"
          >
            {{ article.estado.nombre }}
          </span>
        </td>
        <td>
          <a href="{{ url_for('articles.detail', id=article.id) }}">Ver</a>
          <a href="{{ url_for('articles.edit', id=article.id) }}">Editar</a>
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
```

---

## Flujo de una Request

### Ejemplo: Crear un artículo con PDF

```
1. Usuario sube formulario con PDF
   ↓
2. VIEW (articles.py): Recibe POST /articles/new
   ↓
3. CONTROLLER (article_controller.py):
   - Valida datos del formulario
   - Guarda PDF en /uploads
   ↓
4. SERVICE (pdf_service.py):
   - Extrae metadatos del PDF
   - Retorna diccionario con datos
   ↓
5. CONTROLLER (article_controller.py):
   - Crea instancia de Articulo
   - Completa con metadatos extraídos
   ↓
6. MODEL (articulo.py):
   - SQLAlchemy persiste en BD
   ↓
7. CONTROLLER:
   - Retorna objeto Articulo creado
   ↓
8. VIEW:
   - Redirige a detalle del artículo
   ↓
9. TEMPLATE:
   - Renderiza HTML de confirmación
   ↓
10. BROWSER:
    - Muestra página al usuario
```

---

## Hilo en Background

### Implementación

**Archivo**: `app/services/background_worker.py`

```python
import threading
import time
from app.models.articulo import Articulo
from app import db

class BackgroundWorker:

    def __init__(self, app):
        self.app = app
        self.running = False
        self.thread = None

    def start(self):
        """Inicia el hilo en background"""
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        """Detiene el hilo"""
        self.running = False

    def _run(self):
        """Loop principal del worker"""
        while self.running:
            with self.app.app_context():
                self._check_incomplete_articles()

            # Esperar 1 hora
            time.sleep(3600)

    def _check_incomplete_articles(self):
        """Detecta artículos incompletos"""
        incomplete = Articulo.query.filter(
            (Articulo.doi == None) | (Articulo.descripcion == None)
        ).all()

        if incomplete:
            print(f"Se encontraron {len(incomplete)} artículos incompletos")
            # Aquí se puede enviar notificación, generar reporte, etc.
```

**Inicialización en `run.py`**:

```python
from app import create_app
from app.services.background_worker import BackgroundWorker

app = create_app()
worker = BackgroundWorker(app)
worker.start()

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Ventajas de esta Arquitectura

✅ **Separación de responsabilidades**: Cada capa tiene un propósito claro  
✅ **Testeable**: Controllers y Services se pueden testear independientemente  
✅ **Escalable**: Fácil agregar nuevos módulos  
✅ **Mantenible**: Código organizado y fácil de ubicar  
✅ **Reutilizable**: Services pueden usarse en múltiples Controllers  
✅ **Flask idiomático**: Usa Blueprints, Factory pattern

---

## Convenciones de Código

- **Nombres de archivos**: snake_case (`article_controller.py`)
- **Nombres de clases**: PascalCase (`ArticleController`)
- **Nombres de funciones**: snake_case (`get_all()`)
- **Blueprints**: Plural (`articles_bp`)
- **Templates**: Estructura por módulo (`articles/list.html`)
- **Imports**: Absolutos desde `app` (`from app.models.articulo import Articulo`)
