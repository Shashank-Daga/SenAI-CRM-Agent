from fastapi import APIRouter, Query

from app.rag.retrieval_service import RAGRetrievalService
from app.schemas.email import StandardResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/rag", tags=["rag"])


@router.get("/search", response_model=StandardResponse)
async def search_knowledge_base(
    q: str = Query(..., min_length=1, max_length=500, description="Search query"),
    limit: int = Query(3, ge=1, le=10, description="Number of results to return"),
) -> StandardResponse:
    """
    Search the knowledge base for relevant documents.

    Returns top-k chunks with similarity scores and source metadata.
    """
    logger.info("RAG search endpoint: q=%s, limit=%d", q, limit)

    try:
        results = RAGRetrievalService.search(query=q, top_k=limit)

        return StandardResponse(
            success=True,
            message="Knowledge base search completed.",
            data={
                "query": q,
                "result_count": len(results),
                "results": results,
            },
        )
    except Exception as exc:
        logger.error("RAG search failed: %s", exc, exc_info=True)
        return StandardResponse(
            success=False,
            message="Knowledge base search failed.",
            error_code="rag_search_failed",
            details={"error": str(exc)},
        )
