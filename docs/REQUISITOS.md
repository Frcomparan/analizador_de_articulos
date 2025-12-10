# Especificación de Requisitos del Sistema

## 1. Requisitos Funcionales

### RF-001: Registro de Artículos

**Prioridad**: Alta  
**Descripción**: El sistema debe permitir registrar artículos académicos minimizando la captura manual.

**Criterios de aceptación**:

- Usuario puede subir archivo PDF (artículo o carta de aceptación)
- Sistema extrae automáticamente: título, autores, año, revista, DOI
- Usuario completa campos no extraídos
- Sistema valida datos antes de guardar
- Genera timestamp de registro

**Campos a capturar** (según Excel institucional):

- Tipo de producción (catálogo)
- Título del artículo
- Autor(es) participante(s)
- Registro del autor
- Título de la revista
- Editorial
- ISSN
- Volumen, número
- Páginas (inicio-fin)
- Año de publicación
- País
- LGAC
- Indexación (Scopus, WoS, etc.)
- Estado actual
- Descripción
- Dirección electrónica del artículo
- Propósito del artículo (catálogo)
- Considera para curriculum del CA (Sí/No)
- Nombre del congreso (si aplica)

### RF-002: Extracción Automática de Metadatos

**Prioridad**: Alta  
**Descripción**: Extraer información desde archivos PDF para prellenar formularios.

**Criterios de aceptación**:

- Reconoce y extrae título del artículo
- Identifica nombres de autores
- Detecta año de publicación
- Extrae DOI si está disponible
- Identifica nombre de revista
- Extrae ISSN si está presente
- Maneja casos donde no se encuentra información

**Técnicas**:

- Extracción de texto con PyPDF2/pdfplumber
- Expresiones regulares para patrones comunes
- Búsqueda de palabras clave (Abstract, Introduction, References)

### RF-003: Gestión de Catálogos

**Prioridad**: Alta  
**Descripción**: Administrar catálogos maestros del sistema.

**Catálogos requeridos**:

1. **Tipos de Producción**: Artículo científico, Artículo de divulgación, Review, Conference paper, etc.
2. **Propósitos**: Investigación básica, Investigación aplicada, Desarrollo tecnológico, Divulgación, etc.
3. **Estados**: En revisión, Aceptado, Publicado, Rechazado
4. **LGAC**: Líneas de investigación del Cuerpo Académico
5. **Indexaciones**: Scopus, Web of Science, SciELO, Latindex, etc.
6. **Países**: Catálogo de países de publicación
7. **Autores**: Registro de investigadores del CA
8. **Revistas**: Revistas donde se ha publicado

**Operaciones**:

- Crear nuevo registro en catálogo
- Editar registro existente
- Desactivar (no eliminar) registros
- Listar registros activos

### RF-004: Consulta y Filtrado

**Prioridad**: Alta  
**Descripción**: Visualizar y filtrar artículos registrados.

**Criterios de aceptación**:

- Vista de tabla con todos los artículos
- Paginación (20 registros por página)
- Ordenamiento por columnas
- Filtros disponibles:
  - Año de publicación (rango)
  - Estado actual
  - LGAC
  - Autor
  - Tipo de producción
  - Propósito del artículo
  - Indexación
  - Para curriculum (Sí/No)
- Búsqueda por texto libre (título, revista)
- Indicadores visuales (badges) para estados

### RF-005: Edición de Artículos

**Prioridad**: Media  
**Descripción**: Modificar información de artículos existentes.

**Criterios de aceptación**:

- Formulario pre-llenado con datos actuales
- Validación de campos requeridos
- Historial de cambios (timestamp)
- Confirmación antes de guardar

### RF-006: Eliminación de Artículos

**Prioridad**: Media  
**Descripción**: Eliminar artículos del sistema.

**Criterios de aceptación**:

- Confirmación obligatoria antes de eliminar
- Eliminación lógica (soft delete) con campo `deleted_at`
- Opción de restaurar artículos eliminados
- No mostrar artículos eliminados en consultas normales

### RF-007: Exportación a Excel

**Prioridad**: Alta  
**Descripción**: Exportar artículos al formato Excel institucional.

**Criterios de aceptación**:

- Genera archivo .xlsx con estructura exacta del template
- Respeta columnas y orden del Excel proporcionado
- Incluye todos los artículos o solo filtrados
- Columnas vacías permitidas
- Nombre de archivo con timestamp
- Descarga automática al navegador

**Columnas del Excel**:

1. Tipo de producción
2. Título del artículo
3. Autor(es) participante(s)
4. Registro del autor
5. Título de la revista
6. Editorial
7. ISSN
8. Volumen
9. Número
10. Página inicial
11. Página final
12. Año
13. País
14. LGAC
15. Indexación
16. Estado actual
17. Descripción
18. Dirección electrónica
19. Propósito del artículo
20. Considera para curriculum del CA
21. Nombre del congreso

### RF-008: Procesamiento en Background

**Prioridad**: Media  
**Descripción**: Ejecutar tareas automáticas sin bloquear la interfaz.

**Tareas programadas**:

1. **Detección de artículos incompletos** (cada 1 hora)

   - Identifica artículos con campos vacíos críticos
   - Genera lista de alertas
   - Registra en log

2. **Generación de reportes** (bajo demanda)
   - Crea Excel sin bloquear UI
   - Notifica cuando está listo
   - Limpia archivos antiguos (>7 días)

**Criterios de aceptación**:

- Hilo independiente ejecutándose en background
- No afecta rendimiento de la aplicación principal
- Manejo de errores sin crashes
- Logs detallados de ejecución

