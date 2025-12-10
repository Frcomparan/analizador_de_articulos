# 📋 Resumen Ejecutivo del Proyecto

## Sistema de Gestión de Artículos Académicos

---

## ¿Qué es este proyecto?

Una aplicación web local desarrollada en **Python con Flask** que permite al Cuerpo Académico registrar, consultar y gestionar artículos científicos de forma **semi-automatizada**, reduciendo la captura manual mediante extracción de información desde archivos PDF.

---

## Problema que Resuelve

### Situación Actual

- ❌ Captura manual de todos los datos de artículos en Excel
- ❌ Errores de transcripción y duplicados
- ❌ Tiempo invertido en tareas repetitivas
- ❌ Dificultad para filtrar y buscar información
- ❌ Generación manual de reportes

### Solución Propuesta

- ✅ **Extracción automática** de metadatos desde PDFs (70% de campos)
- ✅ **Validación automática** de datos (ISSN, DOI, años)
- ✅ **Filtrado inteligente** por múltiples criterios
- ✅ **Exportación automática** a Excel institucional
- ✅ **Procesamiento en background** sin bloquear la interfaz

---

## Características Principales

### 🎯 Funcionalidades Core

1. **Registro Semi-Automático**

   - Usuario sube PDF del artículo o carta de aceptación
   - Sistema extrae: título, autores, año, revista, DOI, ISSN
   - Usuario completa campos faltantes
   - Validación automática antes de guardar

2. **Gestión Completa (CRUD)**

   - Crear, ver, editar y eliminar artículos
   - Paginación de resultados
   - Eliminación lógica (recuperable)

3. **Búsqueda y Filtrado Avanzado**

   - Por año (rango)
   - Por estado (En revisión, Publicado, etc.)
   - Por LGAC
   - Por autor
   - Por tipo de producción
   - Búsqueda por texto libre (título, revista)

4. **Exportación a Excel**

   - Formato institucional exacto
   - Incluye todos los campos requeridos
   - Descarga automática
   - Opción de exportar todo o solo filtrados

5. **Procesamiento en Background**

   - Detección automática de artículos incompletos
   - Limpieza de archivos antiguos
   - No bloquea la interfaz principal

6. **Gestión de Catálogos**
   - Tipos de producción
   - Propósitos del artículo
   - Estados
   - LGACs
   - Indexaciones (Scopus, WoS, etc.)
   - Autores
   - Revistas
   - Países

---

## Tecnologías Utilizadas

### Backend

- **Flask 3.0** - Framework web
- **SQLAlchemy 2.0** - ORM para base de datos
- **SQLite** - Base de datos (desarrollo)
- **PyPDF2 / pdfplumber** - Extracción de PDFs

### Frontend

- **HTML5 + CSS3**
- **Bootstrap 5** - Framework UI
- **JavaScript** - Interactividad

### Herramientas

- **Flask-Migrate** - Migraciones de BD
- **openpyxl** - Generación de Excel
- **pytest** - Testing

---

## Arquitectura del Sistema

### Patrón: MVC (Model-View-Controller)

```
┌─────────────┐
│   USUARIO   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   VIEWS (V)     │  ← Rutas y templates HTML
│   Blueprints    │
└────────┬────────┘
         │
         ▼
┌──────────────────┐
│ CONTROLLERS (C)  │  ← Lógica de negocio
│  + SERVICES      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   MODELS (M)     │  ← ORM (SQLAlchemy)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   DATABASE       │  ← SQLite
└──────────────────┘
```

**Ventajas**:

- Código organizado y mantenible
- Separación de responsabilidades
- Fácil de testear
- Escalable

---

## Base de Datos

### Modelo Relacional Normalizado (3NF)

**Tablas principales**:

- `articulos` - Información de artículos (incluye URL, propósito, para_curriculum, nombre_congreso)
- `autores` - Catálogo de autores
- `revistas` - Catálogo de revistas
- `tipos_produccion` - Tipos de artículos
- `propositos` - Propósitos del artículo
- `estados` - Estados del artículo
- `lgac` - Líneas de investigación
- `indexaciones` - Bases de datos de indexación
- `paises` - Países

**Relaciones**:

- Artículo ↔ Autores (N:N)
- Artículo ↔ Indexaciones (N:N)
- Artículo → Revista (N:1)
- Revista ↔ Indexaciones (N:N)

Ver detalles completos en: `docs/DATABASE_DESIGN.md`

---

## Flujo de Trabajo

### Caso de Uso: Registrar Artículo

```
1. Usuario navega a "Nuevo Artículo"
   ↓
2. Sube PDF del artículo
   ↓
3. Sistema extrae metadatos automáticamente
   ↓
4. Formulario se pre-llena con datos extraídos
   ↓
5. Usuario revisa y completa campos faltantes
   ↓
6. Sistema valida datos
   ↓
7. Artículo se guarda en BD
   ↓
8. Confirmación y redirección a detalle
```

---

## Cronograma de Desarrollo

### MVP: 6-7 Semanas

