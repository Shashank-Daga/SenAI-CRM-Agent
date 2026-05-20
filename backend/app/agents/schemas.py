"""
Agent reasoning and tool execution models.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """Represents a tool invocation during agent reasoning."""

    tool_name: str = Field(..., description="Name of the tool")
    input_params: dict[str, Any] = Field(default_factory=dict, description="Tool input parameters")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "tool_name": "search_knowledge_base",
                "input_params": {"query": "SLA response times"},
                "timestamp": "2026-05-20T10:00:00Z",
            }
        }


class ReasoningStep(BaseModel):
    """Single step in agent reasoning trace."""

    step_number: int = Field(..., ge=1, le=6, description="Step number (1-6 max)")
    thought: str = Field(..., min_length=1, max_length=2000, description="Agent's internal reasoning")
    action: str = Field(..., description="Tool name or decision")
    tool_call: Optional[ToolCall] = Field(None, description="Tool invocation (if applicable)")
    observation: str = Field(default="", max_length=5000, description="Tool output or observation")
    next_decision: str = Field(..., description="What happens next")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

    class Config:
        json_schema_extra = {
            "example": {
                "step_number": 1,
                "thought": "This email mentions 'lawsuit' and 'breach of contract'. Legal team must review.",
                "action": "flag_for_legal",
                "tool_call": {
                    "tool_name": "flag_for_legal",
                    "input_params": {"issue_type": "contract_dispute"},
                },
                "observation": "Legal escalation created",
                "next_decision": "Escalate to human for final decision",
                "confidence": 0.95,
            }
        }


class AgentExecutionResult(BaseModel):
    """Complete result of agent reasoning and execution."""

    email_id: str
    thread_id: str
    reasoning_trace: list[ReasoningStep] = Field(default_factory=list)
    total_steps: int = Field(default=0, ge=0, le=6)
    final_decision: str = Field(..., description="Final action taken or recommended")
    requires_human: bool = Field(default=False)
    escalation_triggered: bool = Field(default=False)
    escalation_type: Optional[str] = Field(None, description="e.g., legal, security, vip_retention")
    drafted_reply: Optional[str] = Field(None)
    tickets_created: list[dict[str, Any]] = Field(default_factory=list)
    executed_actions: list[str] = Field(default_factory=list)
    web_intelligence: Optional[dict[str, Any]] = Field(default=None)
    errors: list[str] = Field(default_factory=list)
    execution_time_ms: float = Field(default=0.0)
    is_dry_run: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "email_id": "550e8400-e29b-41d4-a716-446655440000",
                "thread_id": "660e8400-e29b-41d4-a716-446655440001",
                "reasoning_trace": [
                    {
                        "step_number": 1,
                        "thought": "Email contains legal language and threat of lawsuit",
                        "action": "flag_for_legal",
                        "observation": "Legal escalation created",
                        "next_decision": "Escalate and hold for human review",
                        "confidence": 0.98,
                    }
                ],
                "total_steps": 1,
                "final_decision": "escalate_to_legal_team",
                "requires_human": True,
                "escalation_triggered": True,
                "escalation_type": "legal",
                "is_dry_run": False,
            }
        }


class AgentState(BaseModel):
    """Mutable state during agent execution."""

    email_id: str
    thread_id: str
    current_step: int = 0
    max_steps: int = 6
    reasoning_trace: list[ReasoningStep] = Field(default_factory=list)
    tool_calls_made: list[ToolCall] = Field(default_factory=list)
    last_observation: str = ""
    final_decision: Optional[str] = None
    should_escalate: bool = False
    escalation_type: Optional[str] = None
    web_intelligence: Optional[dict[str, Any]] = None
    stop_reason: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email_id": "550e8400-e29b-41d4-a716-446655440000",
                "thread_id": "660e8400-e29b-41d4-a716-446655440001",
                "current_step": 3,
                "reasoning_trace": [],
            }
        }
