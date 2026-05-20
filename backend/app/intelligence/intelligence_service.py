"""
High-level intelligence service for reputation and market enrichment.
"""

from typing import Any, Optional

from app.core.config import settings
from app.intelligence.cache_service import WebIntelligenceCacheService
from app.intelligence.competitor_scraper import CompetitorPricingScraper
from app.intelligence.reputation_scraper import ReputationScraper
from app.intelligence.summarizer import build_reputation_summary
from app.utils.logger import get_logger

logger = get_logger(__name__)


class WebIntelligenceService:
    """Orchestrates web intelligence scraping and caching."""

    def __init__(self):
        self.reputation_scraper = ReputationScraper(timeout=settings.scrape_timeout_seconds, retries=settings.scrape_retry_count)
        self.pricing_scraper = CompetitorPricingScraper(timeout=settings.scrape_timeout_seconds, retries=settings.scrape_retry_count)

    async def get_reputation(self, company_name: str, session: Optional[Any] = None) -> dict[str, Any]:
        """Return cached reputation intelligence or scrape fresh data."""
        source_url = f"https://www.trustpilot.com/review/{company_name.lower().replace(' ', '-')}.json"
        target_entity = company_name.lower().strip()

        cached = await WebIntelligenceCacheService.get_cached_data(source_url, target_entity, session=session)
        if cached is not None:
            cached.update({"cached": True})
            return cached

        try:
            reputation_data = await self.reputation_scraper.fetch(company_name)
            reputation_data["company"] = company_name
            reputation_data["cached"] = False
            reputation_data["summary"] = build_reputation_summary(reputation_data)
            await WebIntelligenceCacheService.set_cached_data(source_url, target_entity, reputation_data, ttl_hours=settings.intelligence_cache_ttl_hours, session=session)
            return reputation_data
        except Exception as exc:
            logger.warning("Reputation intelligence fetch failed for %s: %s", company_name, exc)
            return {
                "company": company_name,
                "rating": None,
                "review_count": None,
                "themes": [],
                "source": "unknown",
                "source_url": source_url,
                "summary": "Unable to fetch reputation intelligence at this time.",
                "cached": False,
            }

    async def get_competitor_pricing(self, pricing_url: str, session: Optional[Any] = None) -> dict[str, Any]:
        """Return competitor pricing intelligence, optionally using cache."""
        target_entity = pricing_url.strip().lower()
        cached = await WebIntelligenceCacheService.get_cached_data(pricing_url, target_entity, session=session)
        if cached is not None:
            cached.update({"cached": True})
            return cached

        try:
            pricing_data = await self.pricing_scraper.fetch_pricing(pricing_url)
            pricing_data["cached"] = False
            await WebIntelligenceCacheService.set_cached_data(pricing_url, target_entity, pricing_data, ttl_hours=settings.intelligence_cache_ttl_hours, session=session)
            return pricing_data
        except Exception as exc:
            logger.warning("Competitor pricing fetch failed for %s: %s", pricing_url, exc)
            return {
                "source_url": pricing_url,
                "tiers": [],
                "summary": "Unable to fetch competitor pricing intelligence at this time.",
                "cached": False,
            }

    @staticmethod
    def should_trigger(classification: dict[str, Any], subject: str | None, body: str | None) -> bool:
        """Determine whether web intelligence should be applied to this email."""
        text = " ".join([subject or "", body or ""]).lower()
        keywords = ["review", "trustpilot", "g2", "post publicly"]
        contains_signal = any(keyword in text for keyword in keywords)
        is_complaint = classification.get("category") == "Complaint"
        urgency = classification.get("urgency")
        sentiment_score = classification.get("sentiment_score", 0.0)

        return contains_signal and is_complaint and urgency in {"High", "Critical"} and sentiment_score < -0.6

    async def enrich_email_context(
        self,
        subject: str | None,
        body: str | None,
        classification: dict[str, Any],
        session: Optional[Any] = None,
    ) -> dict[str, Any]:
        """Fetch intelligence data when a trigger condition is met."""
        company_name = settings.company_name
        if not company_name:
            company_name = "SenAI"

        reputation = await self.get_reputation(company_name, session=session)
        summary = reputation.get("summary")

        return {
            "company": company_name,
            "reputation": reputation,
            "summary": summary,
        }
