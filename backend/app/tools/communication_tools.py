"""
Communication action tools for agent.
"""

import uuid
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.agent import AgentDraftedReply
from app.tools.base import AgentTool
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SendAutoReplyTool(AgentTool):
    """Send or simulate auto-reply to customer."""

    name = "send_auto_reply"
    description = "Send auto-reply to customer email. Simulates email delivery."

    async def execute(
        self,
        email_id: str,
        draft_reply: str,
        tone: str = "professional",
        recipient: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Send auto-reply.

        Args:
            email_id: UUID of email being replied to
            draft_reply: Reply text to send
            tone: Tone of reply (professional, empathetic, etc)
            recipient: Email address to send reply to

        Returns:
            Send status
        """
        logger.info("Sending auto-reply: email_id=%s, tone=%s", email_id, tone)

        if not draft_reply or len(draft_reply.strip()) == 0:
            return self._format_result(False, None, "Draft reply cannot be empty")

        if not recipient:
            recipient = "customer@external.com"

        try:
            # Simulate email sending (production would integrate with SendGrid, AWS SES, etc)
            reply_id = str(uuid.uuid4())

            # Store drafted reply in DB
            drafted_reply = AgentDraftedReply(
                email_id=uuid.UUID(email_id),
                draft_content=draft_reply,
                tone=tone,
                policy_references=[],
                approved=True,
                sent=True,
                approved_by="agent_system",
            )

            async with AsyncSessionLocal() as session:
                session.add(drafted_reply)
                await session.commit()

            logger.info("Auto-reply sent: %s", reply_id)
            return self._format_result(
                True,
                {
                    "reply_id": reply_id,
                    "sent": True,
                    "timestamp": "2026-05-20T10:00:00Z",
                    "recipient": "customer@external.com",  # Would be actual recipient
                    "status": "delivered",
                },
            )

        except Exception as exc:
            logger.error("Auto-reply send failed: %s", exc)
            return self._format_result(False, None, str(exc))
