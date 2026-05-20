from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Email
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ThreadContextService:
    """
    Fetches and formats thread history for LLM injection.
    Retrieves all emails in a thread, ordered chronologically.
    """

    @staticmethod
    async def get_thread_context(thread_id: str, session: AsyncSession, max_emails: int = 10) -> str:
        """
        Retrieve thread history and format as context string.

        Args:
            thread_id: UUID of the thread
            session: Async DB session
            max_emails: Maximum number of emails to include (most recent)

        Returns:
            Formatted thread context string for LLM injection
        """
        logger.info("Fetching thread context for thread_id=%s", thread_id)

        query = (
            select(Email)
            .where(Email.thread_id == thread_id)
            .order_by(Email.received_at.asc())
        )

        result = await session.execute(query)
        emails = result.scalars().all()

        if not emails:
            return "No thread history available."

        # Keep only the most recent max_emails
        if len(emails) > max_emails:
            logger.info("Thread has %d emails, limiting to %d most recent", len(emails), max_emails)
            emails = emails[-max_emails:]

        context_lines = [f"Thread ID: {thread_id}"]
        context_lines.append(f"Total emails in thread: {len(emails)}")
        context_lines.append("---\nThread History (oldest to newest):\n")

        for idx, email in enumerate(emails, 1):
            timestamp = email.received_at.strftime("%Y-%m-%d %H:%M:%S") if email.received_at else "unknown"
            context_lines.append(f"\n[{idx}] {timestamp}")
            context_lines.append(f"From: {email.sender_contact.email if email.sender_contact else 'unknown'}")
            context_lines.append(f"Subject: {email.subject or '(no subject)'}")
            context_lines.append(f"Priority: {email.priority} | Spam: {email.is_spam} | Sentiment: {email.sentiment}")

            body_preview = email.body[:300] + "..." if email.body and len(email.body) > 300 else email.body or "(no body)"
            context_lines.append(f"Body: {body_preview}")

        context_lines.append("\n---")
        return "\n".join(context_lines)

    @staticmethod
    async def summarize_thread(thread_id: str, session: AsyncSession) -> str:
        """
        Create a brief summary of thread for context when thread is very long.
        Returns key facts rather than full history.
        """
        logger.info("Summarizing thread: %s", thread_id)

        query = select(Email).where(Email.thread_id == thread_id).order_by(Email.received_at.asc())
        result = await session.execute(query)
        emails = result.scalars().all()

        if not emails:
            return "Thread has no emails."

        summary_lines = []
        summary_lines.append(f"Thread Summary ({len(emails)} total emails)")
        summary_lines.append("-" * 40)

        # Key facts
        first_email = emails[0]
        last_email = emails[-1]
        summary_lines.append(f"Started: {first_email.received_at.strftime('%Y-%m-%d %H:%M:%S')}")
        summary_lines.append(f"Last activity: {last_email.received_at.strftime('%Y-%m-%d %H:%M:%S')}")
        summary_lines.append(f"Participants: {len(set(e.sender_contact.email for e in emails if e.sender_contact))}")

        # Priority escalation
        priorities = [e.priority for e in emails]
        summary_lines.append(f"Priority progression: {' → '.join(priorities)}")

        # Sentiment progression
        sentiments = [e.sentiment for e in emails]
        summary_lines.append(f"Sentiment: {' → '.join(sentiments)}")

        # Any escalations
        escalations = [e for e in emails if e.urgency_tags or e.security_flags]
        if escalations:
            summary_lines.append(f"Escalations: {len(escalations)} emails with urgency or security flags")

        summary_lines.append("\n" + "=" * 40)
        summary_lines.append("Most recent email (CURRENT):\n")

        current = emails[-1]
        summary_lines.append(f"From: {current.sender_contact.email if current.sender_contact else 'unknown'}")
        summary_lines.append(f"Subject: {current.subject or '(no subject)'}")
        summary_lines.append(f"\n{current.body or '(no body)'}")

        return "\n".join(summary_lines)
