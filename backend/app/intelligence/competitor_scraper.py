"""
Competitor pricing scraper for market intelligence.
"""

import asyncio
import re
from typing import Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from app.intelligence.robots import RobotsChecker
from app.intelligence.summarizer import summarize_pricing_differences
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CompetitorPricingScraper:
    """Scrapes competitor pricing pages for tier and feature data."""

    USER_AGENT = "SenAI-Agent/1.0"
    DEFAULT_TIMEOUT = 10
    MAX_RETRIES = 3

    def __init__(self, timeout: int = DEFAULT_TIMEOUT, retries: int = MAX_RETRIES):
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    async def fetch_pricing(self, pricing_url: str) -> dict[str, Any]:
        if not pricing_url:
            raise ValueError("Pricing URL is required for competitor scraping.")

        if not await RobotsChecker.is_allowed(pricing_url):
            logger.warning("Robots.txt denied scraping of competitor pricing URL %s", pricing_url)
            return {
                "source_url": pricing_url,
                "tiers": [],
                "summary": "Pricing scraping disallowed by robots.txt.",
            }

        for attempt in range(1, self.retries + 1):
            try:
                html = await asyncio.to_thread(self._get_html, pricing_url)
                tiers = self._parse_pricing_page(html)
                summary = summarize_pricing_differences(tiers)
                return {"source_url": pricing_url, "tiers": tiers, "summary": summary}
            except Exception as exc:
                logger.warning("Competitor pricing scrape attempt %d failed for %s: %s", attempt, pricing_url, exc)
                if attempt == self.retries:
                    return {
                        "source_url": pricing_url,
                        "tiers": [],
                        "summary": "Unable to extract competitor pricing data.",
                    }
        return {
            "source_url": pricing_url,
            "tiers": [],
            "summary": "Unable to extract competitor pricing data.",
        }

    def _get_html(self, url: str) -> str:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def _parse_pricing_page(self, html: str) -> list[dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        tiers = []

        cards = soup.select("[class*=pricing], [class*=PriceCard], [class*=tier], [class*=plan]")
        if cards:
            for card in cards[:6]:
                title = self._extract_text(card.select_one("h2, h3, .plan-name, .tier-name"))
                price = self._extract_text(card.select_one(".price, .plan-price, .tier-price, h4"))
                features = [self._extract_text(li) for li in card.select("li") if self._extract_text(li)]
                if title or price or features:
                    tiers.append({"name": title or "Tier", "price": price or "N/A", "features": features})

        if not tiers:
            table_rows = soup.select("table tr")
            for row in table_rows[:6]:
                columns = row.find_all(["th", "td"])
                if len(columns) >= 2:
                    name = self._extract_text(columns[0])
                    price = self._extract_text(columns[1])
                    tiers.append({"name": name or "Tier", "price": price or "N/A", "features": []})

        if not tiers:
            raise ValueError("Unable to parse pricing tiers from target page.")

        return tiers

    @staticmethod
    def _extract_text(element: Any) -> str:
        if element is None:
            return ""
        return element.get_text(separator=" ", strip=True)
