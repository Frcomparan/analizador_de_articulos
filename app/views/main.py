"""
Blueprint principal - Página de inicio y navegación general
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Página de inicio."""
    return render_template('main/index.html')


@main_bp.route('/about')
def about():
    """Página de información sobre el sistema."""
    return render_template('main/about.html')
