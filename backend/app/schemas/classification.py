from typing import Optional

from pydantic import BaseModel, Field


class DetectedEntities(BaseModel):
    """Extracted entities from email."""

    order_ids: list[str] = Field(default_factory=list)
    ticket_ids: list[str] = Field(default_factory=list)
    monetary_amounts: list[str] = Field(default_factory=list)
    deadlines: list[str] = Field(default_factory=list)
    products_mentioned: list[str] = Field(default_factory=list)


class EmailClassification(BaseModel):
    """Strict schema for LLM classification output."""

    category: str = Field(
        ...,
        description="Email category",
        pattern="^(Complaint|Inquiry|Bug Report|Feature Request|Compliance|Legal|Billing|Spam|Internal|Other)$",
    )
    sentiment: str = Field(
        ...,
        description="Sentiment label",
        pattern="^(Positive|Neutral|Negative|Mixed)$",
    )
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="Sentiment score from -1 (negative) to 1 (positive)")
    urgency: str = Field(
        ...,
        description="Urgency level",
        pattern="^(Critical|High|Medium|Low)$",
    )
    requires_human: bool = Field(..., description="Whether email requires human review")
    escalation_reason: Optional[str] = Field(None, description="Reason for escalation if requires_human is true")
    suggested_reply: Optional[str] = Field(None, description="Suggested auto-reply template, null if requires_human=true")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    detected_entities: DetectedEntities = Field(default_factory=DetectedEntities)

    class Config:
        json_schema_extra = {
            "example": {
                "category": "Complaint",
                "sentiment": "Negative",
                "sentiment_score": -0.8,
                "urgency": "High",
                "requires_human": False,
                "escalation_reason": None,
                "suggested_reply": "We apologize for the issue and will investigate immediately.",
                "confidence": 0.92,
                "detected_entities": {
                    "order_ids": ["ORD-12345"],
                    "ticket_ids": [],
                    "monetary_amounts": ["$100 USD"],
                    "deadlines": [],
                    "products_mentioned": ["Pro Plan"],
                },
            }
        }

    def should_escalate(self) -> bool:
        """Determine if email should be escalated based on business rules."""
        if self.requires_human:
            return True
        if self.confidence < 0.70:
            return True
        if self.category == "Legal":
            return True
        if self.urgency == "Critical":
            return True
        return False
