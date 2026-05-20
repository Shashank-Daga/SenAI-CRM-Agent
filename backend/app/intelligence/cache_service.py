"""
Cache service for web intelligence scraping results.
"""

from datetime import datetime, timedelta
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.web_intelligence_cache import WebIntelligenceCache
from app.utils.logger import get_logger

logger = get_logger(__name__)


class WebIntelligenceCacheService:
    """Service for storing and retrieving cached web intelligence."""

    DEFAULT_TTL_HOURS = 6

    @staticmethod
    async def get_cached_data(
        source_url: str,
        target_entity: str,
        session: Optional[AsyncSession] = None,
    ) -> Optional[dict[str, Any]]:
        """Return cached data if it exists and has not expired."""
        own_session = False
        if session is None:
            session = AsyncSessionLocal()
            own_session = True

        try:
            query = select(WebIntelligenceCache).where(
                WebIntelligenceCache.source_url == source_url,
                WebIntelligenceCache.target_entity == target_entity,
                WebIntelligenceCache.expires_at > datetime.utcnow(),
            )
            result = await session.execute(query)
            record = result.scalars().first()
            if record:
                logger.info("Using cached web intelligence for %s", target_entity)
                return record.scraped_data
            return None
        except Exception as exc:
            logger.warning("Cache read failure for %s: %s", target_entity, exc)
            return None
        finally:
            if own_session:
                await session.close()

    @staticmethod
    async def set_cached_data(
        source_url: str,
        target_entity: str,
        scraped_data: dict[str, Any],
        ttl_hours: int = DEFAULT_TTL_HOURS,
        session: Optional[AsyncSession] = None,
    ) -> None:
        """Persist scraped data into cache with expiration."""
        own_session = False
        if session is None:
            session = AsyncSessionLocal()
            own_session = True

        try:
            expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
            cache_record = WebIntelligenceCache(
                source_url=source_url,
                target_entity=target_entity,
                scraped_data=scraped_data,
                scraped_at=datetime.utcnow(),
                expires_at=expires_at,
            )
            session.add(cache_record)
            await session.commit()
            logger.info("Cached intelligence for %s until %s", target_entity, expires_at.isoformat())
        except Exception as exc:
            logger.warning("Failed to cache web intelligence for %s: %s", target_entity, exc)
            if session is not None and not own_session:
                await session.rollback()
        finally:
            if own_session:
                await session.close()
