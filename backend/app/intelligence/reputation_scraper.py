"""
Reputation scraper for Trustpilot and G2.
"""

import asyncio
import re
from typing import Any
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from app.intelligence.robots import RobotsChecker
from app.intelligence.summarizer import extract_common_themes
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ReputationScraper:
    """Scrapes external review sites for company reputation intelligence."""

    USER_AGENT = "SenAI-Agent/1.0"
    DEFAULT_TIMEOUT = 10
    MAX_RETRIES = 3

    def __init__(self, timeout: int = DEFAULT_TIMEOUT, retries: int = MAX_RETRIES):
        self.timeout = timeout
        self.retries = retries
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    async def fetch(self, company_name: str) -> dict[str, Any]:
        """Fetch reputation intelligence for the provided company."""
        normalized_company = company_name.strip()
        if not normalized_company:
            raise ValueError("Company name is required for reputation scraping.")

        trustpilot_url = self._build_trustpilot_url(normalized_company)
        logger.info("Fetching reputation data from Trustpilot for %s", normalized_company)

        result = await self._fetch_site(trustpilot_url, self._parse_trustpilot_page)
        if result["success"]:
            result_data = result["data"]
            result_data["source"] = "Trustpilot"
            result_data["source_url"] = trustpilot_url
            return result_data

        g2_url = self._build_g2_url(normalized_company)
        logger.info("Falling back to G2 for %s", normalized_company)
        result = await self._fetch_site(g2_url, self._parse_g2_page)
        if result["success"]:
            result_data = result["data"]
            result_data["source"] = "G2"
            result_data["source_url"] = g2_url
            return result_data

        logger.warning("Reputation scraping failed for %s", normalized_company)
        return {
            "company": normalized_company,
            "rating": None,
            "review_count": None,
            "themes": [],
            "source": "unknown",
            "source_url": trustpilot_url,
        }

    async def _fetch_site(self, url: str, parser: callable) -> dict[str, Any]:
        if not await RobotsChecker.is_allowed(url):
            logger.warning("Robots.txt denied scraping of %s", url)
            return {"success": False, "data": {}, "error": "Robots disallow scraping"}

        for attempt in range(1, self.retries + 1):
            try:
                html = await asyncio.to_thread(self._get_html, url)
                data = parser(html)
                return {"success": True, "data": data}
            except Exception as exc:
                logger.warning("Reputation scrape attempt %d failed for %s: %s", attempt, url, exc)
                if attempt == self.retries:
                    return {"success": False, "data": {}, "error": str(exc)}
        return {"success": False, "data": {}, "error": "Unknown error"}

    def _get_html(self, url: str) -> str:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    @staticmethod
    def _build_trustpilot_url(company_name: str) -> str:
        slug = quote_plus(company_name.lower().replace(" ", "-"))
        return f"https://www.trustpilot.com/review/{slug}"

    @staticmethod
    def _build_g2_url(company_name: str) -> str:
        slug = quote_plus(company_name.lower().replace(" ", "-"))
        return f"https://www.g2.com/products/{slug}/reviews"

    def _parse_trustpilot_page(self, html: str) -> dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")
        rating = self._parse_rating(soup)
        review_count = self._parse_review_count(soup)
        themes = self._parse_themes(soup)
        return {"company": None, "rating": rating, "review_count": review_count, "themes": themes}

    def _parse_g2_page(self, html: str) -> dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")
        rating = self._parse_rating(soup)
        review_count = self._parse_review_count(soup)
        themes = self._parse_themes(soup)
        return {"company": None, "rating": rating, "review_count": review_count, "themes": themes}

    def _parse_rating(self, soup: BeautifulSoup) -> float | None:
        rating_text = None
        rating_selectors = [
            "span[data-business-unit-rating]",
            "div[data-rating]",
            "span[class*=star-rating]",
            "div[class*=stars]",
        ]
        for selector in rating_selectors:
            element = soup.select_one(selector)
            if element and element.text:
                rating_text = element.text
                break

        if not rating_text:
            rating_text = soup.find(text=re.compile(r"\d\.\d\s+out of 5"))

        if not rating_text:
            return None

        match = re.search(r"(\d\.\d)", rating_text)
        return float(match.group(1)) if match else None

    def _parse_review_count(self, soup: BeautifulSoup) -> int | None:
        count_text = None
        selectors = [
            "span[data-review-count]",
            "div[class*=review-count]",
            "span[class*=headline]",
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.text:
                count_text = element.text
                break

        if not count_text:
            count_text = soup.find(text=re.compile(r"[\d,]+\s+reviews?", re.IGNORECASE))

        if not count_text:
            return None

        digits = re.sub(r"[^\d]", "", count_text)
        return int(digits) if digits else None

    def _parse_themes(self, soup: BeautifulSoup) -> list[str]:
        review_texts = []
        cards = soup.select("div.review-card, div.paper, div.g-grid")
        if not cards:
            cards = soup.select("p, span")

        for card in cards[:10]:
            text = card.get_text(separator=" ", strip=True)
            if text:
                review_texts.append(text)

        return extract_common_themes(review_texts)
