"""
Inicialización de la aplicación Flask usando Factory Pattern
"""
import os
import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

# Inicializar extensiones (sin app todavía)
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='development'):
    """
    Factory function para crear la aplicación Flask
    
    Args:
        config_name: Nombre de la configuración a usar
        
    Returns:
        app: Instancia de Flask configurada
    """
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Importar modelos para que Flask-Migrate los detecte
    from app import models  # noqa: F401
    
    # Registrar blueprints
    from app.views.main import main_bp
    from app.views.articles import articles_bp
    from app.views.catalogs import catalogs_bp
    from app.views.reports import reports_bp
    from app.views.uploads import uploads_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(catalogs_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(uploads_bp)
    
    # Crear directorios necesarios
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)
    
    # Registrar comandos CLI
    register_commands(app)
    
    return app


def register_commands(app):
    """Registra comandos CLI personalizados."""
    
    @app.cli.command('seed-catalogs')
    def seed_catalogs_command():
        """Pobla los catálogos con datos iniciales."""
        from scripts.seed_catalogs import seed_all
        seed_all()
    
    @app.cli.command('init-db')
    def init_db_command():
        """Crea todas las tablas de la base de datos."""
        db.create_all()
        click.echo('✓ Base de datos inicializada.')
    
    @app.cli.command('reset-db')
    @click.confirmation_option(prompt='¿Estás seguro de que quieres eliminar todos los datos?')
    def reset_db_command():
        """Elimina y recrea todas las tablas (¡CUIDADO!)."""
        db.drop_all()
        db.create_all()
        click.echo('✓ Base de datos reiniciada.')

