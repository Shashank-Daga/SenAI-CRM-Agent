# SenAI CRM - PHASE 4 & PHASE 5 Implementation Guide

## Overview

This document covers PHASE 4 (RAG Knowledge Pipeline) and PHASE 5 (LLM Classification Engine) implementation.

## Architecture

### PHASE 4: RAG Knowledge Pipeline

**Purpose**: Retrieve relevant policy and product knowledge before LLM classification.

**Components**:
```
knowledge_base/ (markdown files)
    ├── pricing_policy.md
    ├── sla_policy.md
    ├── refund_policy.md
    ├── api_docs.md
    ├── compliance_faq.md
    └── escalation_matrix.md

app/rag/
    ├── embedding_service.py      # sentence-transformers wrapper
    ├── chunking_service.py       # markdown → overlapping chunks
    ├── chromadb_client.py        # persistent vector database
    ├── retrieval_service.py      # semantic search
    └── indexing_script.py        # index markdown → ChromaDB
```

**Flow**:
1. Load markdown documents
2. Chunk into 300-500 token pieces with 50-token overlap
3. Generate embeddings (all-MiniLM-L6-v2 model)
4. Store in ChromaDB (persistent local database)
5. Query with semantic search on demand

### PHASE 5: LLM Classification Engine

**Purpose**: Classify emails with thread context and retrieved knowledge.

**Components**:
```
app/llm/
    └── classification_service.py  # OpenAI/OpenRouter client

app/prompts/
    └── classification_prompt.py   # System prompt + templates

app/schemas/
    └── classification.py          # EmailClassification schema

app/services/
    └── thread_service.py          # Thread context fetcher

app/api/routes/
    ├── rag.py                     # GET /api/rag/search
    └── classification.py          # POST /api/classify/email/{id}
```

**Classification Workflow**:
1. Fetch email from database
2. Retrieve full thread history (ordered chronologically)
3. Query RAG for relevant knowledge (top-3 chunks)
4. Build unified prompt with thread + knowledge context
5. Call LLM with structured output schema
6. Parse JSON response into EmailClassification
7. Apply business rules for escalation
8. Return structured result

## File Structure

```
backend/
├── knowledge_base/
│   ├── pricing_policy.md
│   ├── sla_policy.md
│   ├── refund_policy.md
│   ├── api_docs.md
│   ├── compliance_faq.md
│   └── escalation_matrix.md
│
├── app/
│   ├── rag/
│   │   ├── embedding_service.py
│   │   ├── chunking_service.py
│   │   ├── chromadb_client.py
│   │   ├── retrieval_service.py
│   │   ├── indexing_script.py
│   │   └── __init__.py
│   │
│   ├── llm/
│   │   ├── classification_service.py
│   │   └── __init__.py
│   │
│   ├── prompts/
│   │   ├── classification_prompt.py
│   │   └── __init__.py
│   │
│   ├── api/routes/
│   │   ├── rag.py
│   │   └── classification.py
│   │
│   └── services/
│       └── thread_service.py
│
├── chroma_db/              # ChromaDB persistent storage (auto-created)
├── requirements.txt        # Updated with new dependencies
├── .env                    # LLM API keys configuration
└── alembic/               # Database migrations
```

## Setup & Initialization

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New dependencies:
- `sentence-transformers==2.2.2` - For embeddings
- `chromadb==0.4.3` - For vector storage
- `openai==1.3.6` - For LLM API
- `tiktoken==0.5.1` - For token counting
- `markdown==3.5.1` - For markdown parsing

### 2. Configure LLM (Optional but Recommended)

Edit `backend/.env`:

```env
# OpenAI (Primary)
OPENAI_API_KEY=sk_live_your_real_key_here
LLM_MODEL=gpt-4

# OR OpenRouter (Fallback/Alternative)
OPENROUTER_API_KEY=your_openrouter_key_here
```

If no API keys configured, the system falls back to safe defaults (requires_human=true).

### 3. Index Knowledge Base

