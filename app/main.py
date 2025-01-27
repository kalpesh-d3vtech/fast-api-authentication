from fastapi import FastAPI
from app.routers import api_router
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(api_router)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI app!"}

@app.on_event("startup")
async def startup_event():
    logger.info("Application is starting...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application is shutting down...")
