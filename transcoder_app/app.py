from fastapi import FastAPI
from routers import videoProcessor

app = FastAPI()

@app.get('/')
def root():
    return {
        "message": "hello"
    }

app.include_router(
    videoProcessor.router,
    prefix='/video-processor',
    tags=['video-processor']
)
