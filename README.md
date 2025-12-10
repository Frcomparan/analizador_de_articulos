# Sistema de Gestión de Artículos Académicos

## Descripción General

Aplicación web local desarrollada en Python con Flask para el registro, consulta y gestión de artículos académicos de un Cuerpo Académico. El sistema minimiza la captura manual mediante extracción automática de información desde archivos PDF y cartas de aceptación.

## Características Principales

- **Captura Mínima**: Extracción automática de metadatos desde PDFs y cartas de aceptación
- **Gestión Completa**: Registro, consulta, edición y eliminación de artículos
- **Filtrado Avanzado**: Por año, estado, LGAC y otros campos
- **Exportación a Excel**: Compatible con formato institucional
- **Procesamiento en Background**: Tareas automáticas sin bloquear la interfaz
- **Arquitectura MVC**: Código organizado y mantenible

## Tecnologías

- **Framework Web**: Flask 3.0+
- **ORM**: SQLAlchemy 2.0+
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción opcional)
- **Procesamiento PDF**: PyPDF2, pdfplumber
- **Exportación**: openpyxl
- **Concurrencia**: threading (hilo en background)
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap 5)

## Requisitos del Sistema

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Edge)

## Instalación Rápida

```bash
# Clonar o descargar el proyecto
cd analizador_articulos

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos
flask db upgrade

# Ejecutar aplicación
python run.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Estructura del Proyecto

```
analizador_articulos/
├── app/
│   ├── __init__.py           # Inicialización de Flask
│   ├── models/               # Modelos de datos (ORM)
│   ├── controllers/          # Lógica de negocio
│   ├── views/                # Rutas y endpoints
│   ├── services/             # Servicios auxiliares
│   ├── templates/            # Plantillas HTML
│   ├── static/               # CSS, JS, imágenes
│   └── utils/                # Utilidades
├── migrations/               # Migraciones de BD
├── uploads/                  # Archivos subidos
├── exports/                  # Archivos exportados
├── config.py                 # Configuración
├── requirements.txt          # Dependencias
└── run.py                    # Punto de entrada
```

## Casos de Uso Principales

### 1. Registro de Artículo

1. Usuario sube PDF o carta de aceptación
2. Sistema extrae automáticamente: título, autores, año, revista
3. Usuario completa campos faltantes
4. Sistema valida y guarda

### 2. Consulta y Filtrado

1. Usuario accede a la lista de artículos
2. Aplica filtros (año, estado, LGAC)
3. Visualiza resultados en tabla
4. Puede editar o eliminar registros

### 3. Exportación

1. Usuario solicita exportación
2. Sistema genera Excel con formato institucional
3. Descarga automática del archivo

### 4. Procesamiento Automático

1. Hilo en background detecta artículos incompletos
2. Notifica al usuario
3. Genera reportes periódicos

## Modelo de Datos

### Tablas Principales

- **articulos**: Información de cada artículo
- **autores**: Catálogo de autores
- **revistas**: Catálogo de revistas
- **tipos_produccion**: Catálogo de tipos
- **estados**: Catálogo de estados
- **lgac**: Líneas de Generación y Aplicación del Conocimiento
- **paises**: Catálogo de países
- **indexaciones**: Tipos de indexación (Scopus, WoS, etc.)

### Relaciones

- Artículo ↔ Autores (N:N)
- Artículo → Revista (N:1)
- Artículo → Tipo Producción (N:1)
- Artículo → Estado (N:1)
- Artículo → LGAC (N:1)
- Revista → País (N:1)
- Revista ↔ Indexaciones (N:N)

## Roadmap de Desarrollo

### Fase 1: MVP Base (2 semanas)

- [ ] Configuración inicial del proyecto
- [ ] Modelos de base de datos
- [ ] CRUD básico de artículos
- [ ] Interfaz web simple

### Fase 2: Extracción Automática (2 semanas)

- [ ] Upload de archivos PDF
- [ ] Extracción de metadatos
- [ ] Pre-llenado de formularios

### Fase 3: Funcionalidades Avanzadas (2 semanas)

- [ ] Sistema de filtrado
- [ ] Exportación a Excel
- [ ] Validaciones completas

### Fase 4: Concurrencia y Optimización (1 semana)

- [ ] Hilo en background
- [ ] Detección de artículos incompletos
- [ ] Optimización de rendimiento

## Contribución

Este es un proyecto académico. Para modificaciones:

1. Documentar cambios en el código
2. Seguir convenciones de nombrado
3. Actualizar documentación si es necesario

## Licencia

Proyecto académico - Uso educativo

## Contacto

Proyecto desarrollado para el Cuerpo Académico - Maestría en Tecnologías de Programación

---

**Versión**: 1.0.0 (MVP)  
**Última actualización**: Diciembre 2025
