import json
import sys
import os
from datetime import datetime, UTC

# Añadir parent directory al path para importar config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import initialize_firebase
from datetime import datetime, timezone

# Obtenemos la ruta raiz
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Función para cargar el archivo JSON en "app/seeds/topics.json"
def load_json(filepath):
    """
    Cargar los datos desde un archivo JSON
    """
    full_path = os.path.join(PROJECT_ROOT, filepath)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def seed_categories(db, categories_data):
    """
    Sembrar categorias en Firestore
    """
    categories_ref = db.collection('categories')

    count = 0
    for category in categories_data:
        # Se usa el "id" en el JSON como document ID en Firestore
        doc_ref = categories_ref.document(category['id'])

        # Los datos a insertar sin usar el id porque ya esta en el document ID
        category_data = {
            'name': category['name'],
            'icon': category['icon'],
            'created_at': datetime.now(UTC)
        }

        doc_ref.set(category_data)
        count += 1
        print(f"✔️ Categoria sembrada: {category['name']} (ID: {category['id']})")


    print(f"\n ✅ conteo de semilla: {count} - Categorias sembradas de manera satisfactoria.")

def seed_topics(db, topics_data):
    """
    Sembrar topics en Firestore
    """
    topic_ref = db.collection('topics')

    count = 0
    for topic in topics_data:
        # Se usa el "id" en el JSON como document ID en Firestore
        doc_ref = topic_ref.document(topic['id'])

        # Los datos a insertar sin usar el id porque ya esta en el document ID
        topic_data = {
            'title': topic['title'],
            'category_id': topic['category_id'],
            'details': topic['details'],
            'created_at': datetime.now(UTC)
        }

        doc_ref.set(topic_data)
        count += 1
        print(f"✔️ Topic sembrado: {topic['title']} (ID: {topic['id']})")

    print(f"\n ✅ conteo de semilla: {count} - Topics sembrados de manera satisfactoria.")
        
# Función principal para ejecutar el seed
def main():
    print("🌱 Iniciando proceso de siembra...\n")

    try:
        # Inicializar Firebase
        db = initialize_firebase()

        # Cargar datos desde JSON
        print("Cargando data desde JSON...")
        data = load_json('app/seeds/topics.json')

        # Verificar la estructura del JSON
        if 'categories' not in data or 'topics' not in data:
            raise ValueError("❌ Error: El archivo JSON debe contener 'categories' y 'topics'.")
        
        # Seed de categorias
        print("\nSembrando categorias...")
        seed_categories(db, data['categories'])

        # Seed de topics
        print("\nSembrando topics...")
        seed_topics(db, data['topics'])

        print("\n🌱 Proceso de siembra completado exitosamente.")
        return 0

    except FileNotFoundError as fnf_error:
        print(f"❌ Error: Archivo no encontrado - {fnf_error}")
        return 1
    except ValueError as ve:
        print(f"❌ Error: {ve}")
        return 1
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
