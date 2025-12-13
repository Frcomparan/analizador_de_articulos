# Formularios - Documentación

Este documento describe los formularios implementados para el sistema de gestión de artículos académicos.

## Archivos Creados

- `app/forms/article_form.py` - Formularios principales
- `app/forms/utils.py` - Utilidades para poblar campos dinámicos
- `tests/test_forms.py` - Tests completos (20 tests, todos pasan)

## Formularios Implementados

### 1. ArticleForm

Formulario principal para crear y editar artículos académicos.

**Campos incluidos**:

#### Información Básica

- `titulo` - Título del artículo (obligatorio, max 500 chars)
- `titulo_revista` - Título de la revista (opcional, max 300 chars)

#### Clasificación

- `tipo_produccion_id` - Tipo de producción (obligatorio, SelectField dinámico)
- `proposito_id` - Propósito (opcional, SelectField dinámico)
- `lgac_id` - LGAC (opcional, SelectField dinámico)
- `estado_id` - Estado (obligatorio, SelectField dinámico)

#### Fechas

- `anio_publicacion` - Año de publicación (opcional, 1900-2100)
- `fecha_publicacion` - Fecha completa de publicación (opcional)
- `fecha_aceptacion` - Fecha de aceptación (opcional)

#### Datos de Publicación

- `revista_id` - Revista (opcional, SelectField dinámico)
- `volumen` - Volumen (opcional, max 20 chars)
- `numero` - Número (opcional, max 20 chars)
- `pagina_inicio` - Página inicio (opcional, número positivo)
- `pagina_fin` - Página fin (opcional, número positivo)

#### Identificadores

- `doi` - DOI (opcional, formato: 10.xxxx/xxxxx)
- `url` - URL (opcional, formato válido)
- `issn` - ISSN (opcional, formato: XXXX-XXXX)

#### Específico para Congresos

- `nombre_congreso` - Nombre del congreso (opcional, max 300 chars)

#### Indicadores

- `factor_impacto` - Factor de impacto (opcional, número positivo)
- `quartil` - Quartil (opcional, Q1/Q2/Q3/Q4)
- `citas` - Número de citas (opcional, default 0)

#### Opciones

- `para_curriculum` - Incluir en curriculum (checkbox, default True)

**Validaciones Personalizadas**:

1. **DOI**: Formato `10.xxxx/xxxxx` usando regex
2. **ISSN**: Formato `XXXX-XXXX` (8 dígitos con guión)
3. **Año**: Entre 1900 y año actual + 1
4. **Páginas**: página_fin >= página_inicio
5. **Fecha publicación**: No puede ser futura
6. **Fecha aceptación**: Debe ser antes de fecha de publicación
7. **Quartil**: Solo Q1, Q2, Q3, Q4 o vacío

**Ejemplo de uso en vista**:

```python
from app.forms import ArticleForm, populate_form_choices

@articles.route('/new', methods=['GET', 'POST'])
def new_article():
    form = ArticleForm()
    populate_form_choices(form)  # Pobla los SelectField desde DB

    if form.validate_on_submit():
        # Crear artículo con form.data
        articulo = Articulo(**form.data)
        db.session.add(articulo)
        db.session.commit()
        flash('Artículo creado exitosamente', 'success')
        return redirect(url_for('articles.detail', id=articulo.id))

    return render_template('articles/form.html', form=form)
```

### 2. ArticleSearchForm

Formulario para búsqueda y filtrado de artículos.

**Campos**:

- `query` - Búsqueda por texto libre
- `tipo_produccion_id` - Filtrar por tipo
- `estado_id` - Filtrar por estado
- `lgac_id` - Filtrar por LGAC
- `anio` - Filtrar por año
- `para_curriculum` - Filtrar por inclusión en curriculum

**Ejemplo de uso**:

```python
from app.forms import ArticleSearchForm, populate_form_choices

@articles.route('/')
def list_articles():
    form = ArticleSearchForm(request.args)
    populate_form_choices(form)

    # Construir query con filtros
    query = Articulo.buscar(
        query=form.query.data,
        tipo_id=form.tipo_produccion_id.data,
        estado_id=form.estado_id.data,
        lgac_id=form.lgac_id.data,
        anio=form.anio.data,
        para_curriculum=form.para_curriculum.data == '1'
    )

    articulos = query.paginate(page=1, per_page=20)
    return render_template('articles/list.html',
                         articulos=articulos,
                         form=form)
```

