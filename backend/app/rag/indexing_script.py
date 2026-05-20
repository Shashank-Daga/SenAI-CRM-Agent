#!/usr/bin/env python3
"""
RAG Indexing Script

Loads knowledge base markdown files, chunks them, generates embeddings,
and stores them in ChromaDB for semantic search.

Usage:
    python -m app.rag.indexing_script
    # or
    python app/rag/indexing_script.py
"""

import asyncio
import sys
from pathlib import Path

from app.rag.chunking_service import ChunkingService
from app.rag.chromadb_client import ChromaDBClient
from app.rag.embedding_service import EmbeddingService
from app.utils.logger import get_logger

logger = get_logger(__name__)


def load_knowledge_base_files() -> list[tuple[str, str]]:
    """Load all markdown files from knowledge_base directory."""
    kb_path = Path(__file__).resolve().parents[3] / "knowledge_base"

    if not kb_path.exists():
        logger.error("Knowledge base directory not found at %s", kb_path)
        return []

    files = list(kb_path.glob("*.md"))
    logger.info("Found %d knowledge base files in %s", len(files), kb_path)

    documents = []
    for file_path in sorted(files):
        try:
            text = file_path.read_text(encoding="utf-8")
            doc_name = file_path.stem
            documents.append((doc_name, text))
            logger.info("Loaded document: %s (%d chars)", doc_name, len(text))
        except Exception as exc:
            logger.error("Failed to load %s: %s", file_path, exc)

    return documents


def index_knowledge_base() -> None:
    """Main indexing function."""
    logger.info("=== Starting RAG Knowledge Base Indexing ===")

    # Load markdown files
    documents = load_knowledge_base_files()
    if not documents:
        logger.error("No documents loaded. Exiting.")
        return

    # Delete and recreate collection for fresh indexing
    ChromaDBClient.delete_collection()

    all_chunks = []
    all_chunk_texts = []
    all_embeddings = []
    all_metadata = []

    # Chunk and embed each document
    for doc_name, doc_text in documents:
        logger.info("Chunking document: %s", doc_name)
        chunks = ChunkingService.chunk_document(doc_name, doc_text)
        logger.info("  → Generated %d chunks", len(chunks))

        for chunk in chunks:
            chunk_dict = chunk.to_dict()
            all_chunks.append(chunk)
            all_chunk_texts.append(chunk.text)
            all_metadata.append(
                {
                    "chunk_id": chunk.chunk_id,
                    "source_doc": chunk.source_doc,
                    "section_title": chunk.section_title or "General",
                    "token_count": chunk.token_count,
                }
            )

    if not all_chunks:
        logger.warning("No chunks generated. Exiting.")
        return

    # Generate embeddings in batch
    logger.info("Generating embeddings for %d chunks", len(all_chunks))
    all_embeddings = EmbeddingService.embed_texts(all_chunk_texts)
    logger.info("Generated %d embeddings", len(all_embeddings))

    # Store in ChromaDB
    logger.info("Storing chunks in ChromaDB...")
    chunk_ids = [chunk.chunk_id for chunk in all_chunks]
    ChromaDBClient.add_documents(
        documents=all_chunk_texts,
        metadatas=all_metadata,
        ids=chunk_ids,
        embeddings=all_embeddings,
    )

    # Verify
    count = ChromaDBClient.count()
    logger.info("✓ Successfully indexed %d chunks", count)
    logger.info("=== RAG Indexing Complete ===")


if __name__ == "__main__":
    try:
        index_knowledge_base()
    except KeyboardInterrupt:
        logger.info("Indexing interrupted by user")
        sys.exit(0)
    except Exception as exc:
        logger.error("Indexing failed: %s", exc, exc_info=True)
        sys.exit(1)
