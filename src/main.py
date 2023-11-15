from fastapi import FastAPI
from .routes import global_router
from .config.settings import settings

app = FastAPI()
app.include_router(global_router)

@app.get("/")
def read_root():
    return {"Hello": settings.APP_NAME}