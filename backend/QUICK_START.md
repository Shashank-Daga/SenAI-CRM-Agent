# PHASE 4 & PHASE 5 Quick Start

## What Was Built

### PHASE 4: RAG Knowledge Pipeline
- **6 markdown knowledge base documents** (pricing, SLA, refund, API, compliance, escalation)
- **Embedding service** using sentence-transformers (all-MiniLM-L6-v2)
- **Chunking service** with 300-500 token chunks + 50-token overlap
- **ChromaDB integration** for persistent vector storage
- **Indexing script** to process markdown → embeddings → vectors
- **RAG retrieval endpoint** (`GET /api/rag/search?q=...`)

### PHASE 5: LLM Classification Engine
- **Thread context service** to fetch full email history
- **LLM classification service** with OpenAI/OpenRouter support
- **Structured prompt templates** with system + user roles
- **Strict JSON schema** for classification output
- **Classification endpoint** (`POST /api/classify/email/{id}`)
- **Business rule escalation** logic
- **Confidence fallback** for LLM failures

## File Structure

```
backend/
├── knowledge_base/                 # Knowledge base docs
│   ├── pricing_policy.md
│   ├── sla_policy.md
│   ├── refund_policy.md
│   ├── api_docs.md
│   ├── compliance_faq.md
│   └── escalation_matrix.md
├── app/
│   ├── rag/                        # RAG components
│   │   ├── embedding_service.py
│   │   ├── chunking_service.py
│   │   ├── chromadb_client.py
│   │   ├── retrieval_service.py
│   │   ├── indexing_script.py
│   │   └── __init__.py
│   ├── llm/                        # LLM components
│   │   ├── classification_service.py
│   │   └── __init__.py
│   ├── prompts/                    # Prompt templates
│   │   ├── classification_prompt.py
│   │   └── __init__.py
│   ├── api/routes/
│   │   ├── rag.py                 # RAG endpoints
│   │   └── classification.py      # Classification endpoints
│   ├── services/
│   │   └── thread_service.py      # Thread context
│   ├── schemas/
│   │   └── classification.py      # Output schema
│   └── core/
│       └── config.py              # Updated with LLM keys
├── PHASE4_PHASE5_README.md         # Full documentation
├── test_phase4_phase5.py           # Integration tests
├── requirements.txt                # Updated dependencies
└── .env                            # LLM API keys
```

## Setup (3 Steps)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure LLM API (Optional)
Edit `backend/.env`:
```env
OPENAI_API_KEY=sk_live_your_key
LLM_MODEL=gpt-4
```

If no keys, system falls back to safe defaults (requires_human=true).

### 3. Index Knowledge Base
```bash
python -m app.rag.indexing_script
```

Expected output:
```
=== Starting RAG Knowledge Base Indexing ===
Found 6 knowledge base files
Loaded document: pricing_policy (3245 chars)
...
Generating embeddings for 47 chunks
✓ Successfully indexed 47 chunks
=== RAG Indexing Complete ===
```

## API Usage

### RAG Search
```bash
curl "http://localhost:8000/api/rag/search?q=how%20much%20does%20enterprise%20cost&limit=3"
```

### Classify Email
```bash
curl -X POST "http://localhost:8000/api/classify/email/550e8400-e29b-41d4-a716-446655440000"
```

## Classification Output Example

```json
{
  "success": true,
  "data": {
    "classification": {
      "category": "Billing",
      "sentiment": "Negative",
      "sentiment_score": -0.7,
      "urgency": "High",
      "requires_human": false,
      "suggested_reply": "We understand your concern and will investigate immediately...",
      "confidence": 0.88,
      "detected_entities": {
        "order_ids": ["ORD-12345"],
        "monetary_amounts": ["$499 USD"],
        "deadlines": ["2026-05-27"]
      }
    },
    "requires_escalation": false,
    "rag_sources": [
      {
        "source_doc": "billing_policy",
        "section_title": "Pro-Rata Billing",
        "score": 0.85
      }
    ]
  }
}
```

## Key Design Decisions

| Component | Choice | Why |
|-----------|--------|-----|
| Embeddings | all-MiniLM-L6-v2 | Fast (384-dim), semantic search optimized |
| Vector DB | ChromaDB | Persistent, local, no external service |
| Chunking | 400 tokens + 50-token overlap | Semantic coherence + context preservation |
| LLM | OpenAI GPT-4 primary | Reliable, supports structured output |
| Fallback | Safe default classification | Production reliability when LLM fails |
| Escalation | Multiple triggers | Confidence, category, urgency, security |

## Testing

Run integration tests:
```bash
python test_phase4_phase5.py
```

Tests cover:
1. Embedding generation
2. Document chunking
3. ChromaDB storage/retrieval
4. Schema validation
5. RAG search functionality

## Business Rules

**Escalation triggers** (any one):
- confidence < 0.70
- category = "Legal"
- urgency = "Critical"
- Detected ransomware/security threat
- Compliance request (GDPR, HIPAA)

**Never auto-reply if**:
- requires_human = true
- category = "Legal"
- urgency = "Critical"

## Architecture

```
Email arrives
    ↓
Ingest (PHASE 2) → Store in DB
    ↓
Classify endpoint receives email_id
    ↓
Fetch email + thread history
    ↓
RAG search for relevant knowledge
    ↓
Build unified prompt (system + thread + RAG + email)
    ↓
Call LLM with structured schema
    ↓
Parse JSON response
    ↓
Apply escalation business rules
    ↓
Return classification + escalation flag
```

## Performance

- RAG indexing: ~30-60s first run (embedding generation)
- RAG search: ~50-100ms (ChromaDB)
- LLM classification: ~2-4s (OpenAI latency)
- Thread context fetch: ~10-50ms (DB indexed)

## Production Readiness

✅ Modular architecture (clean separation of concerns)
✅ Type hints throughout
✅ Structured logging
✅ Error handling with fallbacks
✅ Async/await for I/O
✅ Schema validation (Pydantic)
✅ Comprehensive documentation
✅ Integration tests included

## Next Steps

1. **Batch Processing**: Classify multiple emails in parallel
2. **Caching**: Store classifications in PostgreSQL
3. **Fine-tuning**: Train smaller model for your domain
4. **Feedback Loop**: Human corrections → model refinement
5. **Batch Indexing**: Re-index knowledge base incrementally

## Support

See `PHASE4_PHASE5_README.md` for:
- Detailed architecture explanation
- Full API reference
- Testing guide
- Troubleshooting section
- Future phases roadmap
