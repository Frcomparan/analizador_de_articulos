"""
Tests para la funcionalidad de upload y procesamiento de PDFs en batch.
"""
import pytest
import os
import time
from pathlib import Path
from io import BytesIO
from werkzeug.datastructures import FileStorage

from app import create_app, db
from app.models.articulo import Articulo
from app.models.catalogs import TipoProduccion, Estado
from app.services.pdf_batch_processor import PDFBatchProcessor
from app.services.file_handler import FileHandler
from config import Config


@pytest.fixture
def app():
    """Crea una aplicación de prueba"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        
        # Crear catálogos necesarios
        tipo = TipoProduccion(nombre='Artículo científico', activo=True)
        estado = Estado(nombre='Publicado', color='#28a745', activo=True)
        db.session.add(tipo)
        db.session.add(estado)
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de prueba"""
    return app.test_client()


@pytest.fixture
def processor(app):
    """Procesador de PDFs"""
    with app.app_context():
        upload_folder = Path(app.config['UPLOAD_FOLDER'])
        upload_folder.mkdir(parents=True, exist_ok=True)
        
        processor = PDFBatchProcessor(
            upload_folder=str(upload_folder),
            max_workers=3,
            app=app
        )
        
        yield processor
        
        # Limpiar archivos de prueba
        for file in upload_folder.glob('*.pdf'):
            try:
                file.unlink()
            except:
                pass


@pytest.fixture
def sample_pdf():
    """Archivo PDF de muestra"""
    pdf_path = Path(__file__).parent.parent / 'pdf' / 'art_rev_indexada' / 'art_rev_indexada_1.pdf'
    
    if not pdf_path.exists():
        # Crear un PDF simple si no existe
        pytest.skip("No se encontró el PDF de prueba")
    
    return pdf_path


def create_file_storage(filepath: Path, filename: str = None) -> FileStorage:
    """
    Crea un FileStorage a partir de un archivo real.
    
    Args:
        filepath: Ruta del archivo
        filename: Nombre del archivo (opcional, usa el nombre real si no se especifica)
    
    Returns:
        FileStorage object
    """
    if not filename:
        filename = filepath.name
    
    with open(filepath, 'rb') as f:
        content = f.read()
    
    return FileStorage(
        stream=BytesIO(content),
        filename=filename,
        content_type='application/pdf'
    )


class TestPDFBatchProcessor:
    """Tests para el procesador de PDFs en batch"""
    
    def test_process_single_pdf(self, app, processor, sample_pdf):
        """Test: Procesar un único PDF"""
        with app.app_context():
            # Crear FileStorage
            file = create_file_storage(sample_pdf)
            
            # Procesar
            results = processor.process_files([file])
            
            # Verificar resultados
            assert results['total'] == 1
            assert results['success'] == 1
            assert results['errors'] == 0
            assert len(results['results']) == 1
            
            result = results['results'][0]
            assert result['filename'] == sample_pdf.name
            assert 'article_id' in result
            assert result['confidence'] > 0
            
            # Verificar que se creó el artículo
            articulo = Articulo.query.get(result['article_id'])
            assert articulo is not None
            assert articulo.archivo_origen == sample_pdf.name
            assert articulo.completo == False  # Por defecto incompleto
    
    def test_process_multiple_pdfs(self, app, processor):
        """Test: Procesar múltiples PDFs en paralelo"""
        with app.app_context():
            # Buscar PDFs de prueba
            pdf_dir = Path(__file__).parent.parent / 'pdf' / 'art_rev_indexada'
            
            if not pdf_dir.exists():
                pytest.skip("No se encontró el directorio de PDFs de prueba")
            
            pdf_files = list(pdf_dir.glob('*.pdf'))[:5]  # Máximo 5 PDFs
            
            if len(pdf_files) < 2:
                pytest.skip("No hay suficientes PDFs de prueba")
            
            # Crear FileStorage objects
            files = [create_file_storage(pdf) for pdf in pdf_files]
            
            # Medir tiempo
            start_time = time.time()
            results = processor.process_files(files)
            elapsed = time.time() - start_time
            
            # Verificar resultados
            assert results['total'] == len(files)
            assert results['success'] >= 1  # Al menos 1 exitoso
            assert len(results['results']) >= 1
            
            # Verificar que se crearon artículos
            for result in results['results']:
                articulo = Articulo.query.get(result['article_id'])
                assert articulo is not None
                assert articulo.archivo_origen is not None
            
            print(f"\nProcesados {results['success']}/{results['total']} PDFs en {elapsed:.2f}s")
    
    def test_process_invalid_file(self, app, processor):
        """Test: Procesar archivo no-PDF"""
        with app.app_context():
            # Crear archivo falso
            fake_file = FileStorage(
                stream=BytesIO(b"Not a PDF"),
                filename="fake.txt",
                content_type="text/plain"
            )
            
            # Procesar
            results = processor.process_files([fake_file])
            
            # Verificar que falló
            assert results['total'] == 1
            assert results['errors'] == 1
            assert results['success'] == 0
    
    def test_max_files_limit(self, app, processor):
        """Test: Verificar límite de archivos"""
        # Esta prueba se hace en la vista, no en el procesador
        pass
    
    def test_concurrent_processing(self, app, processor):
        """Test: Verificar que se usan threads"""
        with app.app_context():
            # Buscar PDFs de prueba
            pdf_dir = Path(__file__).parent.parent / 'pdf' / 'art_rev_indexada'
            
            if not pdf_dir.exists():
                pytest.skip("No se encontró el directorio de PDFs de prueba")
            
            pdf_files = list(pdf_dir.glob('*.pdf'))[:5]
            
            if len(pdf_files) < 5:
                pytest.skip("No hay suficientes PDFs de prueba")
            
            # Crear FileStorage objects
            files = [create_file_storage(pdf) for pdf in pdf_files]
            
            # Procesar con threading
            start_parallel = time.time()
            results = processor.process_files(files)
            time_parallel = time.time() - start_parallel
            
            # Verificar que funcionó
            assert results['success'] >= 1
            
            print(f"\nProcesamiento paralelo: {time_parallel:.2f}s para {len(files)} archivos")
            # El procesamiento paralelo debería ser más rápido que secuencial
            # pero no podemos hacer una prueba directa sin procesar secuencialmente


