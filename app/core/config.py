import os
import logging
import firebase_admin
from firebase_admin import credentials, firestore

# Obtener path de credenciales desde variable de entorno
firebase_cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'serviceAccountKey.json')

# Configurar logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Configurar Firebase

def initialize_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_cred_path)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized successfully.")
        else:
            logger.info("Firebase already initialized.")

        db = firestore.client()
        return db
    
    except Exception as e:
        logger.error(f"Error initializing Firebase: {e}")
        raise