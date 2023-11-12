from fastapi import FastAPI
from .config import settings

app = FastAPI( )

@app.get("/")
def read_root():
    return {"Hello": settings.APP_NAME}