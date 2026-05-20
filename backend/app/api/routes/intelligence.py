from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.intelligence.intelligence_service import WebIntelligenceService
from app.schemas.email import StandardResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/intelligence", tags=["intelligence"])


@router.get("/reputation", response_model=StandardResponse)
async def get_reputation(company: str = Query(..., min_length=1), session: AsyncSession = Depends(get_db_session)) -> StandardResponse:
    """Return cached or freshly scraped reputation intelligence for a company."""
    logger.info("Reputation intelligence requested for company=%s", company)

    try:
        service = WebIntelligenceService()
        reputation = await service.get_reputation(company, session=session)
        return StandardResponse(
            success=True,
            message="Reputation intelligence retrieved.",
            data={
                "company": reputation.get("company"),
                "rating": reputation.get("rating"),
                "review_count": reputation.get("review_count"),
                "themes": reputation.get("themes"),
                "source": reputation.get("source"),
                "cached": reputation.get("cached", False),
                "source_url": reputation.get("source_url"),
            },
        )
    except Exception as exc:
        logger.error("Reputation intelligence endpoint failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Reputation intelligence retrieval failed.")
