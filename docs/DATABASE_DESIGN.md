# Diseño de Base de Datos

## Diagrama Entidad-Relación

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   TipoProduccion│         │    Articulo      │         │     Estado      │
├─────────────────┤         ├──────────────────┤         ├─────────────────┤
│ id (PK)         │────────>│ id (PK)          │<────────│ id (PK)         │
│ nombre          │         │ tipo_id (FK)     │         │ nombre          │
│ descripcion     │         │ titulo           │         │ color           │
│ activo          │         │ año              │         │ activo          │
│ created_at      │         │ volumen          │         │ created_at      │
└─────────────────┘         │ numero           │         └─────────────────┘
                            │ pagina_inicio    │
                            │ pagina_fin       │
┌─────────────────┐         │ descripcion      │         ┌─────────────────┐
│      LGAC       │         │ doi              │         │    Revista      │
├─────────────────┤         │ estado_id (FK)   │         ├─────────────────┤
│ id (PK)         │────────>│ lgac_id (FK)     │<────────│ id (PK)         │
│ nombre          │         │ revista_id (FK)  │         │ nombre          │
│ descripcion     │         │ archivo_pdf      │         │ editorial       │
│ activo          │         │ created_at       │         │ issn            │
│ created_at      │         │ updated_at       │         │ pais_id (FK)    │
└─────────────────┘         │ deleted_at       │         │ url             │
                            └──────────────────┘         │ activo          │
                                    ▲                    │ created_at      │
                                    │                    └─────────────────┘
                            ┌───────┴────────┐                    │
                            │                │                    │
                    ┌───────────────┐  ┌──────────────────┐      │
                    │ArticuloAutor  │  │ArticuloIndexacion│      │
                    ├───────────────┤  ├──────────────────┤      │
                    │ id (PK)       │  │ id (PK)          │      │
                    │ articulo_id   │  │ articulo_id (FK) │      │
                    │ autor_id (FK) │  │ indexacion_id    │      │
                    │ orden         │  │ fecha_indexacion │      ▼
                    │ created_at    │  │ created_at       │ ┌─────────────┐
                    └───────────────┘  └──────────────────┘ │    Pais     │
                            │                    │           ├─────────────┤
                            ▼                    ▼           │ id (PK)     │
                    ┌───────────────┐  ┌──────────────────┐ │ nombre      │
                    │     Autor     │  │   Indexacion     │ │ codigo_iso  │
                    ├───────────────┤  ├──────────────────┤ │ activo      │
                    │ id (PK)       │  │ id (PK)          │ │ created_at  │
                    │ nombre        │  │ nombre           │ └─────────────┘
                    │ apellidos     │  │ acronimo         │
                    │ email         │  │ url              │
                    │ registro      │  │ prestigio        │
                    │ activo        │  │ activo           │
                    │ created_at    │  │ created_at       │
                    └───────────────┘  └──────────────────┘

                    ┌──────────────────┐
                    │RevistaIndexacion │
                    ├──────────────────┤
                    │ id (PK)          │
                    │ revista_id (FK)  │
                    │ indexacion_id    │
                    │ created_at       │
                    └──────────────────┘
