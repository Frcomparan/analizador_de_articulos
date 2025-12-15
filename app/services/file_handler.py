"""
Servicio para manejo de archivos (upload, validación, limpieza).
Gestiona archivos PDF subidos por los usuarios.
"""
import os
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple, Optional, List
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


class FileHandler:
    """
    Maneja operaciones de archivos: upload, validación, nombres únicos, limpieza.
    """
    
    # Tipos MIME permitidos para PDFs
    ALLOWED_MIME_TYPES = {
        'application/pdf',
        'application/x-pdf',
        'application/acrobat',
        'applications/vnd.pdf',
        'text/pdf',
        'text/x-pdf'
    }
    
    # Extensiones permitidas
    ALLOWED_EXTENSIONS = {'.pdf'}
    
    # Tamaño máximo: 10 MB
    MAX_FILE_SIZE = 10 * 1024 * 1024  # bytes
    
    def __init__(self, upload_folder: str, max_file_size: Optional[int] = None):
        """
        Inicializa el manejador de archivos.
        
        Args:
            upload_folder: Ruta absoluta a la carpeta de uploads
            max_file_size: Tamaño máximo en bytes (opcional)
        """
        self.upload_folder = Path(upload_folder)
        self.max_file_size = max_file_size or self.MAX_FILE_SIZE
        
        # Crear carpeta si no existe
        self.upload_folder.mkdir(parents=True, exist_ok=True)
    
    def validate_file(self, file: FileStorage) -> Tuple[bool, Optional[str]]:
        """
        Valida un archivo subido.
        
        Args:
            file: Archivo de Werkzeug FileStorage
            
        Returns:
            Tupla (es_valido, mensaje_error)
            - Si válido: (True, None)
            - Si inválido: (False, mensaje_error)
        """
        # Verificar que hay un archivo
        if not file:
            return False, "No se proporcionó ningún archivo"
        
        if not file.filename or file.filename.strip() == '':
            return False, "El archivo no tiene nombre"
        
        # Verificar extensión
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.ALLOWED_EXTENSIONS:
            return False, f"Extensión no permitida. Solo se aceptan archivos PDF"
        
        # Verificar tipo MIME
        if file.content_type not in self.ALLOWED_MIME_TYPES:
            return False, f"Tipo de archivo no válido: {file.content_type}. Solo se aceptan PDFs"
        
        # Verificar tamaño (si es posible)
        if hasattr(file, 'content_length') and file.content_length:
            if file.content_length > self.max_file_size:
                max_mb = self.max_file_size / (1024 * 1024)
                return False, f"Archivo demasiado grande. Máximo permitido: {max_mb:.1f} MB"
        
        return True, None
    
    def generate_unique_filename(self, original_filename: str, prefix: str = "") -> str:
        """
        Genera un nombre de archivo único y seguro.
        
        Args:
            original_filename: Nombre original del archivo
            prefix: Prefijo opcional (ej: 'article_123')
            
        Returns:
            Nombre único: [prefix_]timestamp_hash.pdf
        """
        # Obtener extensión
        file_ext = Path(original_filename).suffix.lower()
        
        # Generar timestamp con microsegundos para mayor unicidad
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d_%H%M%S')
        
        # Generar hash corto del nombre original + timestamp + microsegundos para unicidad
        hash_input = f"{original_filename}{timestamp}{now.microsecond}{time.time()}".encode('utf-8')
        file_hash = hashlib.md5(hash_input).hexdigest()[:8]
        
        # Construir nombre
        parts = []
        if prefix:
            parts.append(secure_filename(prefix))
        parts.append(timestamp)
        parts.append(file_hash)
        
        unique_name = "_".join(parts) + file_ext
        
        return unique_name
    
    def save_file(self, file: FileStorage, prefix: str = "") -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Valida y guarda un archivo.
        
        Args:
            file: Archivo de Werkzeug FileStorage
            prefix: Prefijo opcional para el nombre
            
        Returns:
            Tupla (exito, mensaje_error, filepath)
            - Si exitoso: (True, None, 'ruta/al/archivo.pdf')
            - Si falla: (False, 'mensaje de error', None)
        """
        # Validar archivo
        is_valid, error = self.validate_file(file)
        if not is_valid:
            return False, error, None
        
        try:
            # Generar nombre único
            unique_filename = self.generate_unique_filename(file.filename, prefix)
            
            # Construir ruta completa
            filepath = self.upload_folder / unique_filename
            
            # Guardar archivo
            file.save(str(filepath))
            
            # Verificar que se guardó
            if not filepath.exists():
                return False, "Error al guardar el archivo", None
            
            # Verificar tamaño del archivo guardado
            file_size = filepath.stat().st_size
            if file_size > self.max_file_size:
                # Eliminar archivo si es demasiado grande
                filepath.unlink()
                max_mb = self.max_file_size / (1024 * 1024)
                return False, f"Archivo demasiado grande: {file_size / (1024 * 1024):.1f} MB. Máximo: {max_mb:.1f} MB", None
            
            # Retornar ruta relativa desde la carpeta de uploads
            return True, None, str(filepath)
            
        except Exception as e:
            return False, f"Error al guardar archivo: {str(e)}", None
    
    def delete_file(self, filepath: str) -> Tuple[bool, Optional[str]]:
        """
        Elimina un archivo.
        
        Args:
            filepath: Ruta al archivo a eliminar
            
        Returns:
            Tupla (exito, mensaje_error)
            - Si exitoso: (True, None)
            - Si falla: (False, 'mensaje de error')
        """
        try:
            file_path = Path(filepath)
            
            # Verificar que está dentro de la carpeta de uploads (seguridad)
            try:
                file_path_resolved = file_path.resolve()
                upload_folder_resolved = self.upload_folder.resolve()
                
                if not str(file_path_resolved).startswith(str(upload_folder_resolved)):
                    return False, "No se puede eliminar archivos fuera de la carpeta de uploads"
            except (OSError, ValueError):
                return False, "Ruta de archivo inválida"
            
            if not file_path.exists():
                return False, f"El archivo no existe: {filepath}"
            
            file_path.unlink()
            return True, None
            
        except Exception as e:
            return False, f"Error al eliminar archivo: {str(e)}"
    
    def cleanup_old_files(self, days_old: int = 30) -> Tuple[int, List[str]]:
        """
        Elimina archivos más antiguos que X días.
        
        Args:
            days_old: Edad mínima en días para eliminar
            
        Returns:
            Tupla (cantidad_eliminada, lista_de_errores)
        """
        deleted_count = 0
        errors = []
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        try:
            # Buscar todos los PDFs
            for pdf_file in self.upload_folder.rglob('*.pdf'):
                try:
                    # Obtener fecha de modificación
                    file_mtime = datetime.fromtimestamp(pdf_file.stat().st_mtime)
                    
                    # Si es más antiguo que cutoff_date, eliminar
                    if file_mtime < cutoff_date:
                        pdf_file.unlink()
                        deleted_count += 1
                        
                except Exception as e:
                    errors.append(f"Error al procesar {pdf_file.name}: {str(e)}")
                    
        except Exception as e:
            errors.append(f"Error al buscar archivos: {str(e)}")
        
        return deleted_count, errors
    
    def get_file_info(self, filepath: str) -> Optional[dict]:
        """
        Obtiene información de un archivo.
        
        Args:
            filepath: Ruta al archivo
            
        Returns:
            Diccionario con info o None si no existe
        """
        try:
            file_path = Path(filepath)
            
            if not file_path.exists():
                return None
            
            stat = file_path.stat()
            
            return {
                'filename': file_path.name,
                'size_bytes': stat.st_size,
                'size_mb': stat.st_size / (1024 * 1024),
                'created_at': datetime.fromtimestamp(stat.st_ctime),
                'modified_at': datetime.fromtimestamp(stat.st_mtime),
                'extension': file_path.suffix,
                'exists': True
            }
            
        except Exception:
            return None
    
    def file_exists(self, filepath: str) -> bool:
        """
        Verifica si un archivo existe.
        
        Args:
            filepath: Ruta al archivo
            
        Returns:
            True si existe, False si no
        """
        return Path(filepath).exists()
    
    def get_upload_stats(self) -> dict:
        """
        Obtiene estadísticas de la carpeta de uploads.
        
        Returns:
            Diccionario con estadísticas
        """
        total_files = 0
        total_size = 0
        oldest_file = None
        newest_file = None
        
        try:
            for pdf_file in self.upload_folder.rglob('*.pdf'):
                total_files += 1
                total_size += pdf_file.stat().st_size
                
                file_mtime = datetime.fromtimestamp(pdf_file.stat().st_mtime)
                
                if oldest_file is None or file_mtime < oldest_file:
                    oldest_file = file_mtime
                
                if newest_file is None or file_mtime > newest_file:
                    newest_file = file_mtime
        
        except Exception:
            pass
        
        return {
            'total_files': total_files,
            'total_size_bytes': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'oldest_file_date': oldest_file,
            'newest_file_date': newest_file,
            'upload_folder': str(self.upload_folder)
        }
