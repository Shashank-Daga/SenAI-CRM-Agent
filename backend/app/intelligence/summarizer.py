"""
Summarizer utilities for web intelligence data.
"""

import collections
import re
from typing import Any

from app.utils.logger import get_logger

logger = get_logger(__name__)

COMMON_STOPWORDS = {
    "and", "the", "for", "with", "from", "that", "this", "their", "our", "your",
    "you", "are", "was", "were", "have", "has", "had", "not", "but", "all",
    "can", "will", "would", "could", "should", "about", "service", "company",
}


def extract_common_themes(texts: list[str], max_themes: int = 4) -> list[str]:
    """Extract frequent complaint themes from review snippets."""
    if not texts:
        return []

    token_counts = collections.Counter()
    for text in texts:
        sanitized = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
        tokens = [word for word in sanitized.split() if len(word) > 3 and word not in COMMON_STOPWORDS]
        token_counts.update(tokens)

    most_common = [token for token, _ in token_counts.most_common(max_themes)]
    logger.debug("Extracted themes: %s", most_common)
    return most_common


def build_reputation_summary(reputation_data: dict[str, Any]) -> str:
    """Build a human-readable intelligence summary from reputation data."""
    rating = reputation_data.get("rating")
    review_count = reputation_data.get("review_count")
    themes = reputation_data.get("themes") or []
    source = reputation_data.get("source", "web")

    parts = [f"Public reputation signal from {source}."]
    if rating is not None:
        parts.append(f"Average rating is {rating:.1f}.")
    if review_count is not None:
        parts.append(f"There are {review_count} published reviews.")
    if themes:
        parts.append(f"Common complaint themes include {', '.join(themes)}.")

    return " ".join(parts)


def summarize_pricing_differences(tiers: list[dict[str, Any]]) -> str:
    """Summarize pricing tiers into a short market intelligence block."""
    if not tiers:
        return "No pricing tiers were extracted."

    summary_lines = []
    tier_names = [tier.get("name", "Tier") for tier in tiers if tier.get("name")]
    if tier_names:
        summary_lines.append(f"Detected pricing tiers: {', '.join(tier_names)}.")

    prices = [tier.get("price") for tier in tiers if tier.get("price")]
    if prices:
        unique_prices = sorted(set(prices), key=lambda x: str(x))
        summary_lines.append(f"Price points include {', '.join(unique_prices)}.")

    features = []
    for tier in tiers:
        tier_features = tier.get("features") or []
        if tier_features:
            features.append(f"{tier.get('name', 'Tier')} includes {', '.join(tier_features[:3])}")

    if features:
        summary_lines.append("Feature highlights: " + "; ".join(features[:3]) + ".")

    return " ".join(summary_lines)
