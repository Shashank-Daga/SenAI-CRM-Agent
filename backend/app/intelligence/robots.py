"""
Robots.txt compliance checker for web intelligence scraping.
"""

import asyncio
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests

from app.utils.logger import get_logger

logger = get_logger(__name__)


class RobotsChecker:
    """Simple robots.txt compliance helper."""

    DEFAULT_USER_AGENT = "SenAI-Agent"
    DEFAULT_TIMEOUT = 10

    @staticmethod
    async def is_allowed(url: str, user_agent: str = DEFAULT_USER_AGENT) -> bool:
        """Return whether the scraper is allowed to fetch the provided URL."""
        parsed = urlparse(url)
        robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "/robots.txt")

        try:
            return await asyncio.to_thread(RobotsChecker._check_robots, robots_url, url, user_agent)
        except Exception as exc:
            logger.warning("Robots.txt check failed for %s: %s. Proceeding with caution.", url, exc)
            return True

    @staticmethod
    def _check_robots(robots_url: str, url: str, user_agent: str) -> bool:
        parser = RobotFileParser()
        parser.set_url(robots_url)
        parser.read()
        allowed = parser.can_fetch(user_agent, url)
        if not allowed:
            logger.info("Robots.txt disallows scraping %s for %s", url, user_agent)
        return allowed