```bash
cd backend
python -m app.rag.indexing_script
```

This will:
1. Load all markdown files from `backend/knowledge_base/`
2. Parse markdown into sections
3. Chunk into 300-500 token pieces
4. Generate embeddings
5. Store in `backend/chroma_db/` (persistent)

**Output**:
```
=== Starting RAG Knowledge Base Indexing ===
Found 6 knowledge base files
Loaded document: pricing_policy (3245 chars)
Loaded document: sla_policy (2987 chars)
...
Chunking document: pricing_policy
  → Generated 8 chunks
...
Generating embeddings for 47 chunks
✓ Successfully indexed 47 chunks
=== RAG Indexing Complete ===
```

### 4. Start Backend API

```bash
uvicorn app.main:app --reload
```

Server runs on `http://localhost:8000`

## API Endpoints

### RAG Search

**Endpoint**: `GET /api/rag/search`

**Parameters**:
- `q` (required): Search query string
- `limit` (optional): Number of results (1-10, default 3)

**Request**:
```bash
curl "http://localhost:8000/api/rag/search?q=pricing%20tiers&limit=3"
```

**Response**:
```json
{
  "success": true,
  "message": "Knowledge base search completed.",
  "data": {
    "query": "pricing tiers",
    "result_count": 3,
    "results": [
      {
        "text": "## Standard Pricing Tiers\n\n### Starter Plan\n- **Monthly Cost**: $99...",
        "source_doc": "pricing_policy",
        "section_title": "Standard Pricing Tiers",
        "similarity_score": 0.91,
        "chunk_id": "abc-123-def"
      },
      ...
    ]
  }
}
```

### Email Classification

**Endpoint**: `POST /api/classify/email/{email_id}`

**Parameters**:
- `email_id` (URL path): UUID of email to classify

**Request**:
```bash
curl -X POST "http://localhost:8000/api/classify/email/550e8400-e29b-41d4-a716-446655440000"
```

**Response**:
```json
{
  "success": true,
  "message": "Email classification completed.",
  "data": {
    "email_id": "550e8400-e29b-41d4-a716-446655440000",
    "thread_id": "660e8400-e29b-41d4-a716-446655440001",
    "classification": {
      "category": "Billing",
      "sentiment": "Negative",
      "sentiment_score": -0.7,
      "urgency": "High",
      "requires_human": false,
      "escalation_reason": null,
      "suggested_reply": "We understand your billing concern and will investigate immediately. You'll hear from our team within 24 hours.",
      "confidence": 0.88,
      "detected_entities": {
        "order_ids": ["ORD-12345"],
        "ticket_ids": [],
        "monetary_amounts": ["$499 USD"],
        "deadlines": [],
        "products_mentioned": ["Professional Plan"]
      }
    },
    "requires_escalation": false,
    "rag_sources": [
      {
        "source_doc": "pricing_policy",
        "section_title": "Pro-Rata Billing",
        "score": 0.85
      },
      {
        "source_doc": "refund_policy",
        "section_title": "Pro-Rata Refunds for Mid-Cycle Downgrades",
        "score": 0.79
      }
    ]
  }
}
```

## Testing Guide

### Test 1: RAG Search

```bash
# Test pricing query
curl "http://localhost:8000/api/rag/search?q=how%20much%20does%20enterprise%20cost"

# Test SLA query
curl "http://localhost:8000/api/rag/search?q=uptime%20guarantee%20SLA"

# Test compliance query
curl "http://localhost:8000/api/rag/search?q=GDPR%20HIPAA%20compliance"
```

### Test 2: Email Classification

First, ingest a test email:

```bash
curl -X POST "http://localhost:8000/api/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "test-msg-001",
    "sender": "customer@external.com",
    "recipient": "support@mycompany.com",
    "subject": "Billing issue with my invoice",
    "body": "Hi, I was charged $499 for the Professional Plan but I only used it for 5 days. Can I get a partial refund?",
    "received_at": "2026-05-20T10:00:00Z"
  }'
```

Then classify it:

