import uuid
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.session import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    thread_id = Column(UUID(as_uuid=True), ForeignKey("threads.id"), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=False)
    recipient = Column(String(255), nullable=False, index=True)
    message_id = Column(String(512), nullable=False, unique=True, index=True)
    subject = Column(String(512), nullable=True)
    body = Column(Text, nullable=True)
    received_at = Column(DateTime(timezone=True), nullable=False)
    priority = Column(String(32), nullable=False, default="Normal")
    is_spam = Column(Boolean, nullable=False, default=False)
    sentiment = Column(String(32), nullable=False, default="neutral")
    urgency_tags = Column(JSONB, nullable=False, default=list)
    security_flags = Column(JSONB, nullable=False, default=list)
    internal_email = Column(Boolean, nullable=False, default=False)
    metadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    thread = relationship("Thread", back_populates="emails")
    sender_contact = relationship("Contact", back_populates="emails")
