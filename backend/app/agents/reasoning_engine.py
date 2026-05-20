"""
Agent reasoning engine that determines actions and tool calls.
"""

from typing import Any

from app.agents.schemas import AgentState, ReasoningStep, ToolCall
from app.intelligence.intelligence_service import WebIntelligenceService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ReasoningEngine:
    """
    Determines agent reasoning and tool calls based on classified email.
    Produces structured thinking trace.
    """

    @staticmethod
    async def reason(
        email_id: str,
        thread_id: str,
        classification: dict[str, Any],
        sender_email: str,
        email_subject: str | None = None,
        email_body: str | None = None,
    ) -> AgentState:
        """
        Reason about email and decide actions.

        Args:
            email_id: UUID of email
            thread_id: UUID of thread
            classification: LLM classification output
            sender_email: Email of sender
            email_subject: Original email subject
            email_body: Original email body

        Returns:
            Agent state with reasoning trace and tool decisions
        """
        logger.info("Starting reasoning for email: %s", email_id)

        state = AgentState(email_id=email_id, thread_id=thread_id)

        # Step 1: Analyze classification and apply business rules
        step1 = await ReasoningEngine._step_analyze_classification(
            classification=classification,
            state=state,
        )
        state.reasoning_trace.append(step1)

        if state.should_escalate or len(state.reasoning_trace) >= state.max_steps:
            state.final_decision = "escalate_to_human"
            state.stop_reason = "Business rule triggered escalation"
            return state

        if WebIntelligenceService.should_trigger(classification, email_subject, email_body):
            state.reasoning_trace.append(await ReasoningEngine._step_fetch_web_intelligence(state=state))

        if state.should_escalate or len(state.reasoning_trace) >= state.max_steps:
            return state

        next_decision = step1.next_decision.lower()

        # Step 2: Contact or account checks when indicated
        if "get_contact_profile" in next_decision:
            state.reasoning_trace.append(await ReasoningEngine._step_fetch_contact(sender_email=sender_email, state=state))

        elif "check_account_status" in next_decision:
            state.reasoning_trace.append(await ReasoningEngine._step_check_account_status(sender_email=sender_email, state=state))

        if state.should_escalate or len(state.reasoning_trace) >= state.max_steps:
            return state

        # Step 3: Get thread history when indicated
        if "get_thread_history" in next_decision:
            state.reasoning_trace.append(await ReasoningEngine._step_fetch_thread(thread_id=thread_id, state=state))

        if state.should_escalate or len(state.reasoning_trace) >= state.max_steps:
            return state

        # Step 4: Search knowledge base when indicated
        if "search_knowledge_base" in next_decision:
            query = f"{email_subject or ''} {email_body or ''}".strip()
            state.reasoning_trace.append(await ReasoningEngine._step_search_knowledge(query=query, state=state))

        if len(state.reasoning_trace) >= state.max_steps:
            state.stop_reason = "Max steps reached"
            return state

        # Step 5: Draft reply when indicated
        if "draft_reply" in next_decision:
            context = classification.get("category", "Inquiry")
            state.reasoning_trace.append(await ReasoningEngine._step_draft_reply(context=context, state=state))

        state.final_decision = "send_auto_reply" if not state.should_escalate else "escalate_to_human"
        state.stop_reason = "Reasoning complete"
        return state

    @staticmethod
    async def _step_analyze_classification(
        classification: dict[str, Any],
        state: AgentState,
    ) -> ReasoningStep:
        """Step 1: Analyze classification and determine escalation."""
        logger.debug("Step 1: Analyzing classification")

        category = classification.get("category", "Other")
        confidence = classification.get("confidence", 0.5)
        urgency = classification.get("urgency", "Low")
        sentiment = classification.get("sentiment", "Neutral")

        # Determine if escalation needed
        escalate = False
        escalation_type = None

        requires_human = classification.get("requires_human", False)
        escalation_reason = classification.get("escalation_reason", "Requires human review.")

        if category == "Legal":
            escalate = True
            escalation_type = "legal"
            thought = "Email classified as Legal. Business rule: Always escalate legal matters."
            action = "flag_for_legal"
            next_decision = "flag_for_legal"
            tool_call = ToolCall(
                tool_name="flag_for_legal",
                input_params={"email_id": state.email_id, "thread_id": state.thread_id, "issue_type": "legal_threat"},
            )

        elif requires_human:
            escalate = True
            escalation_type = "manual_review"
            thought = f"Classification requires human review: {escalation_reason}"
            action = "escalate_to_human"
            next_decision = "escalate_to_human"
            tool_call = ToolCall(
                tool_name="escalate_to_human",
                input_params={"email_id": state.email_id, "thread_id": state.thread_id, "reason": escalation_reason},
            )

        elif confidence < 0.70:
            escalate = True
            escalation_type = "uncertain_classification"
            thought = f"Confidence ({confidence:.2f}) below 0.70 threshold. Requires human review."
            action = "escalate_to_human"
            next_decision = "escalate_to_human"
            tool_call = ToolCall(
                tool_name="escalate_to_human",
                input_params={"email_id": state.email_id, "thread_id": state.thread_id, "reason": "Low confidence classification"},
            )

        elif urgency == "Critical":
            escalate = True
            escalation_type = "urgent"
            thought = f"Urgency is Critical. Business rule: Never auto-reply to critical emails."
            action = "escalate_to_human"
            next_decision = "escalate_to_human"
            tool_call = ToolCall(
                tool_name="escalate_to_human",
                input_params={"email_id": state.email_id, "thread_id": state.thread_id, "reason": "Critical urgency detected"},
            )

        elif sentiment == "Negative" and category in ["Complaint", "Bug Report"]:
            thought = f"Negative sentiment {category}. Need to fetch thread history and draft empathetic reply."
            action = "get_thread_history"
            next_decision = "get_thread_history → draft_reply"
            escalate = False

        elif category == "Billing":
            thought = "Billing inquiry. Need account status and relevant policies."
            action = "check_account_status"
            next_decision = "check_account_status → search_knowledge_base → draft_reply"
            escalate = False

        else:
            thought = f"Standard {category}. Will retrieve context and draft response."
            action = "get_thread_history"
            next_decision = "get_thread_history → search_knowledge_base → draft_reply"
            escalate = False

        state.should_escalate = escalate
        state.escalation_type = escalation_type

        return ReasoningStep(
            step_number=1,
            thought=thought,
            action=action,
            tool_call=locals().get("tool_call"),
            next_decision=next_decision,
            confidence=confidence,
        )

    @staticmethod
    async def _step_fetch_contact(sender_email: str, state: AgentState) -> ReasoningStep:
        """Step 2: Fetch contact profile."""
        logger.debug("Step 2: Fetching contact profile")

        step_number = len(state.reasoning_trace) + 1

        thought = f"Fetching contact profile for {sender_email}. Need VIP/churn risk info."
        action = "get_contact_profile"
        tool_call = ToolCall(tool_name="get_contact_profile", input_params={"email": sender_email})

        return ReasoningStep(
            step_number=step_number,
            thought=thought,
            action=action,
            tool_call=tool_call,
            observation="Contact profile fetched (would be populated during execution)",
            next_decision="get_thread_history",
        )

    @staticmethod
    async def _step_check_account_status(sender_email: str, state: AgentState) -> ReasoningStep:
        """Step 2: Check account status."""
        logger.debug("Step 2: Checking account status")

        step_number = len(state.reasoning_trace) + 1

        thought = f"Checking account status for {sender_email}. Need billing and subscription context."
        action = "check_account_status"
        tool_call = ToolCall(tool_name="check_account_status", input_params={"email": sender_email})

        return ReasoningStep(
            step_number=step_number,
            thought=thought,
            action=action,
            tool_call=tool_call,
            observation="Account status retrieved (would be populated during execution)",
            next_decision="search_knowledge_base",
        )

    @staticmethod
    async def _step_fetch_web_intelligence(state: AgentState) -> ReasoningStep:
        """Step 2: Fetch web intelligence context."""
        logger.debug("Step 2: Planning web intelligence fetch")

        step_number = len(state.reasoning_trace) + 1

        thought = "This complaint appears reputation-sensitive. Fetch public review intelligence to enrich response context."
        action = "fetch_web_intelligence"

        return ReasoningStep(
            step_number=step_number,
            thought=thought,
            action=action,
            observation="Web intelligence will be retrieved during execution.",
            next_decision="get_thread_history or check_account_status",
            confidence=1.0,
        )

    @staticmethod
    async def _step_fetch_thread(thread_id: str, state: AgentState) -> ReasoningStep:
        """Step 3: Fetch thread history."""
        logger.debug("Step 3: Fetching thread history")

        step_number = len(state.reasoning_trace) + 1

        thought = "Retrieving email thread to understand context and escalation progression."
        action = "get_thread_history"
        tool_call = ToolCall(tool_name="get_thread_history", input_params={"thread_id": thread_id, "max_emails": 10})

        return ReasoningStep(
            step_number=step_number,
            thought=thought,
            action=action,
            tool_call=tool_call,
            observation="Thread history retrieved (would be populated during execution)",
            next_decision="search_knowledge_base",
        )

    @staticmethod
    async def _step_search_knowledge(query: str, state: AgentState) -> ReasoningStep:
        """Step 4: Search knowledge base."""
        logger.debug("Step 4: Searching knowledge base")

        step_number = len(state.reasoning_trace) + 1

        thought = f"Searching knowledge base for relevant policies. Query: {query[:100]}..."
        action = "search_knowledge_base"
        tool_call = ToolCall(tool_name="search_knowledge_base", input_params={"query": query, "limit": 3})

        return ReasoningStep(
            step_number=step_number,
            thought=thought,
            action=action,
            tool_call=tool_call,
            observation="Knowledge base search completed (would be populated during execution)",
            next_decision="draft_reply",
        )

    @staticmethod
    async def _step_draft_reply(context: str, state: AgentState) -> ReasoningStep:
        """Step 5: Draft reply."""
        logger.debug("Step 5: Drafting reply")

        step_number = len(state.reasoning_trace) + 1

        thought = f"Drafting professional, empathetic reply for {context} category."
        action = "draft_reply"
        tool_call = ToolCall(tool_name="draft_reply", input_params={"context": context, "tone": "professional"})

        return ReasoningStep(
            step_number=step_number,
            thought=thought,
            action=action,
            tool_call=tool_call,
            observation="Reply drafted (would be populated during execution)",
            next_decision="send_auto_reply or escalate_to_human",
        )
