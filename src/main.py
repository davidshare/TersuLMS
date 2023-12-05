from fastapi import FastAPI
from .models import *
from .routes import global_router
from .config.settings import settings
from .logger import logger
from .middleware import LogMiddleware

app = FastAPI()
app.add_middleware(LogMiddleware)
app.include_router(global_router)

@app.get("/")
def read_root():
    logger.info("Hello World")
    return {"Hello": settings.APP_NAME}

#TODO: use chatgpt to check for more ideas to improve the models and how to better design them
#TODO: update relationships between models to be more efficient
#TODO: update models to return complete data for specific endpoints