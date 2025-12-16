"""
Script de prueba para verificar la integración GROBID + Crossref
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.pdf_service import PDFService

def test_grobid_availability():
    """Verifica si GROBID está disponible"""
    print("=" * 60)
    print("TEST 1: Verificando disponibilidad de GROBID")
    print("=" * 60)
    
    service = PDFService()
    is_available = service._is_grobid_available()
    
    if is_available:
        print("✅ GROBID está disponible en http://localhost:8070")
    else:
        print("❌ GROBID NO está disponible")
        print("\n💡 Para iniciar GROBID, ejecuta:")
        print("   docker run --rm --init -p 8070:8070 lfoppiano/grobid:0.8.2")
    
    print()
    return is_available

def test_extraction_with_sample():
    """Prueba la extracción con un PDF de ejemplo"""
    print("=" * 60)
    print("TEST 2: Extracción de metadatos")
    print("=" * 60)
    
    # Buscar un PDF de ejemplo en uploads
    uploads_dir = os.path.join(os.path.dirname(__file__), '..', 'pdf/art_rev_indexada')
    
    if not os.path.exists(uploads_dir):
        print("❌ No existe el directorio 'uploads'")
        return
    
    pdf_files = [f for f in os.listdir(uploads_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No hay PDFs en el directorio 'uploads'")
        print("\n💡 Coloca un PDF académico en la carpeta 'uploads' para probar")
        return
    
    # Tomar el primer PDF
    pdf_path = os.path.join(uploads_dir, pdf_files[0])
    print(f"\n📄 Probando con: {pdf_files[0]}")
    print()
    
    service = PDFService()
    metadata = service.extract_metadata(pdf_path)
    
    print(f"📊 Método de extracción: {metadata.get('extraction_method', 'unknown')}")
    print(f"🎯 Confianza: {metadata.get('confidence', 0):.2f}")
    print()
    print("📋 Metadatos extraídos:")
    print(f"  • Título: {metadata.get('titulo', 'N/A')[:80]}")
    print(f"  • Autores: {len(metadata.get('autores', []))} detectados")
    if metadata.get('autores'):
        for i, autor in enumerate(metadata.get('autores', [])[:3], 1):
            print(f"    {i}. {autor.get('nombre', '')} {autor.get('apellidos', '')}")
    print(f"  • Año: {metadata.get('anio_publicacion', 'N/A')}")
    print(f"  • DOI: {metadata.get('doi', 'N/A')}")
    print(f"  • ISSN: {metadata.get('issn', 'N/A')}")
    print(f"  • Abstract: {'Sí' if metadata.get('resumen') else 'No'}")
    
    print()

def test_comparison():
    """Compara extracción con y sin GROBID"""
    print("=" * 60)
    print("TEST 3: Comparación GROBID vs Heurísticas")
    print("=" * 60)
    
    uploads_dir = os.path.join(os.path.dirname(__file__), '..', 'pdf/art_rev_indexada')
    
    if not os.path.exists(uploads_dir):
        print("❌ No existe el directorio 'pdf/art_rev_indexada'")
        return
    
    pdf_files = [f for f in os.listdir(uploads_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No hay PDFs para comparar")
        return
    
    pdf_path = os.path.join(uploads_dir, pdf_files[0])
    print(f"\n📄 Archivo: {pdf_files[0]}\n")
    
    # Con GROBID
    service_with_grobid = PDFService(enable_grobid=True)
    metadata_grobid = service_with_grobid.extract_metadata(pdf_path)
    
    # Sin GROBID
    service_without_grobid = PDFService(enable_grobid=False)
    metadata_heuristic = service_without_grobid.extract_metadata(pdf_path)
    
    print("🤖 CON GROBID:")
    print(f"   Método: {metadata_grobid.get('extraction_method', 'unknown')}")
    print(f"   Confianza: {metadata_grobid.get('confidence', 0):.2f}")
    print(f"   Título: {metadata_grobid.get('titulo', 'N/A')[:60]}...")
    print(f"   Autores: {len(metadata_grobid.get('autores', []))}")
    print(f"   DOI: {metadata_grobid.get('doi', 'N/A')}")
    print()
    
    print("🔍 SIN GROBID (Heurísticas):")
    print(f"   Método: {metadata_heuristic.get('extraction_method', 'unknown')}")
    print(f"   Confianza: {metadata_heuristic.get('confidence', 0):.2f}")
    print(f"   Título: {metadata_heuristic.get('titulo', 'N/A')[:60]}...")
    print(f"   Autores: {len(metadata_heuristic.get('autores', []))}")
    print(f"   DOI: {metadata_heuristic.get('doi', 'N/A')}")
    print()
    
    # Análisis
    print("📊 ANÁLISIS:")
    if metadata_grobid.get('confidence', 0) > metadata_heuristic.get('confidence', 0):
        print("   ✅ GROBID tuvo mayor confianza")
    else:
        print("   ⚠️  Heurísticas tuvieron igual o mayor confianza")
    
    print()

def main():
    """Ejecuta todos los tests"""
    print("\n🧪 PRUEBAS DE INTEGRACIÓN GROBID + CROSSREF\n")
    
    # Test 1: Disponibilidad
    grobid_available = test_grobid_availability()
    
    # Test 2: Extracción básica
    test_extraction_with_sample()
    
    # Test 3: Comparación (solo si GROBID está disponible)
    if grobid_available:
        test_comparison()
    else:
        print("⏭️  Test 3 omitido (GROBID no disponible)")
    
    print("\n" + "=" * 60)
    print("✅ PRUEBAS COMPLETADAS")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
