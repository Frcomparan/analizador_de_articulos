# Guía de Inicio Rápido

## 🚀 Comenzando con el Proyecto

Esta guía te ayudará a iniciar el proyecto desde cero.

---

## Paso 1: Verificar Requisitos

Asegúrate de tener instalado:

```powershell
# Python 3.9 o superior
python --version

# pip (gestor de paquetes)
pip --version

# Git (opcional pero recomendado)
git --version
```

---

## Paso 2: Configurar Entorno Virtual

```powershell
# Navegar al directorio del proyecto
cd "c:\Users\paco2\Documents\Maestria\Semestre 1\Tecnologias de programacion\analizador_articulos"

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Si hay error de permisos, ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Paso 3: Instalar Dependencias

```powershell
# Con el entorno virtual activado
pip install --upgrade pip
pip install -r requirements.txt
```

**Tiempo estimado**: 2-3 minutos

---

## Paso 4: Configurar Variables de Entorno

```powershell
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y configurar valores
# Por ahora, los valores por defecto son suficientes
```

---

## Paso 5: Inicializar Base de Datos

⚠️ **NOTA**: Antes de este paso, debes completar la implementación de los modelos en `app/models/`

```powershell
# Inicializar migraciones
flask db init

# Crear primera migración
flask db migrate -m "Initial migration"

# Aplicar migración
flask db upgrade

# Poblar catálogos (crear script primero)
python scripts/seed_catalogs.py
```

---

## Paso 6: Ejecutar Aplicación

```powershell
# Modo desarrollo
python run.py

# La aplicación estará disponible en:
# http://127.0.0.1:5000
```

---

## Estructura de Archivos Actual

```
analizador_articulos/
├── app/                          ✅ Creado
│   ├── __init__.py              ✅ Configurado
│   ├── models/                  ⏳ Pendiente implementar
│   ├── views/                   ⏳ Pendiente implementar
│   ├── controllers/             ⏳ Pendiente implementar
│   ├── services/                ⏳ Pendiente implementar
│   ├── templates/               ⏳ Pendiente implementar
│   ├── static/                  ✅ Creado
│   ├── forms/                   ✅ Creado
│   └── utils/                   ✅ Creado
├── docs/                        ✅ Documentación completa
│   ├── REQUISITOS.md           ✅
│   ├── DATABASE_DESIGN.md      ✅
│   ├── ARQUITECTURA.md         ✅
│   └── MVP_ROADMAP.md          ✅
├── migrations/                  ✅ Creado
├── uploads/                     ✅ Creado
├── exports/                     ✅ Creado
├── tests/                       ✅ Creado
├── config.py                    ✅ Configurado
├── requirements.txt             ✅ Completo
├── run.py                       ✅ Configurado
├── .env.example                 ✅ Creado
├── .gitignore                   ✅ Configurado
└── README.md                    ✅ Completo
```

---

## Próximos Pasos para Desarrollo

### 1. Implementar Modelos (Prioridad: ALTA)

Archivos a crear en `app/models/`:

- [x] `__init__.py` - Ya creado
- [ ] `articulo.py` - Modelo principal
- [ ] `autor.py` - Modelo de autores
- [ ] `revista.py` - Modelo de revistas
- [ ] `catalogs.py` - Modelos de catálogos (Estado, LGAC, etc.)
- [ ] `associations.py` - Tablas N:N

**Referencia**: Ver `docs/DATABASE_DESIGN.md`

### 2. Implementar Views (Blueprints)

Archivos a crear en `app/views/`:

- [x] `__init__.py` - Ya creado
- [ ] `main.py` - Rutas principales (/, /about)
- [ ] `articles.py` - CRUD de artículos
- [ ] `catalogs.py` - CRUD de catálogos
- [ ] `reports.py` - Exportación y reportes
- [ ] `uploads.py` - Upload de PDFs

**Referencia**: Ver `docs/ARQUITECTURA.md`

### 3. Implementar Controllers

Archivos a crear en `app/controllers/`:

- [x] `__init__.py` - Ya creado
- [ ] `article_controller.py`
- [ ] `catalog_controller.py`
- [ ] `report_controller.py`
- [ ] `upload_controller.py`

### 4. Implementar Services

Archivos a crear en `app/services/`:

- [x] `__init__.py` - Ya creado
- [ ] `pdf_service.py` - Extracción de PDFs
- [ ] `excel_service.py` - Generación de Excel
- [ ] `validation_service.py` - Validaciones
- [ ] `background_worker.py` - Tareas en background
- [ ] `file_handler.py` - Manejo de archivos

### 5. Crear Templates Base

Archivos a crear en `app/templates/`:

- [ ] `base.html` - Template principal con Bootstrap
- [ ] `index.html` - Página de inicio
- [ ] `articles/list.html`
- [ ] `articles/form.html`
- [ ] `articles/detail.html`

---

## Comandos Útiles

### Flask

```powershell
# Ver rutas disponibles
flask routes

# Abrir shell interactivo
flask shell

# Crear nueva migración
flask db migrate -m "Descripción"

# Aplicar migraciones
flask db upgrade

# Revertir migración
flask db downgrade
```

### Testing

```powershell
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app

# Test específico
pytest tests/test_models.py
```

### Git

```powershell
# Inicializar repositorio
git init

# Primer commit
git add .
git commit -m "Initial project setup"

# Ver estado
git status

# Ver log
git log --oneline
```

---

## Recursos de Apoyo

### Documentación

- **Flask**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.3/
- **PyPDF2**: https://pypdf2.readthedocs.io/

### Tutoriales Recomendados

1. Flask Mega-Tutorial (Miguel Grinberg)
2. SQLAlchemy ORM Tutorial
3. Bootstrap 5 Crash Course

---

## Troubleshooting

### Error: "Module not found"

```powershell
# Verificar que el entorno virtual esté activo
# Debe aparecer (venv) al inicio del prompt

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Database locked"

```powershell
# Cerrar todas las conexiones a la base de datos
# Reiniciar la aplicación
```

### Error: "ImportError" en blueprints

```powershell
# Los blueprints aún no existen, normal en fase inicial
# Se resolverá al crear los archivos en app/views/
```

---

## Checklist de Inicio

Antes de comenzar a programar:

- [x] ✅ Entorno virtual creado y activado
- [ ] ⏳ Dependencias instaladas
- [ ] ⏳ Base de datos inicializada
- [ ] ⏳ Primer modelo creado
- [ ] ⏳ Primera migración aplicada
- [ ] ⏳ Aplicación ejecutándose sin errores

---

## Contacto y Soporte

Para dudas sobre el proyecto:

1. Revisar documentación en `docs/`
2. Consultar `MVP_ROADMAP.md` para orden de implementación
3. Revisar `ARQUITECTURA.md` para patrones de código

---

**¡Éxito con el proyecto! 🚀**

Última actualización: Diciembre 2025
