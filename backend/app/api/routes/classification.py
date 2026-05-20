from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.llm.classification_service import LLMClassificationService
from app.prompts.classification_prompt import build_classification_prompt, SYSTEM_PROMPT
from app.rag.retrieval_service import RAGRetrievalService
from app.schemas.classification import EmailClassification
from app.schemas.email import StandardResponse
from app.services.thread_service import ThreadContextService
from app.utils.logger import get_logger
from sqlalchemy import select
from app.models import Email

logger = get_logger(__name__)
router = APIRouter(prefix="/classify", tags=["classification"])


@router.post("/email/{email_id}", response_model=StandardResponse)
async def classify_email(
    email_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> StandardResponse:
    """
    Classify a single email using LLM with thread context and RAG knowledge injection.

    Classification workflow:
    1. Fetch email from database
    2. Get full thread context (email history)
    3. Retrieve relevant knowledge base chunks via RAG
    4. Build full prompt with all context
    5. Call LLM for classification
    6. Validate output schema
    7. Apply escalation business rules
    """
    logger.info("Classifying email: %s", email_id)

    # Step 1: Fetch email
    query = select(Email).where(Email.id == email_id)
    result = await session.execute(query)
    email = result.scalars().first()

    if not email:
        logger.warning("Email not found: %s", email_id)
        raise HTTPException(status_code=404, detail="Email not found")

    try:
        # Step 2: Get thread context
        thread_context = await ThreadContextService.get_thread_context(str(email.thread_id), session, max_emails=10)

        # Step 3: Retrieve RAG knowledge
        # Query for relevant docs using email subject + body
        search_query = f"{email.subject or ''} {email.body or ''}"[:500]
        rag_results = RAGRetrievalService.search(query=search_query, top_k=3)
        rag_context = RAGRetrievalService.get_context_string(search_query, top_k=3)

        # Step 4: Build full prompt
        prompt = build_classification_prompt(
            thread_context=thread_context,
            sender=email.sender_contact.email if email.sender_contact else "unknown",
            recipient=email.recipient,
            subject=email.subject,
            body=email.body,
            rag_context=rag_context,
        )

        # Step 5: Call LLM
        llm_service = LLMClassificationService()
        classification = await llm_service.classify_email(prompt)

        # Step 6: Apply escalation business rules
        should_escalate = classification.should_escalate()

        # Step 7: Build response
        response_data = {
            "email_id": str(email.id),
            "thread_id": str(email.thread_id),
            "classification": classification.model_dump(),
            "requires_escalation": should_escalate,
            "rag_sources": [
                {
                    "source_doc": r["source_doc"],
                    "section_title": r["section_title"],
                    "score": r["similarity_score"],
                }
                for r in rag_results
            ],
        }

        logger.info("✓ Classification complete for email %s (category=%s, escalate=%s, confidence=%.2f)", email_id, classification.category, should_escalate, classification.confidence)

        return StandardResponse(
            success=True,
            message="Email classification completed.",
            data=response_data,
        )

    except ValueError as exc:
        logger.error("Classification parse error for email %s: %s", email_id, exc)
        return StandardResponse(
            success=False,
            message="Failed to parse LLM classification response.",
            error_code="classification_parse_error",
            details={"error": str(exc)},
        )

    except Exception as exc:
        logger.error("Classification error for email %s: %s", email_id, exc, exc_info=True)
        return StandardResponse(
            success=False,
            message="Email classification failed.",
            error_code="classification_error",
            details={"error": str(exc)},
        )
