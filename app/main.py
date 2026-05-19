from fastapi import FastAPI
from .db import engine
from .models import Base
from .routes import translate, history, health
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Translator API", version="1.0.0")

@app.on_event("startup")
async def startup():
    logger.info("Starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables checked/created.")

app.include_router(health.router)
app.include_router(translate.router)
app.include_router(history.router)