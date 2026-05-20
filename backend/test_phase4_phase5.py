#!/usr/bin/env python3
"""
Integration test script for PHASE 4 (RAG) and PHASE 5 (LLM Classification).

Tests:
1. RAG knowledge base indexing
2. RAG semantic search
3. Email classification (with fallback)
"""

import asyncio
import json
import sys
from pathlib import Path

from app.rag.embedding_service import EmbeddingService
from app.rag.chunking_service import ChunkingService
from app.rag.chromadb_client import ChromaDBClient
from app.rag.retrieval_service import RAGRetrievalService
from app.schemas.classification import EmailClassification
from app.utils.logger import get_logger

logger = get_logger(__name__)


def test_embedding_service():
    """Test 1: Embedding service."""
    logger.info("=== TEST 1: Embedding Service ===")
    
    texts = [
        "The pricing strategy focuses on three tiers: Starter at $99, Professional at $499, and Enterprise with custom pricing.",
        "SLA uptime guarantee is 99.5% for Professional plans and 99.95% for Enterprise plans.",
        "Refund policy allows 14-day money-back guarantee for all plans.",
    ]
    
    embeddings = EmbeddingService.embed_texts(texts)
    logger.info("✓ Generated %d embeddings of dimension %d", len(embeddings), len(embeddings[0]))
    
    # Test similarity
    query_text = "How much does the platform cost?"
    query_embedding = EmbeddingService.embed_text(query_text)
    
    similarities = []
    for i, emb in enumerate(embeddings):
        sim = EmbeddingService.similarity(query_embedding, emb)
        similarities.append((i, sim))
        logger.info("  Text %d: %.3f similarity", i, sim)
    
    return True


def test_chunking_service():
    """Test 2: Chunking service."""
    logger.info("=== TEST 2: Chunking Service ===")
    
    markdown_text = """# Pricing Policy

## Standard Pricing Tiers

### Starter Plan
- **Monthly Cost**: $99
- **Seats**: Up to 5 users
- **Storage**: 10 GB
- **Support**: Community forum

### Professional Plan
- **Monthly Cost**: $499
- **Seats**: Up to 25 users
- **Storage**: 100 GB
- **Support**: Email support (24-hour response)
- **SLA**: 99.5% uptime guarantee

### Enterprise Plan
- **Custom Pricing**: Starting at $2,000/month
- **Seats**: Unlimited
- **Storage**: Unlimited
- **Support**: 24/7 phone support
- **SLA**: 99.95% uptime guarantee
"""
    
    chunks = ChunkingService.chunk_document("pricing_policy", markdown_text)
    logger.info("✓ Generated %d chunks", len(chunks))
    
    for chunk in chunks[:2]:  # Show first 2
        logger.info("  Chunk %s: %d tokens, section='%s'", chunk.chunk_id, chunk.token_count, chunk.section_title)
    
    return True


def test_chromadb():
    """Test 3: ChromaDB storage and retrieval."""
    logger.info("=== TEST 3: ChromaDB Storage & Retrieval ===")
    
    test_docs = [
        "The Professional Plan costs $499/month for up to 25 users with 100GB storage and email support.",
        "The Enterprise Plan offers custom pricing with unlimited users, storage, and 24/7 support.",
        "Refunds are available within 14 days of purchase with no questions asked.",
    ]
    
    test_metadata = [
        {"source_doc": "pricing_policy", "section_title": "Professional Plan", "chunk_id": "chunk-1"},
        {"source_doc": "pricing_policy", "section_title": "Enterprise Plan", "chunk_id": "chunk-2"},
        {"source_doc": "refund_policy", "section_title": "14-Day Money-Back", "chunk_id": "chunk-3"},
    ]
    
    test_ids = ["test-chunk-1", "test-chunk-2", "test-chunk-3"]
    
    # Generate embeddings
    embeddings = EmbeddingService.embed_texts(test_docs)
    
    # Add to ChromaDB
    ChromaDBClient.add_documents(
        documents=test_docs,
        metadatas=test_metadata,
        ids=test_ids,
        embeddings=embeddings,
    )
    
    logger.info("✓ Stored %d test documents", len(test_docs))
    
    # Search
    results = ChromaDBClient.search(query_text="professional plan pricing", limit=2)
    logger.info("✓ Search returned %d results", len(results))
    
    for i, result in enumerate(results):
        logger.info("  Result %d: score=%.3f, source=%s", i + 1, result["similarity_score"], result["metadata"]["source_doc"])
    
    return True


def test_classification_schema():
    """Test 4: Classification schema validation."""
    logger.info("=== TEST 4: Classification Schema ===")
    
    sample_data = {
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
            "monetary_amounts": ["$150 USD"],
            "deadlines": [],
            "products_mentioned": ["Pro Plan"],
        },
    }
    
    classification = EmailClassification(**sample_data)
    logger.info("✓ Classification schema validated")
    logger.info("  Category: %s, Confidence: %.2f", classification.category, classification.confidence)
    logger.info("  Requires escalation: %s", classification.should_escalate())
    
    return True


def test_rag_retrieval():
    """Test 5: RAG retrieval service."""
    logger.info("=== TEST 5: RAG Retrieval Service ===")
    
    # This assumes indexing_script has been run
    query = "pricing tiers starter professional"
    results = RAGRetrievalService.search(query=query, top_k=2)
    
    logger.info("✓ RAG search returned %d results", len(results))
    
    if results:
        for i, result in enumerate(results):
            logger.info("  Result %d: score=%.3f, source=%s/%s", i + 1, result["similarity_score"], result["source_doc"], result["section_title"])
    else:
        logger.warning("  No results (knowledge base not indexed?)")
    
    return True


def main():
    """Run all tests."""
    logger.info("=== PHASE 4 & PHASE 5 Integration Tests ===\n")
    
    tests = [
        ("Embedding Service", test_embedding_service),
        ("Chunking Service", test_chunking_service),
        ("ChromaDB Storage", test_chromadb),
        ("Classification Schema", test_classification_schema),
        ("RAG Retrieval", test_rag_retrieval),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            logger.info("")
        except Exception as exc:
            logger.error("✗ %s FAILED: %s", name, exc, exc_info=True)
            failed += 1
            logger.info("")
    
    logger.info("=== Test Results ===")
    logger.info("Passed: %d", passed)
    logger.info("Failed: %d", failed)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
