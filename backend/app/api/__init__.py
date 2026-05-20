from fastapi import APIRouter

from app.api.routes.ingest import router as ingest_router
from app.api.routes.rag import router as rag_router
from app.api.routes.classification import router as classification_router

api_router = APIRouter()
api_router.include_router(ingest_router, prefix="/api")
api_router.include_router(rag_router, prefix="/api")
api_router.include_router(classification_router, prefix="/api")