### RF-009: Validación de Datos

**Prioridad**: Alta  
**Descripción**: Validar integridad de datos antes de guardar.

**Validaciones**:

- Campos requeridos no vacíos
- Formato de año (4 dígitos, rango válido)
- Formato de ISSN (####-#### o ########)
- Formato de DOI (10.####/...)
- Formato de URL válido (http/https)
- Páginas: inicio < fin
- Email de autores válido
- Si tipo = "Conference paper", nombre_congreso no debe estar vacío
- para_curriculum por defecto = True (Sí)

### RF-010: Dashboard de Estadísticas

**Prioridad**: Baja (post-MVP)  
**Descripción**: Visualizar métricas del sistema.

**Métricas**:

- Total de artículos por año
- Distribución por estado
- Artículos por LGAC
- Top autores más productivos
- Revistas más utilizadas
- Gráficas interactivas

---

## 2. Requisitos No Funcionales

### RNF-001: Rendimiento

- Tiempo de carga de página < 2 segundos
- Extracción de PDF < 10 segundos
- Exportación Excel < 5 segundos (100 artículos)
- Soporte para 500+ artículos sin degradación

### RNF-002: Usabilidad

- Interfaz intuitiva, sin necesidad de manual
- Diseño responsive (escritorio prioritario)
- Mensajes de error claros y descriptivos
- Feedback visual en todas las operaciones

### RNF-003: Confiabilidad

- Manejo de errores sin crashes
- Validación de archivos subidos (tipo, tamaño)
- Backup automático de base de datos (opcional)
- Logs de errores y operaciones críticas

### RNF-004: Mantenibilidad

- Código documentado (docstrings)
- Arquitectura MVC clara
- Separación de responsabilidades
- Configuración centralizada
- Tests unitarios (cobertura >60%)

### RNF-005: Seguridad

- Validación de archivos subidos (tipo MIME, extensión)
- Límite de tamaño de archivo (10 MB)
- Sanitización de inputs
- Protección contra SQL injection (ORM)
- No se requiere autenticación (app privada local)

### RNF-006: Compatibilidad

- Python 3.9+
- Navegadores: Chrome 90+, Firefox 88+, Edge 90+
- Base de datos: SQLite (desarrollo), PostgreSQL (opcional)

### RNF-007: Escalabilidad

- Diseño modular para agregar nuevas funcionalidades
- Base de datos normalizada
- Posibilidad de migrar a app multi-usuario (futuro)

---

## 3. Requisitos Técnicos

### RT-001: Stack Tecnológico

- **Backend**: Flask 3.0+
- **ORM**: SQLAlchemy 2.0+
- **Base de Datos**: SQLite 3
- **Migraciones**: Flask-Migrate (Alembic)
- **PDF Processing**: PyPDF2, pdfplumber
- **Excel**: openpyxl
- **Forms**: Flask-WTF
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript

### RT-002: Arquitectura

- **Patrón**: MVC por módulos
- **Estructura**:
  - `models/`: Definición de tablas (SQLAlchemy)
  - `controllers/`: Lógica de negocio
  - `views/`: Rutas Flask (Blueprints)
  - `services/`: Servicios auxiliares (PDF, Excel, Background)
  - `templates/`: HTML (Jinja2)
  - `static/`: CSS, JS, imágenes

### RT-003: Base de Datos

- SQLite para desarrollo (archivo local)
- Migraciones con Alembic
- Índices en campos de búsqueda frecuente
- Relaciones con claves foráneas

### RT-004: Archivos

- **Uploads**: `uploads/` (PDFs subidos)
- **Exports**: `exports/` (Excel generados)
- Límite: 10 MB por archivo
- Formatos aceptados: .pdf, .xlsx

---

## 4. Restricciones y Supuestos

### Restricciones

- Aplicación local (no servidor remoto en MVP)
- Un solo usuario simultáneo
- Sin sistema de permisos o roles
- Idioma: Español

### Supuestos

- Usuario tiene conocimientos básicos de informática
- PDFs tienen texto extraíble (no escaneos)
- Excel institucional mantiene estructura estable
- Conexión a internet no requerida (app offline)

---

## 5. Priorización para MVP

### Must Have (Imprescindible)

- ✅ RF-001: Registro de artículos
- ✅ RF-002: Extracción automática básica
- ✅ RF-003: Gestión de catálogos
- ✅ RF-004: Consulta y filtrado
- ✅ RF-007: Exportación a Excel
- ✅ RF-008: Hilo en background (básico)
- ✅ RF-009: Validación de datos

### Should Have (Importante)

- ⭐ RF-005: Edición de artículos
- ⭐ RF-006: Eliminación lógica

### Could Have (Deseable)

- 💡 RF-010: Dashboard estadísticas
- 💡 Búsqueda avanzada por múltiples criterios
- 💡 Importación desde Excel

### Won't Have (Fuera del MVP)

- ❌ Sistema de usuarios y permisos
- ❌ API REST
- ❌ Notificaciones por email
- ❌ Integración con bases de datos externas (Scopus API, etc.)

---

## 6. Criterios de Éxito

El MVP será considerado exitoso si:

1. ✅ Registra artículos con <50% de captura manual
2. ✅ Extrae correctamente 70% de metadatos de PDFs estándar
3. ✅ Exporta Excel con formato institucional exacto
4. ✅ Procesa 100 artículos sin errores
5. ✅ Hilo background funciona sin bloquear interfaz
6. ✅ Tiempo de respuesta < 2 segundos en operaciones comunes
7. ✅ Código cumple con arquitectura MVC
