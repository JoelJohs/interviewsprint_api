import firebase_admin
from firebase_admin import credentials

CRED_PATH = "serviceAccountKey.json"


def initialize_firebase():
    try:
        cred = credentials.Certificate(CRED_PATH)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully.")
    except ValueError as ve:
        print(f"Firebase already initialized: {ve}")
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
