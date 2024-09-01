from fastapi.routing import APIRouter

router = APIRouter()

@router.get('/')
def root():
    return {
        "message": "hello"
    }

