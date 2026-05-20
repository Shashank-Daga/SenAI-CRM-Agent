from app.rag.chromadb_client import ChromaDBClient
from app.rag.embedding_service import EmbeddingService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class RAGRetrievalService:
    """
    High-level service for retrieving relevant knowledge base chunks.
    Handles embedding queries and similarity search against ChromaDB.
    """

    @staticmethod
    def search(query: str, top_k: int = 3) -> list[dict]:
        """
        Search knowledge base for relevant chunks.

        Args:
            query: Search query string
            top_k: Number of top results to return

        Returns:
            List of dicts with keys: text, source_doc, section_title, similarity_score
        """
        logger.info("RAG search query: %s (top_k=%d)", query, top_k)

        # Generate query embedding
        query_embedding = EmbeddingService.embed_text(query)

        # Search ChromaDB
        search_results = ChromaDBClient.search(query_text=query, query_embedding=query_embedding, limit=top_k)

        # Format results
        formatted_results = []
        for result in search_results:
            metadata = result["metadata"]
            formatted_results.append(
                {
                    "text": result["text"],
                    "source_doc": metadata.get("source_doc", "unknown"),
                    "section_title": metadata.get("section_title", "General"),
                    "similarity_score": result["similarity_score"],
                    "chunk_id": metadata.get("chunk_id", "unknown"),
                }
            )

        logger.info("RAG found %d results (scores: %s)", len(formatted_results), [r["similarity_score"] for r in formatted_results])

        return formatted_results

    @staticmethod
    def get_context_string(query: str, top_k: int = 3) -> str:
        """
        Get retrieval results as a formatted string for LLM injection.
        Useful for building prompt context.
        """
        results = RAGRetrievalService.search(query, top_k)

        if not results:
            return "No relevant knowledge base documents found."

        context_lines = ["Retrieved Knowledge Base Context:"]
        for idx, result in enumerate(results, 1):
            context_lines.append(f"\n--- Result {idx} (Score: {result['similarity_score']:.2f}) ---")
            context_lines.append(f"Source: {result['source_doc']} / {result['section_title']}")
            context_lines.append(f"Content: {result['text'][:500]}...")  # First 500 chars

        return "\n".join(context_lines)
