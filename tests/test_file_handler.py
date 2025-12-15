"""
Tests para FileHandler
"""
import pytest
import os
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from werkzeug.datastructures import FileStorage
from io import BytesIO
from app.services.file_handler import FileHandler


@pytest.fixture
def temp_upload_folder():
    """Crea una carpeta temporal para uploads en tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def file_handler(temp_upload_folder):
    """Crea una instancia de FileHandler para tests"""
    return FileHandler(temp_upload_folder)


@pytest.fixture
def mock_pdf_file():
    """Crea un archivo PDF mock para testing"""
    pdf_content = b'%PDF-1.4\n%Mock PDF content for testing'
    return FileStorage(
        stream=BytesIO(pdf_content),
        filename='test_document.pdf',
        content_type='application/pdf'
    )


@pytest.fixture
def mock_invalid_file():
    """Crea un archivo no-PDF para testing"""
    content = b'This is not a PDF file'
    return FileStorage(
        stream=BytesIO(content),
        filename='test_document.txt',
        content_type='text/plain'
    )


class TestFileHandlerInitialization:
    """Tests de inicialización"""
    
    def test_init_creates_folder(self, temp_upload_folder):
        """Test que la carpeta se crea si no existe"""
        upload_path = os.path.join(temp_upload_folder, 'new_folder')
        handler = FileHandler(upload_path)
        
        assert os.path.exists(upload_path)
        assert handler.upload_folder == Path(upload_path)
    
    def test_init_with_custom_max_size(self, temp_upload_folder):
        """Test inicialización con tamaño máximo personalizado"""
        custom_size = 5 * 1024 * 1024  # 5 MB
        handler = FileHandler(temp_upload_folder, max_file_size=custom_size)
        
        assert handler.max_file_size == custom_size
    
    def test_init_with_default_max_size(self, temp_upload_folder):
        """Test inicialización con tamaño máximo por defecto"""
        handler = FileHandler(temp_upload_folder)
        
        assert handler.max_file_size == FileHandler.MAX_FILE_SIZE


class TestFileValidation:
    """Tests de validación de archivos"""
    
    def test_validate_valid_pdf(self, file_handler, mock_pdf_file):
        """Test validación de PDF válido"""
        is_valid, error = file_handler.validate_file(mock_pdf_file)
        
        assert is_valid is True
        assert error is None
    
    def test_validate_no_file(self, file_handler):
        """Test validación sin archivo"""
        is_valid, error = file_handler.validate_file(None)
        
        assert is_valid is False
        assert "No se proporcionó" in error
    
    def test_validate_no_filename(self, file_handler):
        """Test validación sin nombre de archivo"""
        file = FileStorage(
            stream=BytesIO(b'content'),
            filename='',
            content_type='application/pdf'
        )
        is_valid, error = file_handler.validate_file(file)
        
        assert is_valid is False
        # Werkzeug trata filename='' como no file
        assert error is not None
    
    def test_validate_invalid_extension(self, file_handler, mock_invalid_file):
        """Test validación con extensión inválida"""
        is_valid, error = file_handler.validate_file(mock_invalid_file)
        
        assert is_valid is False
        assert "Extensión no permitida" in error
    
    def test_validate_invalid_mime_type(self, file_handler):
        """Test validación con tipo MIME inválido"""
        file = FileStorage(
            stream=BytesIO(b'content'),
            filename='test.pdf',
            content_type='text/plain'
        )
        is_valid, error = file_handler.validate_file(file)
        
        assert is_valid is False
        assert "Tipo de archivo no válido" in error


class TestUniqueFilename:
    """Tests de generación de nombres únicos"""
    
    def test_generate_unique_filename_basic(self, file_handler):
        """Test generación de nombre único básico"""
        filename = file_handler.generate_unique_filename('document.pdf')
        
        assert filename.endswith('.pdf')
        assert len(filename) > len('document.pdf')
    
    def test_generate_unique_filename_with_prefix(self, file_handler):
        """Test generación con prefijo"""
        filename = file_handler.generate_unique_filename('document.pdf', prefix='article_123')
        
        assert filename.startswith('article_123_')
        assert filename.endswith('.pdf')
    
    def test_generate_unique_filenames_are_different(self, file_handler):
        """Test que nombres generados son únicos"""
        import time
        filename1 = file_handler.generate_unique_filename('document.pdf')
        time.sleep(0.001)  # Pequeño delay para asegurar diferencia
        filename2 = file_handler.generate_unique_filename('document.pdf')
        
        assert filename1 != filename2
    
    def test_generate_filename_preserves_extension(self, file_handler):
        """Test que la extensión se preserva"""
        filename = file_handler.generate_unique_filename('TEST.PDF')
        
        assert filename.endswith('.pdf')  # lowercase


class TestFileSaving:
    """Tests de guardado de archivos"""
    
    def test_save_valid_file(self, file_handler, mock_pdf_file):
        """Test guardar archivo válido"""
        success, error, filepath = file_handler.save_file(mock_pdf_file)
        
        assert success is True
        assert error is None
        assert filepath is not None
        assert os.path.exists(filepath)
    
    def test_save_file_with_prefix(self, file_handler, mock_pdf_file):
        """Test guardar con prefijo"""
        success, error, filepath = file_handler.save_file(mock_pdf_file, prefix='art_1')
        
        assert success is True
        assert 'art_1' in os.path.basename(filepath)
    
    def test_save_invalid_file(self, file_handler, mock_invalid_file):
        """Test guardar archivo inválido"""
        success, error, filepath = file_handler.save_file(mock_invalid_file)
        
        assert success is False
        assert error is not None
        assert filepath is None
    
    def test_saved_file_exists(self, file_handler, mock_pdf_file):
        """Test que el archivo guardado existe"""
        success, error, filepath = file_handler.save_file(mock_pdf_file)
        
        assert os.path.isfile(filepath)


class TestFileDeletion:
    """Tests de eliminación de archivos"""
    
    def test_delete_existing_file(self, file_handler, mock_pdf_file):
        """Test eliminar archivo existente"""
        # Primero guardar
        success, error, filepath = file_handler.save_file(mock_pdf_file)
        assert success
        
        # Luego eliminar
        success, error = file_handler.delete_file(filepath)
        
        assert success is True
        assert error is None
        assert not os.path.exists(filepath)
    
    def test_delete_nonexistent_file(self, file_handler):
        """Test eliminar archivo que no existe"""
        filepath = os.path.join(file_handler.upload_folder, 'nonexistent.pdf')
        success, error = file_handler.delete_file(filepath)
        
        assert success is False
        assert "no existe" in error
    
    def test_delete_file_outside_upload_folder(self, file_handler):
        """Test no permite eliminar archivos fuera de upload folder"""
        outside_path = '/tmp/some_file.pdf'
        success, error = file_handler.delete_file(outside_path)
        
        assert success is False
        # Puede ser "no existe" o "fuera de la carpeta" dependiendo del OS
        assert error is not None


class TestFileInfo:
    """Tests de información de archivos"""
    
    def test_get_file_info_existing(self, file_handler, mock_pdf_file):
        """Test obtener info de archivo existente"""
        success, error, filepath = file_handler.save_file(mock_pdf_file)
        assert success
        
        info = file_handler.get_file_info(filepath)
        
        assert info is not None
        assert 'filename' in info
        assert 'size_bytes' in info
        assert 'size_mb' in info
        assert 'created_at' in info
        assert 'modified_at' in info
        assert info['exists'] is True
    
    def test_get_file_info_nonexistent(self, file_handler):
        """Test obtener info de archivo inexistente"""
        info = file_handler.get_file_info('/nonexistent/file.pdf')
        
        assert info is None
    
    def test_file_exists_true(self, file_handler, mock_pdf_file):
        """Test file_exists retorna True para archivo existente"""
        success, error, filepath = file_handler.save_file(mock_pdf_file)
        assert success
        
        exists = file_handler.file_exists(filepath)
        
        assert exists is True
    
    def test_file_exists_false(self, file_handler):
        """Test file_exists retorna False para archivo inexistente"""
        exists = file_handler.file_exists('/nonexistent/file.pdf')
        
        assert exists is False


class TestCleanup:
    """Tests de limpieza de archivos antiguos"""
    
    def test_cleanup_no_old_files(self, file_handler, mock_pdf_file):
        """Test cleanup cuando no hay archivos antiguos"""
        # Guardar archivo reciente
        file_handler.save_file(mock_pdf_file)
        
        # Intentar limpiar archivos de más de 1 día
        deleted_count, errors = file_handler.cleanup_old_files(days_old=1)
        
        assert deleted_count == 0
        assert len(errors) == 0
    
    def test_cleanup_old_files(self, file_handler, mock_pdf_file, temp_upload_folder):
        """Test cleanup elimina archivos antiguos"""
        # Guardar archivo
        success, error, filepath = file_handler.save_file(mock_pdf_file)
        assert success
        
        # Modificar fecha del archivo para que sea antiguo
        old_time = (datetime.now() - timedelta(days=35)).timestamp()
        os.utime(filepath, (old_time, old_time))
        
        # Limpiar archivos de más de 30 días
        deleted_count, errors = file_handler.cleanup_old_files(days_old=30)
        
        assert deleted_count == 1
        assert not os.path.exists(filepath)


class TestUploadStats:
    """Tests de estadísticas de uploads"""
    
    def test_get_stats_empty_folder(self, file_handler):
        """Test estadísticas con carpeta vacía"""
        stats = file_handler.get_upload_stats()
        
        assert stats['total_files'] == 0
        assert stats['total_size_bytes'] == 0
        assert stats['oldest_file_date'] is None
        assert stats['newest_file_date'] is None
    
    def test_get_stats_with_files(self, file_handler, mock_pdf_file):
        """Test estadísticas con archivos"""
        import time
        # Guardar varios archivos
        file_handler.save_file(mock_pdf_file)
        mock_pdf_file.stream.seek(0)  # Reset stream
        time.sleep(0.01)  # Asegurar nombre diferente
        file_handler.save_file(mock_pdf_file)
        
        stats = file_handler.get_upload_stats()
        
        assert stats['total_files'] == 2
        assert stats['total_size_bytes'] > 0
        assert stats['oldest_file_date'] is not None
        assert stats['newest_file_date'] is not None
