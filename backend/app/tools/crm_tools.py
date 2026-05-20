"""
CRM and data retrieval tools for agent.
"""

from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Contact, Email
from app.db.session import AsyncSessionLocal
from app.tools.base import AgentTool
from app.utils.logger import get_logger

logger = get_logger(__name__)


class GetThreadHistoryTool(AgentTool):
    """Fetch complete thread history for an email."""

    name = "get_thread_history"
    description = "Retrieve full email thread history ordered chronologically. Shows all prior communications."

    async def execute(self, thread_id: str, max_emails: int = 10, **kwargs: Any) -> dict[str, Any]:
        """
        Fetch thread history.

        Args:
            thread_id: UUID of thread
            max_emails: Max emails to return (default 10)

        Returns:
            Chronological list of emails in thread
        """
        logger.info("Fetching thread history: thread_id=%s", thread_id)

        try:
            async with AsyncSessionLocal() as session:
                query = select(Email).where(Email.thread_id == thread_id).order_by(Email.received_at.asc())
                result = await session.execute(query)
                emails = result.scalars().all()

                if not emails:
                    return self._format_result(True, {"emails": [], "count": 0})

                # Limit results
                emails = emails[-max_emails:]

                thread_data = []
                for email in emails:
                    sender_email = email.sender_contact.email if email.sender_contact else "unknown"
                    thread_data.append(
                        {
                            "email_id": str(email.id),
                            "from": sender_email,
                            "to": email.recipient,
                            "subject": email.subject or "(no subject)",
                            "body_preview": (email.body[:200] + "...") if email.body and len(email.body) > 200 else email.body or "(empty)",
                            "timestamp": email.received_at.isoformat() if email.received_at else "unknown",
                            "priority": email.priority,
                            "sentiment": email.sentiment,
                        }
                    )

                logger.info("Found %d emails in thread", len(thread_data))
                return self._format_result(True, {"emails": thread_data, "count": len(thread_data)})

        except Exception as exc:
            logger.error("Failed to fetch thread history: %s", exc)
            return self._format_result(False, None, str(exc))


class GetContactProfileTool(AgentTool):
    """Fetch CRM contact profile with account metadata."""

    name = "get_contact_profile"
    description = "Retrieve contact profile including VIP status, account value, and churn risk indicators."

    async def execute(self, email: str, **kwargs: Any) -> dict[str, Any]:
        """
        Fetch contact profile.

        Args:
            email: Email address of contact

        Returns:
            Contact profile with metadata
        """
        logger.info("Fetching contact profile: %s", email)

        try:
            async with AsyncSessionLocal() as session:
                query = select(Contact).where(Contact.email == email)
                result = await session.execute(query)
                contact = result.scalars().first()

                if not contact:
                    return self._format_result(True, {"found": False, "email": email})

                # Calculate simple heuristics (would be richer in production)
                email_count = len(contact.emails) if contact.emails else 0
                vip_status = "VIP" if email_count > 10 else "Standard"
                churn_risk = "High" if email_count < 2 else "Low"

                profile = {
                    "found": True,
                    "email": contact.email,
                    "name": contact.name,
                    "contact_id": str(contact.id),
                    "email_count": email_count,
                    "vip_status": vip_status,
                    "churn_risk": churn_risk,
                    "first_contact": contact.created_at.isoformat() if contact.created_at else "unknown",
                    "last_activity": contact.updated_at.isoformat() if contact.updated_at else "unknown",
                }

                logger.info("Contact profile retrieved: vip=%s, churn_risk=%s", vip_status, churn_risk)
                return self._format_result(True, profile)

        except Exception as exc:
            logger.error("Failed to fetch contact profile: %s", exc)
            return self._format_result(False, None, str(exc))


class CheckAccountStatusTool(AgentTool):
    """Check customer account status (billing, subscription)."""

    name = "check_account_status"
    description = "Check billing tier, subscription status, and any overdue invoices."

    async def execute(self, email: str, **kwargs: Any) -> dict[str, Any]:
        """
        Check account status.

        Args:
            email: Customer email

        Returns:
            Account status information
        """
        logger.info("Checking account status: %s", email)

        try:
            # In production, this would query billing/subscription systems
            # For now, return simulated data based on heuristics

            account_status = {
                "email": email,
                "billing_tier": "Professional",  # Simulated
                "subscription_active": True,
                "monthly_cost": 499,
                "seats_used": 12,
                "seats_allocated": 25,
                "overdue_invoices": 0,
                "last_payment": "2026-05-01",
                "renewal_date": "2026-06-01",
                "account_age_months": 18,
                "payment_method": "credit_card",
            }

            logger.info("Account status retrieved: tier=%s, active=%s", account_status["billing_tier"], account_status["subscription_active"])
            return self._format_result(True, account_status)

        except Exception as exc:
            logger.error("Failed to check account status: %s", exc)
            return self._format_result(False, None, str(exc))
