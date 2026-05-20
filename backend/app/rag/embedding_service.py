from sentence_transformers import SentenceTransformer

from app.utils.logger import get_logger

logger = get_logger(__name__)

# Using a lightweight, fast model optimized for semantic search
MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingService:
    """
    Wraps sentence-transformers for generating semantic embeddings.
    Uses all-MiniLM-L6-v2 for speed and 384-dimensional vectors.
    """

    _instance: SentenceTransformer | None = None

    @classmethod
    def get_model(cls) -> SentenceTransformer:
        if cls._instance is None:
            logger.info("Loading embedding model: %s", MODEL_NAME)
            cls._instance = SentenceTransformer(MODEL_NAME)
        return cls._instance

    @classmethod
    def embed_text(cls, text: str) -> list[float]:
        """
        Embed a single text into a 384-dimensional vector.
        """
        model = cls.get_model()
        embedding = model.encode(text, convert_to_numpy=False)
        return embedding.tolist() if hasattr(embedding, "tolist") else list(embedding)

    @classmethod
    def embed_texts(cls, texts: list[str]) -> list[list[float]]:
        """
        Embed multiple texts efficiently in batch.
        """
        model = cls.get_model()
        embeddings = model.encode(texts, convert_to_numpy=False)
        if len(embeddings) == 0:
            return []
        return [e.tolist() if hasattr(e, "tolist") else list(e) for e in embeddings]

    @classmethod
    def similarity(cls, embedding1: list[float], embedding2: list[float]) -> float:
        """
        Compute cosine similarity between two embeddings.
        Returns value in [0, 1].
        """
        import numpy as np

        arr1 = np.array(embedding1)
        arr2 = np.array(embedding2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(arr1, arr2) / (norm1 * norm2))
