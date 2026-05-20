"""
Escalation and action tools for agent.
"""

import uuid
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.agent import AgentEscalation
from app.tools.base import AgentTool
from app.utils.logger import get_logger

logger = get_logger(__name__)


class EscalateToHumanTool(AgentTool):
    """Create escalation for human review."""

    name = "escalate_to_human"
    description = "Create an escalation ticket for human agent review with priority level."

    async def execute(
        self,
        email_id: str,
        thread_id: str,
        reason: str,
        priority: str = "High",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Create human escalation.

        Args:
            email_id: UUID of email
            thread_id: UUID of thread
            reason: Escalation reason
            priority: Priority level (Critical, High, Medium, Low)

        Returns:
            Escalation record
        """
        logger.info("Escalating to human: email_id=%s, priority=%s", email_id, priority)

        if priority not in ["Critical", "High", "Medium", "Low"]:
            priority = "High"

        try:
            escalation = AgentEscalation(
                email_id=uuid.UUID(email_id),
                thread_id=uuid.UUID(thread_id),
                escalation_type="human_review",
                priority=priority,
                reason=reason,
                metadata={"escalation_reason": reason, "priority": priority},
            )

            async with AsyncSessionLocal() as session:
                session.add(escalation)
                await session.commit()

            logger.info("Escalation created: %s", escalation.id)
            return self._format_result(
                True,
                {
                    "escalation_id": str(escalation.id),
                    "priority": priority,
                    "reason": reason,
                    "status": "pending_human_review",
                },
            )

        except Exception as exc:
            logger.error("Escalation creation failed: %s", exc)
            return self._format_result(False, None, str(exc))


class FlagForLegalTool(AgentTool):
    """Flag email for legal team review."""

    name = "flag_for_legal"
    description = "Create legal escalation for threatening, lawsuit, or compliance-related emails."

    async def execute(
        self,
        email_id: str,
        thread_id: str,
        issue_type: str = "legal_threat",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Create legal escalation.

        Args:
            email_id: UUID of email
            thread_id: UUID of thread
            issue_type: Type of legal issue (legal_threat, breach, contract_dispute, etc)

        Returns:
            Legal escalation record
        """
        logger.info("Flagging for legal: email_id=%s, issue_type=%s", email_id, issue_type)

        try:
            escalation = AgentEscalation(
                email_id=uuid.UUID(email_id),
                thread_id=uuid.UUID(thread_id),
                escalation_type="legal",
                priority="Critical",
                reason=f"Legal escalation: {issue_type}. Requires legal team review before any communication.",
                metadata={
                    "issue_type": issue_type,
                    "requires_no_reply": True,
                    "notify_general_counsel": True,
                },
            )

            async with AsyncSessionLocal() as session:
                session.add(escalation)
                await session.commit()

            logger.info("Legal escalation created: %s", escalation.id)
            return self._format_result(
                True,
                {
                    "escalation_id": str(escalation.id),
                    "type": "legal",
                    "priority": "Critical",
                    "issue_type": issue_type,
                    "requires_no_auto_reply": True,
                },
            )

        except Exception as exc:
            logger.error("Legal escalation failed: %s", exc)
            return self._format_result(False, None, str(exc))


class CreateInternalTicketTool(AgentTool):
    """Create internal support or engineering ticket."""

    name = "create_internal_ticket"
    description = "Create internal ticket for support team or engineering. Simulates ticket creation."

    async def execute(
        self,
        title: str,
        body: str,
        assignee: str = "support_team",
        ticket_type: str = "support",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Create internal ticket.

        Args:
            title: Ticket title
            body: Ticket description
            assignee: Team to assign to (support_team, engineering, billing)
            ticket_type: Type of ticket (support, bug, feature_request)

        Returns:
            Ticket metadata
        """
        logger.info("Creating internal ticket: type=%s, assignee=%s", ticket_type, assignee)

        if not title or not body:
            return self._format_result(False, None, "Title and body required")

        try:
            # Simulate ticket creation (production would integrate with Jira, Linear, etc)
            ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"

            ticket = {
                "ticket_id": ticket_id,
                "title": title,
                "body": body[:500],  # Truncate
                "type": ticket_type,
                "assignee": assignee,
                "status": "open",
                "created_at": "2026-05-20T10:00:00Z",
                "priority": "normal",
            }

            logger.info("Internal ticket created: %s", ticket_id)
            return self._format_result(True, ticket)

        except Exception as exc:
            logger.error("Ticket creation failed: %s", exc)
            return self._format_result(False, None, str(exc))
