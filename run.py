"""
Punto de entrada de la aplicación
"""
import os
from app import create_app

# Crear la aplicación
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

# El background worker se iniciará en fases posteriores
# from app.services.background_worker import BackgroundWorker
# worker = BackgroundWorker(app)
# worker.start()

if __name__ == '__main__':
    # Ejecutar aplicación
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
