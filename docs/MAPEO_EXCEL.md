# Mapeo de Campos: Excel Institucional → Base de Datos

Este documento detalla cómo se mapean los campos del Excel institucional a la base de datos del sistema.

---

## Estructura del Excel Institucional

### Columnas del Excel (21 campos)

| #   | Nombre Columna                   | Tipo        | Requerido | Notas                           |
| --- | -------------------------------- | ----------- | --------- | ------------------------------- |
| 1   | Tipo de producción               | Catálogo    | ✅ Sí     | FK → tipos_produccion           |
| 2   | Título del artículo              | Texto       | ✅ Sí     | VARCHAR(500)                    |
| 3   | Autor(es) participante(s)        | Texto       | ✅ Sí     | Concatenado, separado por comas |
| 4   | Registro del autor               | Texto       | ❌ No     | Número institucional del autor  |
| 5   | Título de la revista             | Texto       | ✅ Sí     | FK → revistas                   |
| 6   | Editorial                        | Texto       | ❌ No     | Casa editorial                  |
| 7   | ISSN                             | Texto       | ❌ No     | Formato: ####-####              |
| 8   | Volumen                          | Texto       | ❌ No     | Ej: "Vol. 12" o "12"            |
| 9   | Número                           | Texto       | ❌ No     | Ej: "No. 3" o "3"               |
| 10  | Página inicial                   | Número      | ❌ No     | Entero                          |
| 11  | Página final                     | Número      | ❌ No     | Entero                          |
| 12  | Año                              | Número      | ✅ Sí     | Año de publicación (4 dígitos)  |
| 13  | País                             | Catálogo    | ❌ No     | FK → paises                     |
| 14  | LGAC                             | Catálogo    | ✅ Sí     | FK → lgac                       |
| 15  | Indexación                       | Texto       | ❌ No     | Múltiples, separadas por comas  |
| 16  | Estado actual                    | Catálogo    | ✅ Sí     | FK → estados                    |
| 17  | Descripción                      | Texto largo | ❌ No     | Resumen o abstract              |
| 18  | Dirección electrónica            | URL         | ❌ No     | URL del artículo                |
| 19  | Propósito del artículo           | Catálogo    | ❌ No     | FK → propositos                 |
| 20  | Considera para curriculum del CA | Booleano    | ✅ Sí     | Sí/No, default: Sí              |
| 21  | Nombre del congreso              | Texto       | ❌ No     | Solo si es conference paper     |

---

## Mapeo a Base de Datos

### Tabla: `articulos`

| Campo BD        | Columna Excel                    | Transformación   | Notas                           |
| --------------- | -------------------------------- | ---------------- | ------------------------------- |
| id              | -                                | Auto-generado    | Primary Key                     |
| tipo_id         | 1. Tipo de producción            | Lookup en tabla  | FK a tipos_produccion           |
| titulo          | 2. Título del artículo           | Directo          | Limpiar espacios extras         |
| año             | 12. Año                          | Directo          | Validar rango 1900-2100         |
| volumen         | 8. Volumen                       | Directo          | Limpiar prefijos ("Vol.", "V.") |
| numero          | 9. Número                        | Directo          | Limpiar prefijos ("No.", "N.")  |
| pagina_inicio   | 10. Página inicial               | Directo          | Convertir a entero              |
| pagina_fin      | 11. Página final                 | Directo          | Convertir a entero              |
| descripcion     | 17. Descripción                  | Directo          | -                               |
| doi             | -                                | Extraído de PDF  | Agregar si está disponible      |
| url             | 18. Dirección electrónica        | Directo          | Validar formato URL             |
| proposito_id    | 19. Propósito del artículo       | Lookup en tabla  | FK a propositos (opcional)      |
| para_curriculum | 20. Considera para curriculum CA | Directo/Boolean  | Convertir Sí/No a True/False    |
| nombre_congreso | 21. Nombre del congreso          | Directo          | Solo si tipo = Conference paper |
| estado_id       | 16. Estado actual                | Lookup en tabla  | FK a estados                    |
| lgac_id         | 14. LGAC                         | Lookup en tabla  | FK a lgac                       |
| revista_id      | 5. Título de la revista          | Buscar o crear   | FK a revistas                   |
| archivo_pdf     | -                                | Ruta del archivo | Generado internamente           |
| created_at      | -                                | Auto-generado    | Timestamp                       |
| updated_at      | -                                | Auto-generado    | Timestamp                       |
| deleted_at      | -                                | NULL             | Soft delete                     |

---

### Tabla: `revistas`

Información complementaria de la revista:

| Campo BD  | Columna Excel           | Notas           |
| --------- | ----------------------- | --------------- |
| id        | -                       | Auto-generado   |
| nombre    | 5. Título de la revista | -               |
| editorial | 6. Editorial            | -               |
| issn      | 7. ISSN                 | Validar formato |
| pais_id   | 13. País                | FK a paises     |

---

