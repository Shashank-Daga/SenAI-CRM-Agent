import json
import re
from typing import Optional

import openai

from app.core.config import settings
from app.schemas.classification import EmailClassification
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LLMClassificationService:
    """
    LLM-based email classification using OpenAI API.
    Handles structured output parsing, retries, and confidence fallback.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or settings.openai_api_key
        self.model = model
        if self.api_key:
            openai.api_key = self.api_key

    async def classify_email(self, prompt: str, max_retries: int = 3) -> EmailClassification:
        """
        Classify email via LLM with structured output and retry logic.

        Args:
            prompt: Full classification prompt with context injected
            max_retries: Number of retry attempts on parse failure

        Returns:
            EmailClassification object

        Raises:
            ValueError: If LLM response cannot be parsed after retries
        """
        logger.info("Classifying email via LLM (model=%s)", self.model)

        if not self.api_key:
            logger.warning("OpenAI API key not configured. Falling back to default classification.")
            return self._get_default_classification()

        for attempt in range(1, max_retries + 1):
            try:
                logger.debug("LLM call attempt %d/%d", attempt, max_retries)
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert email classification system. Return ONLY valid JSON."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                    top_p=0.9,
                    presence_penalty=0.0,
                    frequency_penalty=0.0,
                )

                response_text = response.choices[0].message.content.strip()
                logger.debug("LLM response (attempt %d): %s", attempt, response_text[:200])

                # Parse JSON response
                classification = self._parse_llm_response(response_text)
                logger.info("✓ LLM classification successful (attempt %d)", attempt)
                return classification

            except (json.JSONDecodeError, ValueError) as exc:
                logger.warning("Parse error on attempt %d: %s", attempt, exc)
                if attempt == max_retries:
                    logger.error("Failed to parse LLM response after %d attempts", max_retries)
                    raise
                continue

            except openai.error.OpenAIError as exc:
                logger.error("OpenAI API error: %s", exc)
                if attempt == max_retries:
                    logger.error("OpenAI API failed after %d attempts, using default", max_retries)
                    return self._get_default_classification()
                continue

        return self._get_default_classification()

    @staticmethod
    def _parse_llm_response(response_text: str) -> EmailClassification:
        """
        Parse LLM response text into structured EmailClassification.
        Attempts to extract JSON even if wrapped in markdown or extra text.
        """
        # Try to extract JSON block if wrapped in markdown
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)

        # Parse JSON
        data = json.loads(response_text)

        # Validate and construct
        classification = EmailClassification(**data)
        return classification

    @staticmethod
    def _get_default_classification() -> EmailClassification:
        """
        Fallback classification when LLM unavailable.
        Returns neutral/safe default requiring human review.
        """
        logger.warning("Using default fallback classification (LLM unavailable)")
        return EmailClassification(
            category="Other",
            sentiment="Neutral",
            sentiment_score=0.0,
            urgency="Low",
            requires_human=True,
            escalation_reason="LLM service unavailable. Requires manual review.",
            suggested_reply=None,
            confidence=0.5,
            detected_entities={
                "order_ids": [],
                "ticket_ids": [],
                "monetary_amounts": [],
                "deadlines": [],
                "products_mentioned": [],
            },
        )


class OpenRouterLLMClassificationService(LLMClassificationService):
    """
    Alternative LLM service using OpenRouter API (fallback to OpenAI).
    Supports multiple model providers (Claude, GPT, Llama, etc).
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "openai/gpt-4"):
        self.api_key = api_key or settings.openrouter_api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"

    async def classify_email(self, prompt: str, max_retries: int = 3) -> EmailClassification:
        """Classify using OpenRouter API."""
        logger.info("Classifying email via OpenRouter (model=%s)", self.model)

        if not self.api_key:
            logger.warning("OpenRouter API key not configured. Using default classification.")
            return self._get_default_classification()

        for attempt in range(1, max_retries + 1):
            try:
                import httpx

                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "https://senai-crm.local",
                }

                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json={
                            "model": self.model,
                            "messages": [
                                {"role": "system", "content": "You are an expert email classification system. Return ONLY valid JSON."},
                                {"role": "user", "content": prompt},
                            ],
                            "temperature": 0.3,
                        },
                    )

                    if response.status_code != 200:
                        logger.error("OpenRouter API error: %s", response.text)
                        if attempt == max_retries:
                            return self._get_default_classification()
                        continue

                    data = response.json()
                    response_text = data["choices"][0]["message"]["content"].strip()
                    classification = self._parse_llm_response(response_text)
                    logger.info("✓ OpenRouter classification successful (attempt %d)", attempt)
                    return classification

            except Exception as exc:
                logger.error("OpenRouter error (attempt %d): %s", attempt, exc)
                if attempt == max_retries:
                    return self._get_default_classification()
                continue

        return self._get_default_classification()
