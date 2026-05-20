import re
import uuid
from dataclasses import dataclass

import tiktoken

from app.utils.logger import get_logger

logger = get_logger(__name__)

# OpenAI's tokenizer
TOKENIZER = tiktoken.get_encoding("cl100k_base")

# Chunking parameters per requirements
CHUNK_TARGET_TOKENS = 400  # ~300-500 tokens
CHUNK_OVERLAP_TOKENS = 50
MIN_CHUNK_TOKENS = 50


@dataclass
class DocumentChunk:
    """Represents a chunk of text with metadata."""

    chunk_id: str
    source_doc: str
    section_title: str | None
    text: str
    start_token: int
    end_token: int
    token_count: int

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "source_doc": self.source_doc,
            "section_title": self.section_title,
            "text": self.text,
            "start_token": self.start_token,
            "end_token": self.end_token,
            "token_count": self.token_count,
        }


class ChunkingService:
    """
    Splits markdown documents into overlapping chunks with metadata preservation.
    - Chunk size: ~400 tokens (300-500 range)
    - Overlap: 50 tokens
    - Preserves section titles as metadata
    """

    @staticmethod
    def count_tokens(text: str) -> int:
        """Count tokens using tiktoken."""
        try:
            return len(TOKENIZER.encode(text))
        except Exception as exc:
            logger.warning("Token count fallback to character-based: %s", exc)
            return len(text) // 4  # rough approximation

    @staticmethod
    def extract_sections(markdown_text: str) -> list[tuple[str, str]]:
        """
        Extract sections from markdown.
        Returns list of (section_title, section_content) tuples.
        """
        sections = []
        lines = markdown_text.split("\n")
        current_section = "General"
        current_content = []

        for line in lines:
            if line.startswith("# "):
                if current_content:
                    section_text = "\n".join(current_content).strip()
                    if section_text:
                        sections.append((current_section, section_text))
                current_section = line[2:].strip()
                current_content = []
            elif line.startswith("## "):
                if current_content:
                    section_text = "\n".join(current_content).strip()
                    if section_text:
                        sections.append((current_section, section_text))
                current_section = line[3:].strip()
                current_content = []
            else:
                current_content.append(line)

        if current_content:
            section_text = "\n".join(current_content).strip()
            if section_text:
                sections.append((current_section, section_text))

        return sections

    @classmethod
    def chunk_document(cls, source_doc: str, markdown_text: str) -> list[DocumentChunk]:
        """
        Chunk a markdown document into overlapping chunks.
        Preserves section titles and metadata.
        """
        chunks: list[DocumentChunk] = []
        sections = cls.extract_sections(markdown_text)

        for section_title, section_text in sections:
            section_chunks = cls._chunk_section(source_doc, section_title, section_text)
            chunks.extend(section_chunks)

        logger.info("Chunked %s into %d chunks (source: %s)", source_doc, len(chunks), len(chunks))
        return chunks

    @classmethod
    def _chunk_section(cls, source_doc: str, section_title: str, section_text: str) -> list[DocumentChunk]:
        """Chunk a single section, maintaining overlap."""
        chunks = []
        tokens = TOKENIZER.encode(section_text)
        num_tokens = len(tokens)

        if num_tokens < MIN_CHUNK_TOKENS:
            if section_text.strip():
                chunk = DocumentChunk(
                    chunk_id=str(uuid.uuid4()),
                    source_doc=source_doc,
                    section_title=section_title,
                    text=section_text,
                    start_token=0,
                    end_token=num_tokens,
                    token_count=num_tokens,
                )
                chunks.append(chunk)
            return chunks

        start_idx = 0
        while start_idx < num_tokens:
            end_idx = min(start_idx + CHUNK_TARGET_TOKENS, num_tokens)
            chunk_tokens = tokens[start_idx:end_idx]
            chunk_text = TOKENIZER.decode(chunk_tokens)

            if chunk_text.strip():
                chunk = DocumentChunk(
                    chunk_id=str(uuid.uuid4()),
                    source_doc=source_doc,
                    section_title=section_title,
                    text=chunk_text,
                    start_token=start_idx,
                    end_token=end_idx,
                    token_count=len(chunk_tokens),
                )
                chunks.append(chunk)

            start_idx = end_idx - CHUNK_OVERLAP_TOKENS if end_idx < num_tokens else num_tokens

        return chunks
