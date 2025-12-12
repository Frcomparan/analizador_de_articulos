"""
Blueprint de carga de archivos - Subida y procesamiento de PDFs
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for

uploads_bp = Blueprint('uploads', __name__, url_prefix='/uploads')


@uploads_bp.route('/')
def index():
    """Página de carga de archivos."""
    return render_template('uploads/index.html')


@uploads_bp.route('/process', methods=['POST'])
def process():
    """Procesar archivo subido."""
    # TODO: Implementar procesamiento de PDFs
    return redirect(url_for('uploads.index'))


@uploads_bp.route('/history')
def history():
    """Historial de archivos procesados."""
    return render_template('uploads/history.html')
