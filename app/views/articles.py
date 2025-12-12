"""
Blueprint de artículos - CRUD y gestión de artículos
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

articles_bp = Blueprint('articles', __name__, url_prefix='/articles')


@articles_bp.route('/')
def index():
    """Lista de artículos."""
    return render_template('articles/index.html')


@articles_bp.route('/new')
def new():
    """Formulario para nuevo artículo."""
    return render_template('articles/form.html')


@articles_bp.route('/<int:id>')
def show(id):
    """Ver detalle de un artículo."""
    return render_template('articles/show.html')


@articles_bp.route('/<int:id>/edit')
def edit(id):
    """Formulario para editar artículo."""
    return render_template('articles/form.html')
