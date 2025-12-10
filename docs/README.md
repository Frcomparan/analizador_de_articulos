# 📄 Índice de Documentación del Proyecto

## Guía de Navegación

Esta carpeta contiene toda la documentación técnica y funcional del Sistema de Gestión de Artículos Académicos.

---

## 🚀 Para Empezar

**Nuevo en el proyecto? Empieza aquí:**

1. **[RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)** ⭐

   - Visión general del proyecto
   - Objetivos y beneficios
   - Estado actual
   - **Tiempo de lectura**: 10 minutos

2. **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** ⭐
   - Guía de instalación paso a paso
   - Comandos útiles
   - Troubleshooting
   - **Tiempo de lectura**: 15 minutos

---

## 📋 Documentación Funcional

### [REQUISITOS.md](REQUISITOS.md)

**¿Qué hace el sistema?**

- ✅ Requisitos funcionales (RF-001 a RF-010)
- ✅ Requisitos no funcionales (rendimiento, seguridad)
- ✅ Casos de uso
- ✅ Priorización para MVP
- ✅ Criterios de éxito

**Útil para**:

- Entender funcionalidades completas
- Validar implementación
- Definir tests

---

## 🏗️ Documentación Técnica

### [ARQUITECTURA.md](ARQUITECTURA.md)

**¿Cómo está estructurado el código?**

- Patrón MVC detallado
- Estructura de directorios
- Capas del sistema (Models, Views, Controllers, Services)
- Flujo de requests
- Convenciones de código
- Ejemplo completo de cada capa

**Útil para**:

- Implementar nuevas funcionalidades
- Mantener consistencia en el código
- Onboarding de nuevos desarrolladores

### [DATABASE_DESIGN.md](DATABASE_DESIGN.md)

**¿Cómo se organiza la información?**

- Diagrama Entidad-Relación
- Especificación de 11 tablas
- Relaciones y cardinalidad
- Queries SQL comunes
- Estrategia de migración
- Normalización (3NF)

**Útil para**:

- Crear modelos SQLAlchemy
- Escribir queries eficientes
- Diseñar nuevas funcionalidades

### [MAPEO_EXCEL.md](MAPEO_EXCEL.md)

**¿Cómo se relaciona el Excel con la base de datos?**

- Mapeo columna por columna (17 campos)
- Transformaciones necesarias
- Ejemplo de código para exportación
- Métodos auxiliares en modelos
- Validaciones al exportar

**Útil para**:

- Implementar ExcelService
- Entender formato institucional
- Validar exportaciones

---

## 📅 Planificación

### [MVP_ROADMAP.md](MVP_ROADMAP.md)

**¿Cuándo y cómo se implementará?**

- 8 fases de desarrollo (7 semanas)
- Tareas detalladas por fase
- Entregables específicos
- Cronograma visual
- Riesgos y mitigaciones
- Métricas de seguimiento

**Útil para**:

- Planificar sprints
- Seguimiento de progreso
- Estimación de tiempos

---

## 📊 Documentos por Audiencia

### Para Desarrolladores

1. [INICIO_RAPIDO.md](INICIO_RAPIDO.md) - Setup inicial
2. [ARQUITECTURA.md](ARQUITECTURA.md) - Estructura del código
3. [DATABASE_DESIGN.md](DATABASE_DESIGN.md) - Modelos y queries
4. [MVP_ROADMAP.md](MVP_ROADMAP.md) - Plan de trabajo

### Para Gestores de Proyecto

1. [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md) - Overview completo
2. [REQUISITOS.md](REQUISITOS.md) - Funcionalidades y alcance
3. [MVP_ROADMAP.md](MVP_ROADMAP.md) - Cronograma y riesgos

### Para Usuarios Finales

1. [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md) - ¿Qué hace el sistema?
2. [REQUISITOS.md](REQUISITOS.md) - Funcionalidades disponibles

---

## 🔍 Búsqueda Rápida

### ¿Necesitas información sobre...?

**Instalación y Setup**
→ [INICIO_RAPIDO.md](INICIO_RAPIDO.md)

**Campos del Excel institucional**
→ [MAPEO_EXCEL.md](MAPEO_EXCEL.md)

**Tablas de la base de datos**
→ [DATABASE_DESIGN.md](DATABASE_DESIGN.md)

**Patrón MVC**
→ [ARQUITECTURA.md](ARQUITECTURA.md)

**Extracción de PDFs**
→ [REQUISITOS.md](REQUISITOS.md) (RF-002) + [ARQUITECTURA.md](ARQUITECTURA.md) (PDFService)

**Hilo en background**
→ [REQUISITOS.md](REQUISITOS.md) (RF-008) + [ARQUITECTURA.md](ARQUITECTURA.md) (BackgroundWorker)

**Cronograma de desarrollo**
→ [MVP_ROADMAP.md](MVP_ROADMAP.md)