```

---

## Especificación de Tablas

### 1. Tabla: `articulos`

**Descripción**: Almacena información principal de cada artículo académico.

| Campo           | Tipo        | Restricciones                      | Descripción                        |
| --------------- | ----------- | ---------------------------------- | ---------------------------------- |
| id              | Integer     | PK, AutoIncrement                  | Identificador único                |
| tipo_id         | Integer     | FK → tipos_produccion.id, NOT NULL | Tipo de producción                 |
| titulo          | String(500) | NOT NULL, Unique                   | Título del artículo                |
| año             | Integer     | NOT NULL, CHECK (año >= 1900)      | Año de publicación                 |
| volumen         | String(50)  | Nullable                           | Volumen de la revista              |
| numero          | String(50)  | Nullable                           | Número de la revista               |
| pagina_inicio   | Integer     | Nullable                           | Página inicial                     |
| pagina_fin      | Integer     | Nullable                           | Página final                       |
| descripcion     | Text        | Nullable                           | Resumen o descripción              |
| doi             | String(100) | Nullable, Unique                   | Digital Object Identifier          |
| url             | String(500) | Nullable                           | Dirección electrónica del artículo |
| proposito_id    | Integer     | FK → propositos.id, Nullable       | Propósito del artículo             |
| para_curriculum | Boolean     | NOT NULL, Default=True             | Considera para curriculum del CA   |
| nombre_congreso | String(300) | Nullable                           | Nombre del congreso (si aplica)    |
| estado_id       | Integer     | FK → estados.id, NOT NULL          | Estado actual                      |
| lgac_id         | Integer     | FK → lgac.id, NOT NULL             | LGAC asociada                      |
| revista_id      | Integer     | FK → revistas.id, NOT NULL         | Revista donde se publicó           |
| archivo_pdf     | String(255) | Nullable                           | Ruta del PDF subido                |
| created_at      | DateTime    | NOT NULL, Default=now()            | Fecha de creación                  |
| updated_at      | DateTime    | Nullable, OnUpdate=now()           | Última actualización               |
| deleted_at      | DateTime    | Nullable                           | Fecha de eliminación lógica        |

**Índices**:

- `idx_articulos_titulo` en `titulo`
- `idx_articulos_año` en `año`
- `idx_articulos_estado` en `estado_id`
- `idx_articulos_lgac` en `lgac_id`
- `idx_articulos_para_curriculum` en `para_curriculum`

---

### 2. Tabla: `autores`

**Descripción**: Catálogo de autores/investigadores del Cuerpo Académico.

| Campo      | Tipo        | Restricciones           | Descripción                      |
| ---------- | ----------- | ----------------------- | -------------------------------- |
| id         | Integer     | PK, AutoIncrement       | Identificador único              |
| nombre     | String(100) | NOT NULL                | Nombre(s)                        |
| apellidos  | String(100) | NOT NULL                | Apellidos                        |
| email      | String(150) | Nullable, Unique        | Correo electrónico               |
| registro   | String(50)  | Nullable                | Número de registro institucional |
| activo     | Boolean     | NOT NULL, Default=True  | Si está activo                   |
| created_at | DateTime    | NOT NULL, Default=now() | Fecha de creación                |

**Restricciones únicas**: `(nombre, apellidos)` - Evitar duplicados

---

### 3. Tabla: `articulo_autor`

**Descripción**: Relación N:N entre artículos y autores con orden.

| Campo       | Tipo     | Restricciones               | Descripción                    |
| ----------- | -------- | --------------------------- | ------------------------------ |
| id          | Integer  | PK, AutoIncrement           | Identificador único            |
| articulo_id | Integer  | FK → articulos.id, NOT NULL | Artículo                       |
| autor_id    | Integer  | FK → autores.id, NOT NULL   | Autor                          |
| orden       | Integer  | NOT NULL, Default=1         | Orden del autor en el artículo |
| created_at  | DateTime | NOT NULL, Default=now()     | Fecha de creación              |

**Restricciones únicas**: `(articulo_id, autor_id)` - Un autor no se repite en el mismo artículo

---

### 4. Tabla: `revistas`

**Descripción**: Catálogo de revistas científicas.

| Campo      | Tipo        | Restricciones            | Descripción          |
| ---------- | ----------- | ------------------------ | -------------------- |
| id         | Integer     | PK, AutoIncrement        | Identificador único  |
| nombre     | String(300) | NOT NULL, Unique         | Nombre de la revista |
| editorial  | String(200) | Nullable                 | Casa editorial       |
| issn       | String(20)  | Nullable                 | ISSN (####-####)     |
| pais_id    | Integer     | FK → paises.id, Nullable | País de publicación  |
| url        | String(255) | Nullable                 | Sitio web            |
| activo     | Boolean     | NOT NULL, Default=True   | Si está activa       |
| created_at | DateTime    | NOT NULL, Default=now()  | Fecha de creación    |

---

### 5. Tabla: `tipos_produccion`

**Descripción**: Catálogo de tipos de producción académica.

| Campo       | Tipo        | Restricciones           | Descripción           |
| ----------- | ----------- | ----------------------- | --------------------- |
| id          | Integer     | PK, AutoIncrement       | Identificador único   |
| nombre      | String(100) | NOT NULL, Unique        | Nombre del tipo       |
| descripcion | Text        | Nullable                | Descripción detallada |
| activo      | Boolean     | NOT NULL, Default=True  | Si está activo        |
| created_at  | DateTime    | NOT NULL, Default=now() | Fecha de creación     |

**Valores iniciales**:

- Artículo científico
- Artículo de divulgación
- Review (revisión sistemática)
- Case study
- Technical report
- Conference paper

---

### 6. Tabla: `estados`

**Descripción**: Catálogo de estados del artículo.

| Campo      | Tipo       | Restricciones           | Descripción            |
| ---------- | ---------- | ----------------------- | ---------------------- |
| id         | Integer    | PK, AutoIncrement       | Identificador único    |
| nombre     | String(50) | NOT NULL, Unique        | Nombre del estado      |
| color      | String(20) | Nullable                | Color para badge (hex) |
| activo     | Boolean    | NOT NULL, Default=True  | Si está activo         |
| created_at | DateTime   | NOT NULL, Default=now() | Fecha de creación      |

**Valores iniciales**:

- En preparación (#6c757d - gris)
- Enviado (#0dcaf0 - cyan)
- En revisión (#ffc107 - amarillo)
- Aceptado (#198754 - verde)
- Publicado (#0d6efd - azul)
- Rechazado (#dc3545 - rojo)

---

### 7. Tabla: `propositos`

**Descripción**: Catálogo de propósitos del artículo.

| Campo       | Tipo        | Restricciones           | Descripción           |
| ----------- | ----------- | ----------------------- | --------------------- |
| id          | Integer     | PK, AutoIncrement       | Identificador único   |
| nombre      | String(100) | NOT NULL, Unique        | Nombre del propósito  |
| descripcion | Text        | Nullable                | Descripción detallada |
| activo      | Boolean     | NOT NULL, Default=True  | Si está activo        |
| created_at  | DateTime    | NOT NULL, Default=now() | Fecha de creación     |

**Valores iniciales**:

- Investigación básica
- Investigación aplicada
- Desarrollo tecnológico
- Divulgación científica
- Revisión bibliográfica
- Desarrollo de metodología
- Transferencia de conocimiento

---

### 8. Tabla: `lgac`

**Descripción**: Líneas de Generación y Aplicación del Conocimiento.

| Campo       | Tipo        | Restricciones           | Descripción           |
| ----------- | ----------- | ----------------------- | --------------------- |
| id          | Integer     | PK, AutoIncrement       | Identificador único   |
| nombre      | String(200) | NOT NULL, Unique        | Nombre de la LGAC     |
| descripcion | Text        | Nullable                | Descripción detallada |
| activo      | Boolean     | NOT NULL, Default=True  | Si está activa        |
| created_at  | DateTime    | NOT NULL, Default=now() | Fecha de creación     |

---

### 9. Tabla: `indexaciones`

**Descripción**: Catálogo de bases de datos de indexación.

| Campo      | Tipo        | Restricciones           | Descripción              |
| ---------- | ----------- | ----------------------- | ------------------------ |
| id         | Integer     | PK, AutoIncrement       | Identificador único      |
| nombre     | String(100) | NOT NULL, Unique        | Nombre completo          |
| acronimo   | String(20)  | Nullable                | Acrónimo (WoS, JCR)      |
| url        | String(255) | Nullable                | Sitio web                |
| prestigio  | Integer     | Nullable, CHECK (1-5)   | Nivel de prestigio (1-5) |
| activo     | Boolean     | NOT NULL, Default=True  | Si está activa           |
| created_at | DateTime    | NOT NULL, Default=now() | Fecha de creación        |

**Valores iniciales**:

- Scopus (prestigio=5)
- Web of Science (prestigio=5)
- JCR - Journal Citation Reports (prestigio=5)
- SciELO (prestigio=3)
- Latindex (prestigio=2)
- DOAJ (prestigio=3)
- PubMed (prestigio=4)

---

### 10. Tabla: `articulo_indexacion`

**Descripción**: Relación N:N entre artículos e indexaciones.

| Campo            | Tipo     | Restricciones                  | Descripción            |
| ---------------- | -------- | ------------------------------ | ---------------------- |
| id               | Integer  | PK, AutoIncrement              | Identificador único    |
| articulo_id      | Integer  | FK → articulos.id, NOT NULL    | Artículo               |
| indexacion_id    | Integer  | FK → indexaciones.id, NOT NULL | Indexación             |
| fecha_indexacion | Date     | Nullable                       | Fecha en que se indexó |
| created_at       | DateTime | NOT NULL, Default=now()        | Fecha de creación      |

**Restricciones únicas**: `(articulo_id, indexacion_id)`

---

### 11. Tabla: `revista_indexacion`

**Descripción**: Relación N:N entre revistas e indexaciones.

| Campo         | Tipo     | Restricciones                  | Descripción         |
| ------------- | -------- | ------------------------------ | ------------------- |
| id            | Integer  | PK, AutoIncrement              | Identificador único |
| revista_id    | Integer  | FK → revistas.id, NOT NULL     | Revista             |
| indexacion_id | Integer  | FK → indexaciones.id, NOT NULL | Indexación          |
| created_at    | DateTime | NOT NULL, Default=now()        | Fecha de creación   |

**Restricciones únicas**: `(revista_id, indexacion_id)`

---

### 12. Tabla: `paises`

**Descripción**: Catálogo de países.

| Campo      | Tipo        | Restricciones           | Descripción               |
| ---------- | ----------- | ----------------------- | ------------------------- |
| id         | Integer     | PK, AutoIncrement       | Identificador único       |
| nombre     | String(100) | NOT NULL, Unique        | Nombre del país           |
| codigo_iso | String(3)   | Nullable, Unique        | Código ISO 3166-1 alpha-3 |
| activo     | Boolean     | NOT NULL, Default=True  | Si está activo            |
| created_at | DateTime    | NOT NULL, Default=now() | Fecha de creación         |

**Valores comunes**:

- México (MEX)
- Estados Unidos (USA)
- España (ESP)
- Reino Unido (GBR)
- Alemania (DEU)

---

## Relaciones y Cardinalidad

| Relación                  | Tipo | Descripción                                    |
| ------------------------- | ---- | ---------------------------------------------- |
| Articulo → TipoProduccion | N:1  | Cada artículo tiene un tipo                    |
| Articulo → Proposito      | N:1  | Cada artículo tiene un propósito (opcional)    |
| Articulo → Estado         | N:1  | Cada artículo tiene un estado                  |
| Articulo → LGAC           | N:1  | Cada artículo pertenece a una LGAC             |
| Articulo → Revista        | N:1  | Cada artículo se publicó en una revista        |
| Articulo ↔ Autor          | N:N  | Un artículo tiene varios autores y viceversa   |
| Articulo ↔ Indexacion     | N:N  | Un artículo puede estar en varias indexaciones |
| Revista → Pais            | N:1  | Cada revista es de un país                     |
| Revista ↔ Indexacion      | N:N  | Una revista puede estar en varias indexaciones |

---

## Queries Comunes

### 1. Listar artículos con autores

```sql
SELECT
    a.id, a.titulo, a.año,
    GROUP_CONCAT(au.nombre || ' ' || au.apellidos) as autores