### 3. ArticleAuthorForm

Formulario para agregar autores a un artículo.

**Campos**:

- `autor_id` - Autor a agregar (obligatorio, SelectField dinámico)
- `orden` - Orden en lista de autores (obligatorio, >= 1)
- `es_corresponsal` - Es autor corresponsal (checkbox)

**Ejemplo de uso**:

```python
from app.forms import ArticleAuthorForm, populate_form_choices

@articles.route('/<int:id>/add_author', methods=['POST'])
def add_author(id):
    articulo = Articulo.query.get_or_404(id)
    form = ArticleAuthorForm()
    populate_form_choices(form)

    if form.validate_on_submit():
        autor = Autor.query.get(form.autor_id.data)
        articulo.agregar_autor(
            autor=autor,
            orden=form.orden.data,
            es_corresponsal=form.es_corresponsal.data
        )
        db.session.commit()
        flash('Autor agregado exitosamente', 'success')

    return redirect(url_for('articles.detail', id=id))
```

## Utilidades (app/forms/utils.py)

### populate_form_choices(form)

Puebla automáticamente todos los campos SelectField de un formulario con datos desde la base de datos.

```python
from app.forms import ArticleForm, populate_form_choices

form = ArticleForm()
populate_form_choices(form)  # Llena todos los SelectField
```

### Funciones individuales

Para casos específicos, puedes usar las funciones individuales:

- `populate_tipo_produccion_choices()` - Lista de tipos
- `populate_proposito_choices()` - Lista de propósitos
- `populate_lgac_choices()` - Lista de LGACs
- `populate_estado_choices()` - Lista de estados
- `populate_revista_choices()` - Lista de revistas
- `populate_autor_choices()` - Lista de autores

Todas retornan una lista de tuplas `(id, nombre)` con `(0, '-- Seleccione --')` como primera opción.

### validate_articulo_data(form_data)

Realiza validaciones adicionales de negocio que dependen de relaciones entre campos:

```python
from app.forms.utils import validate_articulo_data

form_data = {
    'estado_id': 1,
    'revista_id': None,
    'anio_publicacion': 2024
}

is_valid, errors = validate_articulo_data(form_data)
if not is_valid:
    for field, error in errors.items():
        flash(f'{field}: {error}', 'error')
```

**Validaciones de negocio**:

1. **Artículo publicado**: Debe tener revista y año
2. **Con DOI**: Se recomienda tener año
3. **Conference paper**: Debe tener nombre de congreso

## Tests

Se crearon 20 tests que cubren:

- ✅ Creación de formularios
- ✅ Validación de DOI (válido e inválido)
- ✅ Validación de ISSN (válido e inválido)
- ✅ Validación de año (válido, futuro, muy antiguo)
- ✅ Validación de páginas (válido e inválido)
- ✅ Validación de fechas (publicación futura, aceptación posterior a publicación)
- ✅ Validación de quartil
- ✅ Población de campos dinámicos
- ✅ Validaciones de negocio (publicado sin revista/año, conference paper sin congreso)
- ✅ Mapeo entre formularios y modelos

**Ejecutar tests**:

```bash
pytest tests/test_forms.py -v
```

**Resultado**: `20 passed in 4.65s` ✅

## Configuración Requerida

Para usar Flask-WTF, asegúrate de tener en `config.py`:

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    WTF_CSRF_ENABLED = True  # Protección CSRF activada
```

En templates, incluye el token CSRF:

```html
<form method="POST">
  {{ form.hidden_tag() }}
  <!-- Incluye token CSRF -->
  <!-- resto del formulario -->
</form>
```

## Próximos Pasos

Con los formularios implementados, ahora se pueden desarrollar:

1. **Controladores** (Fase 2, Paso 6) - Lógica de negocio para CRUD
2. **Vistas/Routes** (Fase 2, Paso 7) - Rutas para manejar requests
3. **Templates** (Fase 2, Paso 8) - Interfaz HTML para los formularios

Ver [MVP_ROADMAP.md](../docs/MVP_ROADMAP.md) para más detalles.
