from fastapi import APIRouter
from firebase_admin import auth

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Monitoring API is up and running."}


@router.get("/test-firebase")
def test_firebase():
    try:
        page = auth.list_users(max_results=1)
        return {"message": "Firebase connection successful.", "user_count": page.users.__len__()}
    except Exception as e:
        return {"message": "Firebase connection failed.", "error": str(e)}
