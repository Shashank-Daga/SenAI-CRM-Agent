"""
Database models for agent execution logs and escalations.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.session import Base


class AgentReasoningLog(Base):
    """Stores complete reasoning trace for audit and analysis."""

    __tablename__ = "agent_reasoning_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(UUID(as_uuid=True), ForeignKey("emails.id"), nullable=False, index=True)
    thread_id = Column(UUID(as_uuid=True), ForeignKey("threads.id"), nullable=False, index=True)
    
    # Agent execution details
    reasoning_trace = Column(JSONB, nullable=False, default=list)
    total_steps = Column(String(32), nullable=False, default="0")
    final_decision = Column(String(128), nullable=False)
    requires_human = Column(Boolean, nullable=False, default=False)
    escalation_triggered = Column(Boolean, nullable=False, default=False)
    escalation_type = Column(String(64), nullable=True)
    
    # Action outcomes
    drafted_reply = Column(Text, nullable=True)
    tickets_created = Column(JSONB, nullable=False, default=list)
    executed_actions = Column(JSONB, nullable=False, default=list)
    errors = Column(JSONB, nullable=False, default=list)
    web_intelligence = Column(JSONB, nullable=True)

    # Execution metadata
    execution_time_ms = Column(String(32), nullable=False, default="0")
    is_dry_run = Column(Boolean, nullable=False, default=False)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class AgentEscalation(Base):
    """Records escalation actions triggered by agent."""

    __tablename__ = "agent_escalations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(UUID(as_uuid=True), ForeignKey("emails.id"), nullable=False, index=True)
    thread_id = Column(UUID(as_uuid=True), ForeignKey("threads.id"), nullable=False, index=True)
    reasoning_log_id = Column(UUID(as_uuid=True), ForeignKey("agent_reasoning_logs.id"), nullable=True)
    
    escalation_type = Column(String(64), nullable=False)  # legal, security, vip_retention, etc
    priority = Column(String(32), nullable=False)  # Critical, High, Medium, Low
    reason = Column(Text, nullable=False)
    metadata = Column(JSONB, nullable=True)
    
    # Resolution tracking
    resolved = Column(Boolean, nullable=False, default=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class AgentDraftedReply(Base):
    """Stores drafted replies for human review."""

    __tablename__ = "agent_drafted_replies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(UUID(as_uuid=True), ForeignKey("emails.id"), nullable=False, index=True)
    reasoning_log_id = Column(UUID(as_uuid=True), ForeignKey("agent_reasoning_logs.id"), nullable=True)
    
    draft_content = Column(Text, nullable=False)
    tone = Column(String(32), nullable=False)  # professional, empathetic, technical
    policy_references = Column(JSONB, nullable=False, default=list)
    
    # Approval tracking
    approved = Column(Boolean, nullable=False, default=False)
    approved_by = Column(String(255), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    sent = Column(Boolean, nullable=False, default=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
