from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import get_db_session
from app.schemas.email import EmailIngestPayload, StandardResponse
from app.services.email_service import ingest_email
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="", tags=["ingest"])


@router.post("/ingest", response_model=StandardResponse)
async def ingest_email_endpoint(
    payload: EmailIngestPayload,
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse:
    try:
        result = await ingest_email(payload, session)
    except IntegrityError as exc:
        logger.error("Database integrity error during email ingest: %s", exc)
        raise HTTPException(status_code=400, detail="Duplicate or invalid ingest payload.")
    return StandardResponse(success=True, message="Email ingestion accepted.", data=result)