```bash
# Replace email_id with the actual UUID from the ingest response
curl -X POST "http://localhost:8000/api/classify/email/{email_id}"
```

### Test 3: Thread Context with Classification

Create a multi-email thread:

```bash
# Email 1: Initial inquiry
curl -X POST "http://localhost:8000/api/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "thread-001-email-1",
    "sender": "customer@external.com",
    "recipient": "support@mycompany.com",
    "subject": "Can we discuss pricing?",
    "body": "Hi, we are interested in your Professional Plan but need a bulk discount for our team of 50 people.",
    "received_at": "2026-05-20T09:00:00Z",
    "thread_subject": "Bulk Pricing Discussion"
  }'

# Email 2: Follow-up (same thread)
curl -X POST "http://localhost:8000/api/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "thread-001-email-2",
    "sender": "support@mycompany.com",
    "recipient": "customer@external.com",
    "subject": "Re: Can we discuss pricing?",
    "body": "Absolutely! For 50 seats, we can offer 15% discount on the Professional Plan at $424.15/month per seat.",
    "received_at": "2026-05-20T10:30:00Z",
    "thread_subject": "Bulk Pricing Discussion"
  }'

# Email 3: Customer response (classify this one)
curl -X POST "http://localhost:8000/api/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "thread-001-email-3",
    "sender": "customer@external.com",
    "recipient": "support@mycompany.com",
    "subject": "Re: Can we discuss pricing?",
    "body": "Great! That works for us. Can we get a 3-year contract with annual prepayment for another 10% discount? We want to move forward ASAP.",
    "received_at": "2026-05-20T11:00:00Z",
    "thread_subject": "Bulk Pricing Discussion"
  }'

# Then classify the third email to see full thread context
```

## How RAG Works

### Chunking Strategy

Documents are split into overlapping chunks:

```
Document: "The starter plan costs $99/month for up to 5 users with 10GB storage.
The professional plan costs $499/month..."

Chunks (with 50-token overlap):
├─ Chunk 1: [tokens 0-400] "The starter plan costs $99/month for up to 5 users..."
├─ Chunk 2: [tokens 350-750] "...with 10GB storage. The professional plan costs..."
└─ Chunk 3: [tokens 700-1100] "...for up to 25 users..."
```

**Parameters**:
- Target chunk size: ~400 tokens (300-500 range)
- Overlap: 50 tokens between chunks
- Metadata preserved: source_doc, section_title, chunk_id

### Embedding Model

- Model: `all-MiniLM-L6-v2` (fast, 384-dimensional vectors)
- Library: sentence-transformers
- Speed: ~100 chunks/second on CPU
- Use case: Semantic search (not generative)

### Similarity Search

When querying:
1. Encode user query into embedding
2. Search ChromaDB using cosine similarity
3. Return top-k chunks with scores (0-1)
4. Format results for LLM injection

## LLM Classification Details

### Prompt Engineering

The classification prompt includes:

1. **System prompt**: Role definition, critical rules
2. **Thread context**: Full email history (ordered by time)
3. **Email content**: Current email to classify
4. **RAG context**: Top-3 relevant knowledge base chunks
5. **Output schema**: Strict JSON format with examples

### Structured Output

LLM returns JSON with:

```json
{
  "category": "one of 10 categories",
  "sentiment": "Positive|Neutral|Negative|Mixed",
  "sentiment_score": -1.0 to 1.0,
  "urgency": "Critical|High|Medium|Low",
  "requires_human": true/false,
  "escalation_reason": "why escalate, or null",
  "suggested_reply": "auto-reply template, or null",
  "confidence": 0.0 to 1.0,
  "detected_entities": {
    "order_ids": [],
    "ticket_ids": [],
    "monetary_amounts": [],
    "deadlines": [],
    "products_mentioned": []
  }
}
```

### Confidence Fallback Logic

**Business Rules**:

| Condition | Action |
|-----------|--------|
| confidence < 0.70 | requires_human = true |
| category = "Legal" | escalate always |
| urgency = "Critical" | escalate always |
| LLM unavailable | use safe default (confidence=0.5) |