**Tecnologías utilizadas**
→ [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)

---

## 📝 Orden de Lectura Recomendado

### Primera vez en el proyecto

```
1. RESUMEN_EJECUTIVO.md    (Visión general)
2. INICIO_RAPIDO.md         (Setup)
3. ARQUITECTURA.md          (Estructura)
4. DATABASE_DESIGN.md       (Modelos)
5. MVP_ROADMAP.md           (Plan de trabajo)
```

### Antes de implementar funcionalidad

```
1. REQUISITOS.md            (¿Qué necesito implementar?)
2. ARQUITECTURA.md          (¿Dónde va el código?)
3. DATABASE_DESIGN.md       (¿Qué tablas necesito?)
4. MAPEO_EXCEL.md           (Si involucra Excel)
```

### Antes de exportar a Excel

```
1. MAPEO_EXCEL.md           (Mapeo completo)
2. DATABASE_DESIGN.md       (Queries necesarias)
3. ARQUITECTURA.md          (ExcelService)
```

---

## 🎯 Documentación por Fase del MVP

| Fase                       | Documentos Relevantes                                      |
| -------------------------- | ---------------------------------------------------------- |
| **Fase 1**: Setup Base     | INICIO_RAPIDO.md, ARQUITECTURA.md                          |
| **Fase 2**: CRUD Artículos | DATABASE_DESIGN.md, ARQUITECTURA.md, REQUISITOS.md         |
| **Fase 3**: PDFs           | ARQUITECTURA.md (PDFService), REQUISITOS.md (RF-002)       |
| **Fase 4**: Filtrado       | REQUISITOS.md (RF-004), DATABASE_DESIGN.md                 |
| **Fase 5**: Excel          | MAPEO_EXCEL.md, DATABASE_DESIGN.md                         |
| **Fase 6**: Background     | ARQUITECTURA.md (BackgroundWorker), REQUISITOS.md (RF-008) |
| **Fase 7**: Catálogos      | DATABASE_DESIGN.md, REQUISITOS.md (RF-003)                 |
| **Fase 8**: Testing        | Todos los documentos                                       |

---

## 📦 Otros Archivos en el Proyecto

### Raíz del Proyecto

- **[../README.md](../README.md)** - Documentación principal (versión pública)
- **[../requirements.txt](../requirements.txt)** - Dependencias del proyecto
- **[../config.py](../config.py)** - Configuración de Flask
- **[../run.py](../run.py)** - Punto de entrada de la aplicación
- **[../.env.example](../.env.example)** - Variables de entorno de ejemplo
- **[../.gitignore](../.gitignore)** - Archivos ignorados por Git

---

## 🔄 Mantenimiento de la Documentación

### Cuándo actualizar

- ✏️ **Nuevas funcionalidades**: Actualizar REQUISITOS.md
- 🗄️ **Cambios en BD**: Actualizar DATABASE_DESIGN.md
- 🏗️ **Nueva arquitectura**: Actualizar ARQUITECTURA.md
- 📅 **Cambios en plan**: Actualizar MVP_ROADMAP.md
- 📊 **Cambio en Excel**: Actualizar MAPEO_EXCEL.md

### Versiones

Cada documento tiene fecha de última actualización al final.

---

## 💡 Consejos para Usar la Documentación

1. **No leas todo de una vez**: Usa el índice para encontrar lo que necesitas
2. **Busca ejemplos**: Todos los docs técnicos incluyen código de ejemplo
3. **Valida con el código**: La documentación y el código deben coincidir
4. **Actualiza si encuentras errores**: La documentación es un documento vivo
5. **Usa diagramas**: Son más fáciles de entender que texto largo

---

## 📞 ¿Falta algo?

Si necesitas documentación adicional sobre:

- Guía de usuario final
- Manual de deployment
- Guía de contribución
- API documentation

Agrégala siguiendo el formato de los documentos existentes.

---

## 📈 Estadísticas de Documentación

| Documento            | Páginas | Líneas    | Tiempo Lectura |
| -------------------- | ------- | --------- | -------------- |
| RESUMEN_EJECUTIVO.md | 6       | ~350      | 10 min         |
| REQUISITOS.md        | 8       | ~550      | 20 min         |
| DATABASE_DESIGN.md   | 9       | ~600      | 25 min         |
| ARQUITECTURA.md      | 10      | ~700      | 30 min         |
| MVP_ROADMAP.md       | 11      | ~800      | 25 min         |
| MAPEO_EXCEL.md       | 7       | ~500      | 20 min         |
| INICIO_RAPIDO.md     | 5       | ~350      | 15 min         |
| **TOTAL**            | **56**  | **~3850** | **~2.5 horas** |

---

**Última actualización**: Diciembre 2025  
**Versión**: 1.0.0
