"""
Agent executor orchestrates reasoning, tool execution, and audit logging.
"""

import time
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.reasoning_engine import ReasoningEngine
from app.agents.schemas import AgentExecutionResult
from app.intelligence.intelligence_service import WebIntelligenceService
from app.llm.classification_service import LLMClassificationService
from app.models.email import Email
from app.models.agent import AgentReasoningLog
from app.prompts.classification_prompt import build_classification_prompt
from app.rag.retrieval_service import RAGRetrievalService
from app.services.thread_service import ThreadContextService
from app.tools.base import get_tool_registry
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AgentExecutor:
    """Orchestrates the autonomous triage agent execution."""

    def __init__(self, tool_registry=None):
        self.tool_registry = tool_registry or get_tool_registry()
        self.llm_service = LLMClassificationService()
        self.intelligence_service = WebIntelligenceService()

    async def execute(self, email_id: str, session: AsyncSession, is_dry_run: bool = False) -> AgentExecutionResult:
        """Execute the agent for a specific email."""
        start_time = time.perf_counter()
        logger.info("Agent execution started for email %s dry_run=%s", email_id, is_dry_run)

        query = select(Email).where(Email.id == email_id)
        result = await session.execute(query)
        email = result.scalars().first()

        if not email:
            raise ValueError(f"Email not found: {email_id}")

        thread_id = str(email.thread_id)
        sender_email = email.sender_contact.email if email.sender_contact else "unknown"

        classification = await self._classify_email(email=email, session=session)
        classification_map = classification.model_dump()

        state = await ReasoningEngine.reason(
            email_id=email_id,
            thread_id=thread_id,
            classification=classification_map,
            sender_email=sender_email,
            email_subject=email.subject,
            email_body=email.body,
        )

        executed_actions: list[str] = []
        tickets_created: list[dict[str, Any]] = []
        drafted_reply: str | None = None
        errors: list[str] = []

        if is_dry_run:
            for step in state.reasoning_trace:
                if step.action == "fetch_web_intelligence":
                    step.observation = "Dry-run: intelligence enrichment skipped"
                elif step.tool_call:
                    step.observation = "Dry-run: tool execution skipped"
        else:
            web_intelligence_data = None
            for step in state.reasoning_trace:
                if step.action == "fetch_web_intelligence":
                    try:
                        web_intelligence_data = await self.intelligence_service.enrich_email_context(
                            subject=email.subject,
                            body=email.body,
                            classification=classification_map,
                            session=session,
                        )
                        state.web_intelligence = web_intelligence_data
                        step.observation = web_intelligence_data.get("summary", "Web intelligence fetched.")
                        executed_actions.append("fetch_web_intelligence")
                    except Exception as exc:
                        errors.append(str(exc))
                        step.observation = f"Web intelligence fetch failed: {exc}"
                    continue

                if not step.tool_call:
                    continue

                tool_result = await self.tool_registry.execute(
                    step.tool_call.tool_name,
                    **step.tool_call.input_params,
                )
                if tool_result.get("success"):
                    step.observation = str(tool_result.get("data"))
                else:
                    step.observation = str(tool_result.get("error"))

                if tool_result.get("success"):
                    executed_actions.append(step.tool_call.tool_name)
                    data = tool_result.get("data") or {}

                    if step.tool_call.tool_name == "draft_reply":
                        drafted_reply = data.get("draft")
                    elif step.tool_call.tool_name == "create_internal_ticket":
                        tickets_created.append(data)

                else:
                    errors.append(tool_result.get("error") or "Unknown tool error")

            if state.final_decision == "send_auto_reply" and drafted_reply:
                send_result = await self.tool_registry.execute(
                    "send_auto_reply",
                    email_id=email_id,
                    draft_reply=drafted_reply,
                    recipient=email.recipient,
                    tone="professional",
                )
                if send_result.get("success"):
                    executed_actions.append("send_auto_reply")
                    drafted_reply = drafted_reply
                else:
                    errors.append(send_result.get("error") or "Failed to send auto reply")

        execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

        agent_result = AgentExecutionResult(
            email_id=email_id,
            thread_id=thread_id,
            reasoning_trace=state.reasoning_trace,
            total_steps=len(state.reasoning_trace),
            final_decision=state.final_decision or "no_action",
            requires_human=state.should_escalate,
            escalation_triggered=state.should_escalate,
            escalation_type=state.escalation_type,
            drafted_reply=drafted_reply,
            tickets_created=tickets_created,
            executed_actions=executed_actions,
            web_intelligence=web_intelligence_data if not is_dry_run else None,
            errors=errors,
            execution_time_ms=execution_time_ms,
            is_dry_run=is_dry_run,
        )

        if not is_dry_run:
            await self._persist_reasoning_log(session, agent_result)

        return agent_result

    async def _classify_email(self, email: Email, session: AsyncSession) -> Any:
        """Classify email using LLM with thread context and RAG injection."""
        logger.debug("Starting classification for agent execution: %s", email.id)

        thread_context = await ThreadContextService.get_thread_context(str(email.thread_id), session, max_emails=10)
        search_query = f"{email.subject or ''} {email.body or ''}"[:500]
        rag_context = RAGRetrievalService.get_context_string(search_query, top_k=3)
        prompt = build_classification_prompt(
            thread_context=thread_context,
            sender=email.sender_contact.email if email.sender_contact else "unknown",
            recipient=email.recipient,
            subject=email.subject,
            body=email.body,
            rag_context=rag_context,
        )

        return await self.llm_service.classify_email(prompt)

    async def _persist_reasoning_log(self, session: AsyncSession, result: AgentExecutionResult) -> None:
        """Persist agent reasoning log for audit."""
        log = AgentReasoningLog(
            email_id=UUID(result.email_id),
            thread_id=UUID(result.thread_id),
            reasoning_trace=[step.model_dump() for step in result.reasoning_trace],
            total_steps=str(result.total_steps),
            final_decision=result.final_decision,
            requires_human=result.requires_human,
            escalation_triggered=result.escalation_triggered,
            escalation_type=result.escalation_type,
            drafted_reply=result.drafted_reply,
            tickets_created=result.tickets_created,
            executed_actions=result.executed_actions,
            web_intelligence=result.web_intelligence,
            errors=result.errors,
            execution_time_ms=str(result.execution_time_ms),
            is_dry_run=result.is_dry_run,
        )
        session.add(log)
        await session.commit()
        logger.info("Persisted agent reasoning log: %s", log.id)