### Tabla: `articulo_autor` (N:N)

Se crea un registro por cada autor:

| Campo BD    | Columna Excel                | Transformación                  |
| ----------- | ---------------------------- | ------------------------------- |
| articulo_id | -                            | ID del artículo                 |
| autor_id    | 3. Autor(es) participante(s) | Split por comas, buscar o crear |
| orden       | -                            | Secuencia (1, 2, 3...)          |

**Proceso**:

1. Separar string por comas: "Juan Pérez, María García, Carlos López"
2. Para cada nombre:
   - Buscar en tabla `autores`
   - Si no existe, crear nuevo registro
   - Crear relación en `articulo_autor` con orden

---

### Tabla: `articulo_indexacion` (N:N)

Se crea un registro por cada indexación:

| Campo BD      | Columna Excel  | Transformación          |
| ------------- | -------------- | ----------------------- |
| articulo_id   | -              | ID del artículo         |
| indexacion_id | 15. Indexación | Split por comas, lookup |

**Proceso**:

1. Separar: "Scopus, Web of Science, Latindex"
2. Para cada indexación:
   - Buscar en tabla `indexaciones`
   - Crear relación en `articulo_indexacion`

---

## Ejemplo de Transformación

### Excel Input

| Tipo                | Título                    | Autores                        | Año  | Revista         | Indexación  |
| ------------------- | ------------------------- | ------------------------------ | ---- | --------------- | ----------- |
| Artículo científico | Deep Learning in Medicine | Dr. Juan Pérez, Dra. Ana López | 2024 | Nature Medicine | Scopus, WoS |

### Base de Datos Output

**Tabla: articulos**

```sql
INSERT INTO articulos (tipo_id, titulo, año, revista_id, estado_id, lgac_id)
VALUES (1, 'Deep Learning in Medicine', 2024, 45, 5, 2);
-- Retorna: id = 100
```

**Tabla: autores** (si no existen)

```sql
INSERT INTO autores (nombre, apellidos) VALUES ('Juan', 'Pérez');  -- id = 20
INSERT INTO autores (nombre, apellidos) VALUES ('Ana', 'López');   -- id = 21
```

**Tabla: articulo_autor**

```sql
INSERT INTO articulo_autor (articulo_id, autor_id, orden) VALUES (100, 20, 1);
INSERT INTO articulo_autor (articulo_id, autor_id, orden) VALUES (100, 21, 2);
```

**Tabla: articulo_indexacion**

```sql
-- Asumiendo: Scopus = id 1, WoS = id 2
INSERT INTO articulo_indexacion (articulo_id, indexacion_id) VALUES (100, 1);
INSERT INTO articulo_indexacion (articulo_id, indexacion_id) VALUES (100, 2);
```

---

## Generación de Excel desde BD

### Query SQL para Exportación

```sql
SELECT
    tp.nombre AS 'Tipo de producción',
    a.titulo AS 'Título del artículo',
    GROUP_CONCAT(au.nombre || ' ' || au.apellidos, ', ') AS 'Autor(es) participante(s)',
    au.registro AS 'Registro del autor',
    r.nombre AS 'Título de la revista',
    r.editorial AS 'Editorial',
    r.issn AS 'ISSN',
    a.volumen AS 'Volumen',
    a.numero AS 'Número',
    a.pagina_inicio AS 'Página inicial',
    a.pagina_fin AS 'Página final',
    a.año AS 'Año',
    p.nombre AS 'País',
    l.nombre AS 'LGAC',
    GROUP_CONCAT(i.acronimo, ', ') AS 'Indexación',
    e.nombre AS 'Estado actual',
    a.descripcion AS 'Descripción',
    a.url AS 'Dirección electrónica',
    pr.nombre AS 'Propósito del artículo',
    CASE WHEN a.para_curriculum THEN 'Sí' ELSE 'No' END AS 'Considera para curriculum del CA',
    a.nombre_congreso AS 'Nombre del congreso'
FROM articulos a
JOIN tipos_produccion tp ON a.tipo_id = tp.id
JOIN estados e ON a.estado_id = e.id
JOIN lgac l ON a.lgac_id = l.id
JOIN revistas r ON a.revista_id = r.id
LEFT JOIN propositos pr ON a.proposito_id = pr.id
LEFT JOIN paises p ON r.pais_id = p.id
LEFT JOIN articulo_autor aa ON a.id = aa.articulo_id
LEFT JOIN autores au ON aa.autor_id = au.id
LEFT JOIN articulo_indexacion ai ON a.id = ai.articulo_id
LEFT JOIN indexaciones i ON ai.indexacion_id = i.id
WHERE a.deleted_at IS NULL
GROUP BY a.id
ORDER BY a.año DESC, a.titulo;
```

---

## Validaciones al Exportar

### 1. Campos Requeridos

Verificar antes de exportar:

```python
required_fields = ['titulo', 'año', 'tipo_id', 'revista_id', 'estado_id', 'lgac_id']

for field in required_fields:
    if article[field] is None:
        warnings.append(f"Artículo {article.id}: {field} está vacío")
```

