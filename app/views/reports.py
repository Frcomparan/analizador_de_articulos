"""
Blueprint de reportes - Generación de reportes y exportación
"""
from flask import Blueprint, render_template, send_file

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')


@reports_bp.route('/')
def index():
    """Panel de reportes."""
    return render_template('reports/index.html')


@reports_bp.route('/export/excel')
def export_excel():
    """Exportar artículos a Excel."""
    # TODO: Implementar exportación a Excel
    return "Exportación a Excel - Por implementar"


@reports_bp.route('/incomplete')
def incomplete():
    """Lista de artículos con información incompleta."""
    return render_template('reports/incomplete.html')
