"""
Knowledge retrieval tools for agent.
"""

from typing import Any

from app.rag.retrieval_service import RAGRetrievalService
from app.tools.base import AgentTool
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SearchKnowledgeBaseTool(AgentTool):
    """Search RAG knowledge base for relevant policy information."""

    name = "search_knowledge_base"
    description = "Search knowledge base for pricing, SLA, compliance, or policy information. Returns top 3 matching chunks with sources."

    async def execute(self, query: str, limit: int = 3, **kwargs: Any) -> dict[str, Any]:
        """
        Search knowledge base.

        Args:
            query: Search query string
            limit: Number of results (default 3, max 5)

        Returns:
            Results with source documents and relevance scores
        """
        logger.info("Knowledge search: query='%s'", query)

        if not query or len(query.strip()) == 0:
            return self._format_result(False, None, "Query cannot be empty")

        limit = min(limit, 5)  # Cap at 5 results

        try:
            results = RAGRetrievalService.search(query=query, top_k=limit)

            formatted_results = [
                {
                    "text": r["text"][:300],  # Truncate for clarity
                    "source_doc": r["source_doc"],
                    "section_title": r["section_title"],
                    "similarity_score": round(r["similarity_score"], 3),
                }
                for r in results
            ]

            logger.info("Found %d knowledge base results", len(formatted_results))
            return self._format_result(True, {"results": formatted_results, "count": len(formatted_results)})

        except Exception as exc:
            logger.error("Knowledge base search failed: %s", exc)
            return self._format_result(False, None, f"Search failed: {str(exc)}")
