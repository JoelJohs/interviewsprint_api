import sys
import os

# Añadir parent directory al path para importar app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import initialize_firebase

def test_firestore_connection():
    """
    Test de conexion a Firestore
    """
    try:
        # Inicializar Firebase
        db = initialize_firebase()

        # Intentar obtener una coleccion de prueba
        collections = db.collections()
        collection_names = [col.id for col in collections]

        print("✅ Conexion a Firestore exitosa.")
        print(f"📚 Colecciones disponibles: {collection_names if collection_names else '(ninguna aún)'}")
        
        # Si hay colecciones, contar documentos
        for col_name in collection_names:
            count = len(list(db.collection(col_name).stream()))
            print(f"   - {col_name}: {count} documentos")

    except Exception as e:
        print(f"❌ Error al conectar a Firestore: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_firestore_connection()