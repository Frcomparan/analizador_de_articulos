"""
Punto de entrada de la aplicación
"""
import os
from app import create_app
from app.services.background_worker import BackgroundWorker

# Crear la aplicación
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

# Iniciar worker en background
worker = BackgroundWorker(app)
worker.start()

if __name__ == '__main__':
    # Ejecutar aplicación
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