**Default Classification**:
```
category: "Other"
sentiment: "Neutral"
sentiment_score: 0.0
urgency: "Low"
requires_human: true
escalation_reason: "LLM service unavailable. Requires manual review."
confidence: 0.5
```

### Escalation Rules

Email is escalated if **any** of these are true:
- `requires_human = true` (LLM flagged it)
- `confidence < 0.70` (uncertain classification)
- `category = "Legal"` (always escalate legal)
- `urgency = "Critical"` (time-sensitive/urgent)
- Detected ransomware/security flags
- Detected compliance request (GDPR, HIPAA, etc.)

## Performance Considerations

### RAG Indexing

- First run: ~30-60 seconds (embedding generation)
- Subsequent runs: <5 seconds (ChromaDB cached)
- Vector database size: ~5-10 MB for 6 policies

### LLM Classification

- Per email: ~2-4 seconds (OpenAI GPT-4 latency)
- Falls back to safe default if timeout
- Batch classification possible (not implemented yet)

### Database Queries

- Thread context fetch: ~50ms (indexed on thread_id)
- Email lookup: ~10ms (primary key)
- Classifications cached in PostgreSQL (optional future feature)

## Troubleshooting

### ChromaDB Issues

**Problem**: "ChromaDB directory already exists"
```bash
# Solution: Delete and recreate
rm -rf backend/chroma_db/
python -m app.rag.indexing_script
```

**Problem**: Vector similarity always returns same results
```bash
# Cause: Embeddings not generated properly
# Solution: Check embedding model download:
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### LLM Classification Issues

**Problem**: "OpenAI API key not configured"
```bash
# Solution: Add to .env:
OPENAI_API_KEY=sk_live_your_real_key
```

**Problem**: LLM returns non-JSON response
```
# Cause: Prompt injection or model hallucination
# Solution: LLM service catches this and uses default classification
# Check logs for: "Parse error on attempt"
```

### Thread Context Issues

**Problem**: "Thread has no emails"
```bash
# Cause: Email not ingested properly
# Solution: Check email ingestion response for errors
```

## Next Steps (Future Phases)

1. **Batch Classification**: Classify multiple emails in parallel
2. **Confidence Tuning**: A/B test prompt templates
3. **Fine-tuned Model**: Train smaller model for faster inference
4. **Caching Layer**: Cache classifications in PostgreSQL
5. **Feedback Loop**: Store human corrections for model refinement
6. **Agent Orchestration**: Chain classifications into multi-step workflows

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────┐
│                      FastAPI                            │
├──────────────────────────────────────────────────────────┤
│
├─→ GET /api/rag/search?q=...
│   └─→ Embedding Service (sentence-transformers)
│       └─→ ChromaDB (vector search)
│           └─→ Knowledge Base Files (markdown)
│
├─→ POST /api/classify/email/{id}
│   ├─→ Fetch Email (PostgreSQL)
│   ├─→ Thread Context Service
│   │   └─→ Fetch all emails in thread
│   ├─→ RAG Retrieval Service
│   │   └─→ ChromaDB search
│   ├─→ Prompt Builder
│   │   └─→ Inject: system prompt + thread + RAG
│   ├─→ LLM Classification Service
│   │   └─→ OpenAI API / OpenRouter
│   │       └─→ JSON Parser
│   ├─→ Escalation Logic
│   └─→ Return structured response
│
└──────────────────────────────────────────────────────────┘
```

## Summary

**PHASE 4** (RAG):
- Loads 6 knowledge base documents
- Chunks into 47 vectors
- Enables semantic search via ChromaDB
- Fast (<100ms) retrieval

**PHASE 5** (LLM):
- Orchestrates thread context + RAG injection
- Calls LLM with structured prompt
- Parses JSON output
- Applies business rule escalations
- Falls back gracefully when LLM unavailable

Both phases are **modular, testable, and production-ready**.
