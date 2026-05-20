"""
Draft reply generation tools.
"""

from typing import Any, Optional

from app.tools.base import AgentTool
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Reply templates by tone and situation
REPLY_TEMPLATES = {
    "empathetic_issue": "We sincerely apologize for the issue you're experiencing. Our team is treating this as a priority and will investigate immediately. You can expect an update within 24 hours.",
    "empathetic_wait": "Thank you for your patience. We understand how frustrating this must be. Our team is working on a resolution and will keep you updated every 24 hours.",
    "professional_faq": "Thank you for reaching out. Based on our {policy_name} policy, here's the information: {details}. Please let us know if you need clarification.",
    "professional_billing": "Thank you for your inquiry about billing. Our {billing_tier} plan includes {features}. For your specific situation, our billing team will reach out within 24 hours.",
    "holding_legal": "Thank you for your message. We take all concerns seriously and are reviewing your inquiry carefully. We will provide a detailed response shortly.",
    "escalation_acknowledge": "Thank you for bringing this to our attention. Due to the nature of your inquiry, we're escalating this to our specialist team who will contact you within 4 hours.",
}


class DraftReplyTool(AgentTool):
    """Generate a draft reply to a customer email."""

    name = "draft_reply"
    description = "Generate a professional, empathetic draft reply with optional policy references."

    async def execute(
        self,
        context: str,
        tone: str = "professional",
        policy_refs: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Generate draft reply.

        Args:
            context: Brief context of what needs to be addressed
            tone: Reply tone - professional, empathetic, technical, holding
            policy_refs: List of policy document references to cite

        Returns:
            Drafted reply text
        """
        logger.info("Drafting reply: tone=%s, context_len=%d", tone, len(context))

        if not context or len(context.strip()) == 0:
            return self._format_result(False, None, "Context cannot be empty")

        tone = tone.lower()
        if tone not in ["professional", "empathetic", "technical", "holding"]:
            tone = "professional"

        try:
            # Simple template-based generation (production would use LLM)
            template_key = f"{tone}_faq"

            if "issue" in context.lower() or "problem" in context.lower():
                if tone == "empathetic":
                    draft = REPLY_TEMPLATES["empathetic_issue"]
                else:
                    draft = "Thank you for reporting this issue. Our team will investigate and follow up shortly."

            elif "billing" in context.lower() or "invoice" in context.lower():
                draft = REPLY_TEMPLATES.get(
                    "professional_billing",
                    "Thank you for your billing inquiry. Our support team will assist you shortly.",
                )

            elif "legal" in context.lower() or "lawsuit" in context.lower():
                draft = REPLY_TEMPLATES["holding_legal"]

            else:
                draft = REPLY_TEMPLATES.get(template_key, "Thank you for your message. We will review and respond shortly.")

            # Add policy references if provided
            policy_section = ""
            if policy_refs and len(policy_refs) > 0:
                policy_section = f"\n\nReference: See our {', '.join(policy_refs)} for more details."
                draft += policy_section

            draft += "\n\nBest regards,\nCustomer Support Team"

            logger.info("Draft reply generated (%d chars)", len(draft))
            return self._format_result(True, {"draft": draft, "tone": tone, "policy_references": policy_refs or []})

        except Exception as exc:
            logger.error("Draft reply generation failed: %s", exc)
            return self._format_result(False, None, str(exc))
