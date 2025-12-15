"""
Blueprint de catálogos - Gestión de catálogos maestros
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.controllers.catalog_controller import CatalogController
from app.forms.catalog_forms import get_catalog_form
import logging

logger = logging.getLogger(__name__)

catalogs_bp = Blueprint('catalogs', __name__, url_prefix='/catalogs')


@catalogs_bp.route('/')
def index():
    """
    Dashboard de catálogos - Lista todos los catálogos disponibles.
    GET /catalogs
    """
    catalogs = CatalogController.get_catalog_list()
    return render_template('catalogs/index.html', catalogs=catalogs)


@catalogs_bp.route('/<catalog_name>')
def list_catalog(catalog_name):
    """
    Lista registros de un catálogo específico.
    GET /catalogs/<catalog_name>?page=1&query=texto&show_inactive=false
    """
    # Verificar que el catálogo existe
    config = CatalogController.get_config(catalog_name)
    if not config:
        flash(f'Catálogo "{catalog_name}" no encontrado', 'error')
        return redirect(url_for('catalogs.index'))
    
    # Obtener parámetros
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '').strip()
    show_inactive = request.args.get('show_inactive', 'false').lower() == 'true'
    
    # Obtener registros
    pagination, error = CatalogController.get_all(
        catalog_name,
        page=page,
        per_page=50,
        query=query,
        show_inactive=show_inactive
    )
    
    if error:
        flash(f'Error al cargar catálogo: {error}', 'error')
        return redirect(url_for('catalogs.index'))
    
    return render_template(
        'catalogs/list.html',
        catalog_name=catalog_name,
        config=config,
        pagination=pagination,
        query=query,
        show_inactive=show_inactive
    )


@catalogs_bp.route('/<catalog_name>/new', methods=['GET', 'POST'])
def new(catalog_name):
    """
    Formulario para crear nuevo registro en catálogo.
    GET /catalogs/<catalog_name>/new - Muestra formulario
    POST /catalogs/<catalog_name>/new - Procesa creación
    """
    config = CatalogController.get_config(catalog_name)
    if not config:
        flash(f'Catálogo "{catalog_name}" no encontrado', 'error')
        return redirect(url_for('catalogs.index'))
    
    # Obtener formulario apropiado
    form = get_catalog_form(catalog_name)
    if not form:
        flash(f'Formulario no disponible para "{catalog_name}"', 'error')
        return redirect(url_for('catalogs.list_catalog', catalog_name=catalog_name))
    
    if form.validate_on_submit():
        # Extraer datos del formulario
        data = {}
        for field in form:
            if field.name not in ['submit', 'csrf_token']:
                value = field.data
                # Si es SelectField con valor 0, convertir a None
                if field.name.endswith('_id') and value == 0:
                    value = None
                data[field.name] = value
        
        # Crear registro
        registro, error = CatalogController.create(catalog_name, data)
        
        if error:
            flash(f'Error al crear registro: {error}', 'error')
        else:
            flash(f'{config["singular"]} creado exitosamente', 'success')
            return redirect(url_for('catalogs.list_catalog', catalog_name=catalog_name))
    
    return render_template(
        'catalogs/form.html',
        catalog_name=catalog_name,
        config=config,
        form=form,
        registro=None
    )


@catalogs_bp.route('/<catalog_name>/<int:id>')
def show(catalog_name, id):
    """
    Ver detalle de un registro.
    GET /catalogs/<catalog_name>/<id>
    """
    config = CatalogController.get_config(catalog_name)
    if not config:
        flash(f'Catálogo "{catalog_name}" no encontrado', 'error')
        return redirect(url_for('catalogs.index'))
    
    registro, error = CatalogController.get_by_id(catalog_name, id)
    
    if error:
        flash(error, 'error')
        return redirect(url_for('catalogs.list_catalog', catalog_name=catalog_name))
    
    return render_template(
        'catalogs/detail.html',
        catalog_name=catalog_name,
        config=config,
        registro=registro
    )


@catalogs_bp.route('/<catalog_name>/<int:id>/edit', methods=['GET', 'POST'])
def edit(catalog_name, id):
    """
    Formulario para editar registro existente.
    GET /catalogs/<catalog_name>/<id>/edit - Muestra formulario
    POST /catalogs/<catalog_name>/<id>/edit - Procesa actualización
    """
    config = CatalogController.get_config(catalog_name)
    if not config:
        flash(f'Catálogo "{catalog_name}" no encontrado', 'error')
        return redirect(url_for('catalogs.index'))
    
    # Obtener registro actual
    registro, error = CatalogController.get_by_id(catalog_name, id)
    
    if error:
        flash(error, 'error')
        return redirect(url_for('catalogs.list_catalog', catalog_name=catalog_name))
    
    # Obtener formulario pre-llenado
    form = get_catalog_form(catalog_name, obj=registro)
    if not form:
        flash(f'Formulario no disponible para "{catalog_name}"', 'error')
        return redirect(url_for('catalogs.list_catalog', catalog_name=catalog_name))
    
    if form.validate_on_submit():
        # Extraer datos del formulario
        data = {}
        for field in form:
            if field.name not in ['submit', 'csrf_token']:
                value = field.data
                # Si es SelectField con valor 0, convertir a None
                if field.name.endswith('_id') and value == 0:
                    value = None
                # Solo incluir si cambió
                if getattr(registro, field.name, None) != value:
                    data[field.name] = value
        
        # Actualizar si hay cambios
        if data:
            registro_actualizado, error = CatalogController.update(catalog_name, id, data)
            
            if error:
                flash(f'Error al actualizar registro: {error}', 'error')
            else:
                flash(f'{config["singular"]} actualizado exitosamente', 'success')
                return redirect(url_for('catalogs.show', catalog_name=catalog_name, id=id))
        else:
            flash('No se detectaron cambios', 'info')
            return redirect(url_for('catalogs.show', catalog_name=catalog_name, id=id))
    
    return render_template(
        'catalogs/form.html',
        catalog_name=catalog_name,
        config=config,
        form=form,
        registro=registro
    )


@catalogs_bp.route('/<catalog_name>/<int:id>/delete', methods=['POST'])
def delete(catalog_name, id):
    """
    Eliminar registro (soft delete por defecto).
    POST /catalogs/<catalog_name>/<id>/delete
    """
    config = CatalogController.get_config(catalog_name)
    if not config:
        flash(f'Catálogo "{catalog_name}" no encontrado', 'error')
        return redirect(url_for('catalogs.index'))
    
    # Verificar si se solicita eliminación física
    hard_delete = request.form.get('hard_delete', 'false').lower() == 'true'
    
    success, error = CatalogController.delete(catalog_name, id, soft=not hard_delete)
    
    if error:
        flash(f'Error al eliminar registro: {error}', 'error')
    else:
        tipo = 'permanentemente' if hard_delete else 'lógicamente'
        flash(f'{config["singular"]} eliminado {tipo}', 'success')
    
    return redirect(url_for('catalogs.list_catalog', catalog_name=catalog_name))


@catalogs_bp.route('/<catalog_name>/<int:id>/toggle', methods=['POST'])
def toggle_active(catalog_name, id):
    """
    Activar/desactivar un registro.
    POST /catalogs/<catalog_name>/<id>/toggle
    """
    config = CatalogController.get_config(catalog_name)
    if not config:
        flash(f'Catálogo "{catalog_name}" no encontrado', 'error')
        return redirect(url_for('catalogs.index'))
    
    registro, error = CatalogController.toggle_active(catalog_name, id)
    
    if error:
        flash(f'Error: {error}', 'error')
    else:
        estado = 'activado' if registro.activo else 'desactivado'
        flash(f'{config["singular"]} {estado} exitosamente', 'success')
    
    # Redirigir según el referrer
    return redirect(request.referrer or url_for('catalogs.list_catalog', catalog_name=catalog_name))
