import os
from pathlib import Path

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.utils.logger import get_logger

logger = get_logger(__name__)


class ChromaDBClient:
    """
    Persistent ChromaDB client for vector storage and similarity search.
    Stores vectors in ./chroma_db/ directory.
    """

    _instance: chromadb.Client | None = None
    _collection = None

    @classmethod
    def get_client(cls) -> chromadb.Client:
        """Singleton pattern for ChromaDB client."""
        if cls._instance is None:
            db_path = Path(__file__).resolve().parents[3] / "chroma_db"
            os.makedirs(db_path, exist_ok=True)

            settings = ChromaSettings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=str(db_path),
                anonymized_telemetry=False,
            )

            logger.info("Initializing ChromaDB at %s", db_path)
            cls._instance = chromadb.Client(settings)

        return cls._instance

    @classmethod
    def get_or_create_collection(cls, collection_name: str = "knowledge_base") -> chromadb.Collection:
        """Get or create a collection for storing document chunks."""
        client = cls.get_client()
        try:
            collection = client.get_collection(name=collection_name, include=["embeddings", "documents", "metadatas"])
            logger.info("Retrieved existing collection: %s", collection_name)
        except Exception:
            collection = client.create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
            logger.info("Created new collection: %s", collection_name)

        return collection

    @classmethod
    def add_documents(cls, documents: list[str], metadatas: list[dict], ids: list[str], embeddings: list[list[float]] | None = None) -> None:
        """
        Add documents (chunks) to the collection.
        If embeddings provided, use them; otherwise ChromaDB will generate.
        """
        collection = cls.get_or_create_collection()

        if embeddings:
            collection.add(documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings)
        else:
            collection.add(documents=documents, metadatas=metadatas, ids=ids)

        logger.info("Added %d documents to knowledge base collection", len(documents))

    @classmethod
    def search(cls, query_text: str, query_embedding: list[float] | None = None, limit: int = 3) -> list[dict]:
        """
        Search for similar chunks.
        Returns list of (text, metadata, similarity_score).
        """
        collection = cls.get_or_create_collection()

        if query_embedding:
            results = collection.query(query_embeddings=[query_embedding], n_results=limit, include=["documents", "metadatas", "distances"])
        else:
            results = collection.query(query_texts=[query_text], n_results=limit, include=["documents", "metadatas", "distances"])

        if not results["documents"] or len(results["documents"]) == 0:
            return []

        docs = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        search_results = []
        for doc, metadata, distance in zip(docs, metadatas, distances):
            similarity_score = 1 - distance  # ChromaDB returns distances, convert to similarity
            search_results.append(
                {
                    "text": doc,
                    "metadata": metadata,
                    "similarity_score": max(0.0, min(1.0, similarity_score)),
                }
            )

        return search_results

    @classmethod
    def delete_collection(cls, collection_name: str = "knowledge_base") -> None:
        """Delete and recreate a collection (for re-indexing)."""
        client = cls.get_client()
        try:
            client.delete_collection(name=collection_name)
            logger.info("Deleted collection: %s", collection_name)
        except Exception as exc:
            logger.warning("Failed to delete collection %s: %s", collection_name, exc)

    @classmethod
    def count(cls) -> int:
        """Return total document count in collection."""
        collection = cls.get_or_create_collection()
        return collection.count()
