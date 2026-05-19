from __future__ import annotations

import re
from typing import Any, Dict, List

KEYWORD_BLOCKLIST = [
    "buy now",
    "free",
    "click here",
    "act now",
    "unsubscribe",
    "win money",
    "urgent response",
    "account suspended",
]
SUSPICIOUS_DOMAINS = [
    "cheapdeals.com",
    "noreply.spam",
    "malicious.example",
    "suspicious-domain.com",
]
URGENCY_KEYWORDS = {
    "urgent": "urgent",
    "p0": "p0",
    "legal": "legal",
    "cease and desist": "legal",
    "ransomware": "ransomware",
    "lawsuit": "legal",
    "breach": "security",
}
SECURITY_KEYWORDS = {
    "suspicious login": "suspicious_login",
    "data breach": "data_breach",
    "ransomware": "ransomware",
    "unauthorized access": "suspicious_login",
    "credential leak": "data_breach",
}
INTERNAL_DOMAINS = ["@internal.com", "@mycompany.com"]
POSITIVE_KEYWORDS = ["thank you", "thanks", "great", "appreciate", "awesome", "happy"]
NEGATIVE_KEYWORDS = ["angry", "disappointed", "frustrated", "upset", "bad", "hate"]

PRIORITY_MAP = {
    "ransomware": "Critical",
    "legal": "High",
    "refund": "Medium",
    "spam": "Low",
    "normal": "Normal",
}
PRIORITY_ORDER = ["Low", "Normal", "Medium", "High", "Critical"]


def normalize_text(*parts: Any) -> str:
    return " ".join(str(part).strip() for part in parts if part).lower()


def detect_internal(sender: str) -> bool:
    sender_lower = sender.lower()
    return any(domain in sender_lower for domain in INTERNAL_DOMAINS)


def detect_spam(subject: str | None, body: str | None, sender: str) -> bool:
    text = normalize_text(subject, body)
    if any(block in text for block in KEYWORD_BLOCKLIST):
        return True
    return any(domain in sender.lower() for domain in SUSPICIOUS_DOMAINS)


def detect_urgency(subject: str | None, body: str | None) -> List[str]:
    text = normalize_text(subject, body)
    tags: List[str] = []
    for keyword, tag in URGENCY_KEYWORDS.items():
        if keyword in text and tag not in tags:
            tags.append(tag)
    return tags


def detect_security(subject: str | None, body: str | None) -> List[str]:
    text = normalize_text(subject, body)
    flags: List[str] = []
    for keyword, flag in SECURITY_KEYWORDS.items():
        if keyword in text and flag not in flags:
            flags.append(flag)
    return flags


def sentiment_score(subject: str | None, body: str | None) -> str:
    text = normalize_text(subject, body)
    positive_count = sum(text.count(word) for word in POSITIVE_KEYWORDS)
    negative_count = sum(text.count(word) for word in NEGATIVE_KEYWORDS)
    if positive_count > negative_count:
        return "positive"
    if negative_count > positive_count:
        return "negative"
    return "neutral"


def determine_priority(subject: str | None, body: str | None, is_spam: bool, urgency_tags: List[str], security_flags: List[str]) -> str:
    if is_spam:
        return PRIORITY_MAP["spam"]

    text = normalize_text(subject, body)
    if "ransomware" in text or "ransomware" in security_flags:
        return PRIORITY_MAP["ransomware"]
    if any(tag in ["legal", "urgent", "p0"] for tag in urgency_tags):
        return PRIORITY_MAP["legal"]
    if "refund" in text:
        return PRIORITY_MAP["refund"]
    return PRIORITY_MAP["normal"]


def merge_priority(current: str, candidate: str) -> str:
    current_index = PRIORITY_ORDER.index(current) if current in PRIORITY_ORDER else 1
    candidate_index = PRIORITY_ORDER.index(candidate) if candidate in PRIORITY_ORDER else 1
    return current if current_index >= candidate_index else candidate


def analyze_email(subject: str | None, body: str | None, sender: str) -> Dict[str, Any]:
    is_spam = detect_spam(subject, body, sender)
    urgency_tags = detect_urgency(subject, body)
    security_flags = detect_security(subject, body)
    internal_email = detect_internal(sender)
    sentiment = sentiment_score(subject, body)
    priority = determine_priority(subject, body, is_spam, urgency_tags, security_flags)
    return {
        "is_spam": is_spam,
        "urgency_tags": urgency_tags,
        "security_flags": security_flags,
        "internal_email": internal_email,
        "sentiment": sentiment,
        "priority": priority,
    }
