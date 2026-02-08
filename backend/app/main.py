from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from backend.app.db.database import create_db_and_tables
from backend.app.core.logging_config import logger # Import the configured logger
from backend.app.api.chat import router as chat_router # Import chat router
from fastapi import HTTPException # Import HTTPException for the handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan event handler to create database tables on startup.
    """
    logger.info("Application startup begins.")
    print("Creating database tables...") # Keep print for immediate visibility
    create_db_and_tables()
    yield
    logger.info("Application shutdown.")

app = FastAPI(
    title="AI Todo Chatbot Backend",
    version="0.1.0",
    lifespan=lifespan,
)

# Global exception handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException occurred: {exc.detail} for URL: {request.url}", exc_info=True)
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

app.include_router(chat_router) # Include chat router

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the AI Todo Chatbot Backend!"}

# Routers will be included here as they are developed (e.g., chat router)