FROM articulos a
JOIN articulo_autor aa ON a.id = aa.articulo_id
JOIN autores au ON aa.autor_id = au.id
WHERE a.deleted_at IS NULL
GROUP BY a.id
ORDER BY a.año DESC;
```

### 2. Artículos por LGAC

```sql
SELECT l.nombre, COUNT(a.id) as total
FROM lgac l
LEFT JOIN articulos a ON l.id = a.lgac_id AND a.deleted_at IS NULL
GROUP BY l.id
ORDER BY total DESC;
```

### 3. Autores más productivos

```sql
SELECT
    au.nombre || ' ' || au.apellidos as autor,
    COUNT(DISTINCT aa.articulo_id) as articulos
FROM autores au
JOIN articulo_autor aa ON au.id = aa.autor_id
JOIN articulos a ON aa.articulo_id = a.id
WHERE a.deleted_at IS NULL
GROUP BY au.id
ORDER BY articulos DESC
LIMIT 10;
```

### 4. Revistas con más publicaciones

```sql
SELECT r.nombre, COUNT(a.id) as total
FROM revistas r
LEFT JOIN articulos a ON r.id = a.revista_id AND a.deleted_at IS NULL
GROUP BY r.id
ORDER BY total DESC
LIMIT 10;
```

---

## Estrategia de Migración

### Versión 1.0 (MVP)

- Crear todas las tablas base
- Insertar datos de catálogos (seed data)
- Índices básicos

### Versión 1.1 (Futuro)

- Agregar tablas de auditoría
- Historial de cambios
- Sistema de notificaciones

### Scripts de Seed Data

Se crearán scripts para poblar:

- Estados iniciales (6 registros)
- Tipos de producción (6 registros)
- Indexaciones (7 registros)
- Países comunes (20 registros)
- LGACs (según el CA específico)

---

## Normalización

El diseño cumple con **3NF (Tercera Forma Normal)**:

- ✅ 1NF: Valores atómicos
- ✅ 2NF: Sin dependencias parciales
- ✅ 3NF: Sin dependencias transitivas

**Ventajas**:

- Minimiza redundancia
- Facilita actualizaciones
- Mantiene integridad referencial
- Escalable