| Fase                           | Duración  | Entregables                           |
| ------------------------------ | --------- | ------------------------------------- |
| **Fase 1**: Configuración Base | 1 semana  | Proyecto configurado, BD inicializada |
| **Fase 2**: CRUD Artículos     | 2 semanas | Gestión completa de artículos         |
| **Fase 3**: Extracción PDFs    | 2 semanas | Upload y extracción automática        |
| **Fase 4**: Filtrado           | 1 semana  | Sistema de búsqueda y filtros         |
| **Fase 5**: Exportación Excel  | 1 semana  | Generación de reportes                |
| **Fase 6**: Background Worker  | 1 semana  | Tareas automáticas                    |
| **Fase 7**: Catálogos          | 1 semana  | Gestión de maestros                   |
| **Fase 8**: Testing            | 1 semana  | Refinamiento y correcciones           |

Ver cronograma detallado en: `docs/MVP_ROADMAP.md`

---

## Métricas de Éxito

El MVP será considerado exitoso si cumple:

| Métrica                     | Objetivo           |
| --------------------------- | ------------------ |
| Reducción de captura manual | < 50%              |
| Precisión de extracción     | > 70%              |
| Tiempo de respuesta         | < 2 segundos       |
| Soporte de artículos        | 100+ sin problemas |
| Cobertura de tests          | > 60%              |
| Formato Excel               | 100% exacto        |

---

## Beneficios Esperados

### Cuantitativos

- ⏱️ **Ahorro de tiempo**: ~60% en captura de datos
- 📊 **Reducción de errores**: ~80% menos errores de transcripción
- 🔍 **Búsquedas**: De minutos a segundos

### Cualitativos

- ✨ **Mejor experiencia**: Interfaz intuitiva vs. Excel
- 🎯 **Mayor precisión**: Validaciones automáticas
- 📈 **Escalabilidad**: Fácil agregar funcionalidades
- 🔄 **Automatización**: Tareas repetitivas en background

---

## Requisitos Técnicos

### Para Desarrollo

- Python 3.9 o superior
- Editor de código (VS Code recomendado)
- Navegador web moderno

### Para Producción (Futuro)

- Servidor Linux/Windows
- PostgreSQL (opcional)
- 2 GB RAM mínimo

---

## Riesgos y Mitigaciones

| Riesgo                      | Impacto | Mitigación                         |
| --------------------------- | ------- | ---------------------------------- |
| Extracción de PDF imprecisa | Alto    | Permitir edición manual siempre    |
| Cambios en formato Excel    | Medio   | Configuración flexible de columnas |
| Background worker inestable | Medio   | Manejo robusto de errores          |

---

## Alcance del MVP

### ✅ Incluido

- CRUD de artículos
- Extracción básica de PDFs
- Filtrado y búsqueda
- Exportación a Excel
- Hilo en background
- Gestión de catálogos

### ❌ No Incluido (Post-MVP)

- Sistema de usuarios y permisos
- API REST
- Integración con bases externas (Scopus API)
- Dashboard con gráficas avanzadas
- Notificaciones por email

---

## Documentación Disponible

| Documento                 | Descripción                             |
| ------------------------- | --------------------------------------- |
| `README.md`               | Visión general del proyecto             |
| `docs/REQUISITOS.md`      | Requisitos funcionales y no funcionales |
| `docs/DATABASE_DESIGN.md` | Diseño de base de datos                 |
| `docs/ARQUITECTURA.md`    | Arquitectura MVC detallada              |
| `docs/MVP_ROADMAP.md`     | Plan de implementación por fases        |
| `docs/INICIO_RAPIDO.md`   | Guía de instalación paso a paso         |
| `docs/MAPEO_EXCEL.md`     | Mapeo Excel ↔ Base de datos             |

---

## Estado Actual del Proyecto

### ✅ Completado

- [x] Documentación completa
- [x] Diseño de base de datos
- [x] Arquitectura definida
- [x] Estructura de directorios creada
- [x] Archivos de configuración
- [x] Dependencias listadas

### ⏳ Pendiente

- [ ] Implementación de modelos
- [ ] Implementación de views
- [ ] Implementación de controllers
- [ ] Implementación de services
- [ ] Templates HTML
- [ ] Testing

---

## Próximos Pasos Inmediatos

1. **Instalar dependencias**

   ```powershell
   pip install -r requirements.txt
   ```

2. **Crear modelos de base de datos**

   - Comenzar con `articulo.py`
   - Seguir con catálogos

3. **Inicializar migraciones**

   ```powershell
   flask db init
   flask db migrate -m "Initial migration"
   ```

4. **Implementar primer CRUD**
   - Comenzar con Artículos
   - Probar ciclo completo

Ver guía completa en: `docs/INICIO_RAPIDO.md`

---

## Contacto y Recursos

### Documentación Técnica

- Flask: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Bootstrap: https://getbootstrap.com/

### Soporte

- Revisar documentación en carpeta `docs/`
- Consultar código de ejemplo en documentos
- Seguir roadmap en `MVP_ROADMAP.md`

---

## Conclusión

Este proyecto representa una **solución moderna y eficiente** para la gestión de artículos académicos, con énfasis en:

- 🎯 **Automatización** - Reducir trabajo manual
- 🏗️ **Arquitectura sólida** - Código mantenible y escalable
- 🧪 **Calidad** - Testing y validaciones
- 📚 **Documentación** - Guías completas para desarrollo

Con un plan detallado de 7 semanas, se espera entregar un **MVP funcional** que cumpla con todos los requisitos establecidos.

---

**Proyecto**: Sistema de Gestión de Artículos Académicos  
**Versión**: 1.0.0 (MVP)  
**Fecha**: Diciembre 2025  
**Estado**: 🟢 En Planificación → 🔵 Listo para Desarrollo
