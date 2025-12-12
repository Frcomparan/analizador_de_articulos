"""
Blueprint de catálogos - Gestión de catálogos del sistema
"""
from flask import Blueprint, render_template, jsonify

catalogs_bp = Blueprint('catalogs', __name__, url_prefix='/catalogs')


@catalogs_bp.route('/')
def index():
    """Lista de catálogos disponibles."""
    return render_template('catalogs/index.html')


@catalogs_bp.route('/tipos-produccion')
def tipos_produccion():
    """Lista de tipos de producción."""
    return render_template('catalogs/tipos_produccion.html')


@catalogs_bp.route('/estados')
def estados():
    """Lista de estados."""
    return render_template('catalogs/estados.html')


@catalogs_bp.route('/lgac')
def lgac():
    """Lista de LGAC."""
    return render_template('catalogs/lgac.html')


@catalogs_bp.route('/indexaciones')
def indexaciones():
    """Lista de indexaciones."""
    return render_template('catalogs/indexaciones.html')
