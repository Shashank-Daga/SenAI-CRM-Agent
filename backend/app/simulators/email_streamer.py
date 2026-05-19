import asyncio
import json
from pathlib import Path
from typing import Any

import httpx

from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def load_email_events(path: str) -> list[dict[str, Any]]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Email data file not found: {path}")
    with file_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


async def replay_email_stream(
    data_path: str,
    ingest_url: str,
    delay_seconds: float | None = None,
    batch_size: int = 1,
) -> None:
    delay = delay_seconds if delay_seconds is not None else settings.streamer_default_delay_seconds
    events = load_email_events(data_path)
    logger.info("Starting email replay simulator with %s events", len(events))

    async with httpx.AsyncClient(timeout=30.0) as client:
        for idx, event in enumerate(events, start=1):
            try:
                response = await client.post(ingest_url, json=event)
                if response.is_error:
                    logger.warning("[%s] ingest failed: %s", idx, response.text)
                else:
                    logger.info("[%s] ingest OK: %s", idx, response.json())
            except httpx.HTTPError as exc:
                logger.error("[%s] HTTP error while sending email event: %s", idx, exc)
            if idx % batch_size == 0:
                await asyncio.sleep(delay)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Replay email JSON into the ingest endpoint.")
    parser.add_argument(
        "--data",
        default=str(Path(__file__).resolve().parents[4] / "datasets" / "email-data-advanced.json"),
        help="Path to email JSON file.",
    )
    parser.add_argument("--url", default="http://localhost:8000/api/ingest", help="Ingest endpoint URL.")
    parser.add_argument("--delay", type=float, default=settings.streamer_default_delay_seconds, help="Seconds between batches.")
    parser.add_argument("--batch-size", type=int, default=1, help="Number of messages per batch before delay.")
    args = parser.parse_args()

    asyncio.run(replay_email_stream(args.data, args.url, args.delay, args.batch_size))