### 2. Formato de Datos

- **ISSN**: Validar formato ####-#### o convertir ########
- **Año**: Verificar que sea entero de 4 dígitos
- **Páginas**: página_inicio < página_fin

### 3. Manejo de Valores Nulos

En Excel, campos vacíos deben ser:

- Celdas completamente vacías (no "NULL", "N/A", etc.)
- Sin espacios en blanco

---

## Ejemplo de Código: ExcelService

### Estructura básica del servicio

```python
# app/services/excel_service.py

import openpyxl
from openpyxl.styles import Font, Alignment
from app.models import Articulo

class ExcelService:

    COLUMNS = [
        'Tipo de producción',
        'Título del artículo',
        'Autor(es) participante(s)',
        'Registro del autor',
        'Título de la revista',
        'Editorial',
        'ISSN',
        'Volumen',
        'Número',
        'Página inicial',
        'Página final',
        'Año',
        'País',
        'LGAC',
        'Indexación',
        'Estado actual',
        'Descripción',
        'Dirección electrónica',
        'Propósito del artículo',
        'Considera para curriculum del CA',
        'Nombre del congreso'
    ]

    @staticmethod
    def generate(articles, output_path):
        """Genera archivo Excel con artículos"""

        # Crear workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Artículos"

        # Headers
        for col, header in enumerate(ExcelService.COLUMNS, start=1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')

        # Datos
        for row, article in enumerate(articles, start=2):
            ws.cell(row, 1, article.tipo.nombre)
            ws.cell(row, 2, article.titulo)
            ws.cell(row, 3, article.get_authors_string())
            ws.cell(row, 4, article.get_first_author_registro())
            ws.cell(row, 5, article.revista.nombre)
            ws.cell(row, 6, article.revista.editorial)
            ws.cell(row, 7, article.revista.issn)
            ws.cell(row, 8, article.volumen)
            ws.cell(row, 9, article.numero)
            ws.cell(row, 10, article.pagina_inicio)
            ws.cell(row, 11, article.pagina_fin)
            ws.cell(row, 12, article.año)
            ws.cell(row, 13, article.revista.pais.nombre if article.revista.pais else None)
            ws.cell(row, 14, article.lgac.nombre)
            ws.cell(row, 15, article.get_indexaciones_string())
            ws.cell(row, 16, article.estado.nombre)
            ws.cell(row, 17, article.descripcion)
            ws.cell(row, 18, article.url)
            ws.cell(row, 19, article.proposito.nombre if article.proposito else None)
            ws.cell(row, 20, 'Sí' if article.para_curriculum else 'No')
            ws.cell(row, 21, article.nombre_congreso)

        # Ajustar ancho de columnas
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[column].width = min(max_length + 2, 50)

        # Guardar
        wb.save(output_path)
        return output_path
```

---

## Métodos Auxiliares en Modelo

Para facilitar la exportación, agregar métodos en el modelo `Articulo`:

```python
# app/models/articulo.py

class Articulo(db.Model):
    # ... campos ...

    def get_authors_string(self):
        """Retorna autores como string separado por comas"""
        authors = [f"{aa.autor.nombre} {aa.autor.apellidos}"
                   for aa in self.articulo_autores.order_by('orden')]
        return ', '.join(authors)

    def get_first_author_registro(self):
        """Retorna registro del primer autor"""
        first = self.articulo_autores.order_by('orden').first()
        return first.autor.registro if first and first.autor.registro else None

    def get_indexaciones_string(self):
        """Retorna indexaciones como string separado por comas"""
        indexaciones = [ai.indexacion.acronimo or ai.indexacion.nombre
                        for ai in self.articulo_indexaciones]
        return ', '.join(indexaciones)
```

---

## Testing de Exportación

### Test Case: Excel generado correctamente

```python
def test_excel_export():
    # Crear artículo de prueba
    article = create_test_article()

    # Exportar
    output_path = ExcelService.generate([article], '/tmp/test.xlsx')

    # Verificar
    wb = openpyxl.load_workbook(output_path)
    ws = wb.active

    # Verificar headers (fila 1)
    assert ws.cell(1, 1).value == "Tipo de producción"
    assert ws.cell(1, 2).value == "Título del artículo"

    # Verificar datos (fila 2)
    assert ws.cell(2, 2).value == article.titulo
    assert ws.cell(2, 12).value == article.año
```

---

## Notas Importantes

1. **Múltiples autores**: Siempre separar por coma seguida de espacio (", ")
2. **Campos vacíos**: Dejar celda completamente vacía, no poner "N/A"
3. **ISSN**: Mantener formato con guión (1234-5678)
4. **Orden**: Respetar orden exacto de columnas del Excel institucional
5. **Encoding**: Usar UTF-8 para caracteres especiales (acentos, ñ)

---

**Última actualización**: Diciembre 2025
