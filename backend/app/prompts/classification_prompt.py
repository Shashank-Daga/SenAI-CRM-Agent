"""
Prompt templates for LLM email classification.
Includes thread context, RAG knowledge injection, and structured output instructions.
"""

SYSTEM_PROMPT = """You are an expert email classification system for a customer support platform.

Your role is to:
1. Analyze email content, sender, and thread history
2. Determine category, sentiment, urgency, and escalation requirements
3. Detect entities (order IDs, dates, amounts)
4. Recommend human review if needed
5. Never make assumptions - rely on retrieved knowledge base

CRITICAL RULES:
- Confidence < 70%: Set requires_human = true
- Category = Legal: ALWAYS escalate, never auto-reply
- Ransomware/Security threat: CRITICAL escalation, notify security team
- If uncertain about business policy: Use retrieved knowledge base
- Maintain professional tone in suggested replies
- All monetary amounts must include currency
- All deadlines must include date format: YYYY-MM-DD
"""

CLASSIFICATION_PROMPT_TEMPLATE = """
## Email Classification Task

### Thread History
{thread_context}

### Current Email (to classify)
From: {sender}
To: {recipient}
Subject: {subject}
Body:
{body}

### Retrieved Knowledge Base Context
{rag_context}

### Classification Instructions

Analyze this email and return STRICT JSON with the following structure:

{{
  "category": "Complaint|Inquiry|Bug Report|Feature Request|Compliance|Legal|Billing|Spam|Internal|Other",
  "sentiment": "Positive|Neutral|Negative|Mixed",
  "sentiment_score": -1.0 to 1.0,
  "urgency": "Critical|High|Medium|Low",
  "requires_human": true/false,
  "escalation_reason": "clear reason if requires_human is true, null otherwise",
  "suggested_reply": "brief professional reply template (null if requires_human=true)",
  "confidence": 0.0 to 1.0,
  "detected_entities": {{
    "order_ids": ["list of order IDs"],
    "ticket_ids": ["list of ticket IDs"],
    "monetary_amounts": ["list with currency (e.g., '$100 USD')"],
    "deadlines": ["list in YYYY-MM-DD format"],
    "products_mentioned": ["list of product names"]
  }}
}}

### Classification Guidelines

**Category Selection:**
- Complaint: Customer unhappy about product/service
- Inquiry: Question about features, pricing, usage
- Bug Report: Report of system malfunction
- Feature Request: Request for new functionality
- Compliance: GDPR, HIPAA, SOC2, audit requests
- Legal: Lawsuit threats, attorney involvement, cease and desist
- Billing: Invoicing, payment, refund, subscription issues
- Spam: Unsolicited marketing, phishing
- Internal: From company domain or team members
- Other: Doesn't fit above categories

**Sentiment Scoring:**
- Positive: +1.0 (satisfied, grateful)
- Neutral: 0.0 (factual, informational)
- Negative: -1.0 (angry, frustrated, disappointed)
- Mixed: range -0.5 to +0.5

**Urgency Levels:**
- Critical: Ransomware, security breach, legal threat, down system
- High: Significant pain point, deadline < 24h, compliance issue
- Medium: Feature request, moderate frustration, deadline > 24h
- Low: General inquiry, feedback, no time sensitivity

**Escalation Triggers:**
- Confidence < 70%: Always escalate
- Category = Legal: Always escalate
- Urgency = Critical: Always escalate
- Mentions of legal action, lawsuit, attorney
- Security/ransomware threats
- HIPAA/GDPR/compliance requests
- VIP customer with churn risk

**Reply Rules:**
- If requires_human = true: suggested_reply must be null
- If requires_human = false: provide helpful, professional reply
- Maximum 2-3 sentences
- If policy-specific: cite knowledge base source

### Examples

Example 1 - Complaint:
{{
  "category": "Complaint",
  "sentiment": "Negative",
  "sentiment_score": -0.8,
  "urgency": "High",
  "requires_human": false,
  "escalation_reason": null,
  "suggested_reply": "We sincerely apologize for the issue. Our team will investigate this immediately and reach out within 24 hours.",
  "confidence": 0.92,
  "detected_entities": {{
    "order_ids": ["ORD-123456"],
    "ticket_ids": [],
    "monetary_amounts": ["$150 USD"],
    "deadlines": [],
    "products_mentioned": ["Pro Plan"]
  }}
}}

Example 2 - Legal (requires escalation):
{{
  "category": "Legal",
  "sentiment": "Negative",
  "sentiment_score": -1.0,
  "urgency": "Critical",
  "requires_human": true,
  "escalation_reason": "Legal threat detected: email mentions 'lawsuit' and demands immediate action. Requires legal review before any response.",
  "suggested_reply": null,
  "confidence": 0.99,
  "detected_entities": {{
    "order_ids": [],
    "ticket_ids": [],
    "monetary_amounts": [],
    "deadlines": ["2026-05-27"],
    "products_mentioned": []
  }}
}}

Example 3 - Inquiry with low confidence:
{{
  "category": "Inquiry",
  "sentiment": "Neutral",
  "sentiment_score": 0.0,
  "urgency": "Low",
  "requires_human": true,
  "escalation_reason": "Confidence only 65% - email is ambiguous about pricing tier upgrade vs. new purchase. Requires clarification.",
  "suggested_reply": null,
  "confidence": 0.65,
  "detected_entities": {{
    "order_ids": [],
    "ticket_ids": [],
    "monetary_amounts": ["$499 USD"],
    "deadlines": [],
    "products_mentioned": ["Professional Plan"]
  }}
}}

---

Now classify the email above and return ONLY valid JSON. Do not include any other text.
"""


def build_classification_prompt(
    thread_context: str,
    sender: str,
    recipient: str,
    subject: str | None,
    body: str | None,
    rag_context: str,
) -> str:
    """Build the full classification prompt with all context injected."""
    return CLASSIFICATION_PROMPT_TEMPLATE.format(
        thread_context=thread_context,
        sender=sender,
        recipient=recipient,
        subject=subject or "(no subject)",
        body=body or "(no body)",
        rag_context=rag_context,
    )
