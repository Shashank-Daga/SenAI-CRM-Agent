import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AuditLog, Contact, Email, Thread
from app.schemas.email import EmailIngestPayload
from app.services.heuristics import analyze_email, merge_priority
from app.utils.logger import get_logger

logger = get_logger(__name__)


def _normalize_subject(subject: Optional[str], thread_subject: Optional[str]) -> str:
    if thread_subject:
        return thread_subject.strip()
    if subject:
        return subject.strip()
    return "No Subject"


def _normalize_body(body: Optional[str]) -> Optional[str]:
    if body is None:
        return None
    stripped = body.strip()
    if not stripped:
        return None
    if len(stripped) > 10000:
        return stripped[:10000]
    return stripped


def _make_metadata(body: Optional[str], original_body: Optional[str]) -> Dict[str, Any]:
    return {
        "truncated": bool(original_body and len(original_body.strip()) > 10000),
        "body_length": len(body or ""),
    }


async def get_or_create_contact(session: AsyncSession, sender: str) -> Contact:
    query = select(Contact).where(Contact.email == sender)
    result = await session.execute(query)
    contact = result.scalars().first()
    if contact:
        return contact

    contact = Contact(email=sender)
    session.add(contact)
    await session.flush()
    return contact


async def get_or_create_thread(session: AsyncSession, payload: EmailIngestPayload) -> Thread:
    if payload.thread_id:
        query = select(Thread).where(Thread.id == payload.thread_id)
        result = await session.execute(query)
        thread = result.scalars().first()
        if thread:
            return thread

    subject = _normalize_subject(payload.subject, payload.thread_subject)
    query = select(Thread).where(Thread.subject == subject)
    result = await session.execute(query)
    thread = result.scalars().first()
    if thread:
        return thread

    thread = Thread(subject=subject, last_received_at=payload.received_at)
    session.add(thread)
    await session.flush()
    return thread


async def record_audit(session: AsyncSession, event_type: str, entity_type: str, entity_id: str, payload: Dict[str, Any]) -> None:
    audit = AuditLog(
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        payload=payload,
    )
    session.add(audit)


async def ingest_email(payload: EmailIngestPayload, session: AsyncSession) -> Dict[str, Any]:
    job_id = str(uuid.uuid4())
    normalized_body = _normalize_body(payload.body)
    truncated_metadata = _make_metadata(normalized_body, payload.body)

    duplicate_query = select(Email).where(Email.message_id == payload.message_id)
    duplicate_result = await session.execute(duplicate_query)
    existing_email = duplicate_result.scalars().first()
    if existing_email:
        return {
            "job_id": job_id,
            "status": "duplicate",
            "thread_id": str(existing_email.thread_id),
            "message_id": existing_email.message_id,
            "priority": existing_email.priority,
            "is_duplicate": True,
            "details": {"reason": "message_id already exists"},
        }

    response_data = analyze_email(payload.subject, normalized_body, payload.sender)

    contact = await get_or_create_contact(session, payload.sender)
    thread = await get_or_create_thread(session, payload)

    if thread.last_received_at is None or payload.received_at > thread.last_received_at:
        thread.last_received_at = payload.received_at
    elif payload.received_at < thread.last_received_at:
        logger.info("Out-of-order email timestamp for thread %s: received_at=%s last_received_at=%s", thread.id, payload.received_at, thread.last_received_at)

    thread.priority = merge_priority(thread.priority, response_data["priority"])
    thread.updated_at = datetime.utcnow()

    email = Email(
        thread_id=thread.id,
        sender_id=contact.id,
        recipient=payload.recipient,
        message_id=payload.message_id,
        subject=payload.subject,
        body=normalized_body,
        received_at=payload.received_at,
        priority=response_data["priority"],
        is_spam=response_data["is_spam"],
        sentiment=response_data["sentiment"],
        urgency_tags=response_data["urgency_tags"],
        security_flags=response_data["security_flags"],
        internal_email=response_data["internal_email"],
        metadata=truncated_metadata,
    )
    session.add(email)

    await record_audit(
        session,
        event_type="email_ingested",
        entity_type="email",
        entity_id=str(email.id),
        payload={
            "message_id": payload.message_id,
            "thread_id": str(thread.id),
            "priority": response_data["priority"],
        },
    )

    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        logger.error("Failed to ingest email %s: %s", payload.message_id, exc)
        raise

    return {
        "job_id": job_id,
        "status": "ingested",
        "thread_id": str(thread.id),
        "message_id": payload.message_id,
        "priority": response_data["priority"],
        "is_duplicate": False,
        "details": {
            "thread_subject": thread.subject,
            "is_spam": response_data["is_spam"],
            "sentiment": response_data["sentiment"],
            "urgency_tags": response_data["urgency_tags"],
            "security_flags": response_data["security_flags"],
            "internal_email": response_data["internal_email"],
        },
    }