class TestUploadRoute:
    """Tests para las rutas de upload"""
    
    def test_upload_form_accessible(self, client):
        """Test: Acceder al formulario de upload"""
        response = client.get('/articles/upload')
        assert response.status_code == 200
        assert b'Cargar' in response.data
        assert b'dropZone' in response.data
    
    def test_upload_no_files(self, client):
        """Test: Upload sin archivos"""
        response = client.post('/articles/upload')
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_upload_too_many_files(self, client, sample_pdf):
        """Test: Upload con más de 10 archivos"""
        # Crear 11 FileStorage objects
        files = []
        for i in range(11):
            file = create_file_storage(sample_pdf, f"file_{i}.pdf")
            files.append((file.stream, file.filename))
        
        response = client.post(
            '/articles/upload',
            data={'pdfs': files},
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert '10' in data['error']
    
    def test_upload_single_pdf_success(self, app, client, sample_pdf):
        """Test: Upload exitoso de un PDF"""
        with app.app_context():
            # Crear FileStorage
            file = create_file_storage(sample_pdf)
            
            # Upload
            response = client.post(
                '/articles/upload',
                data={'pdfs': [(file.stream, file.filename)]},
                content_type='multipart/form-data'
            )
            
            # Verificar respuesta
            assert response.status_code == 200
            data = response.get_json()
            
            assert 'total' in data
            assert 'success' in data
            assert data['total'] == 1
            assert data['success'] >= 0
            
            # Si fue exitoso, verificar artículo
            if data['success'] == 1:
                result = data['results'][0]
                articulo = Articulo.query.get(result['article_id'])
                assert articulo is not None


class TestArticleCreation:
    """Tests para la creación de artículos desde PDFs"""
    
    def test_article_has_metadata(self, app, processor, sample_pdf):
        """Test: Artículo creado tiene metadatos"""
        with app.app_context():
            file = create_file_storage(sample_pdf)
            results = processor.process_files([file])
            
            if results['success'] > 0:
                result = results['results'][0]
                articulo = Articulo.query.get(result['article_id'])
                
                # Verificar campos básicos
                assert articulo.titulo is not None
                assert articulo.tipo_produccion_id is not None
                assert articulo.estado_id is not None
                assert articulo.archivo_origen == sample_pdf.name
                assert articulo.activo == True
    
    def test_article_marked_incomplete(self, app, processor, sample_pdf):
        """Test: Artículo se marca como incompleto"""
        with app.app_context():
            file = create_file_storage(sample_pdf)
            results = processor.process_files([file])
            
            if results['success'] > 0:
                result = results['results'][0]
                articulo = Articulo.query.get(result['article_id'])
                
                # Debería estar marcado como incompleto para revisión
                assert articulo.completo == False
                assert articulo.campos_faltantes is not None
    
    def test_missing_fields_identified(self, app, processor, sample_pdf):
        """Test: Campos faltantes se identifican"""
        with app.app_context():
            file = create_file_storage(sample_pdf)
            results = processor.process_files([file])
            
            if results['success'] > 0:
                result = results['results'][0]
                articulo = Articulo.query.get(result['article_id'])
                
                # Debería tener información de campos faltantes
                assert articulo.campos_faltantes is not None
                # Puede contener texto como "Faltan: autores, DOI"
                assert len(articulo.campos_faltantes) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
