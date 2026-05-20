"""
Database model for web intelligence caching.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.db.session import Base


class WebIntelligenceCache(Base):
    __tablename__ = "web_intelligence_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_url = Column(String(1024), nullable=False, index=True)
    target_entity = Column(String(255), nullable=False, index=True)
    scraped_data = Column(JSONB, nullable=False, default=dict)
    scraped_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
