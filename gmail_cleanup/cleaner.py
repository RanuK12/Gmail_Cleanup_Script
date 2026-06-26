"""
Core module for Gmail cleanup operations.

Port of the original Google Apps Script (gmail-cleanup.js) to Python,
using the Gmail API via google-auth and google-api-python-client.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


# Default queries matching the original JS behaviour
DEFAULT_QUERIES = [
    "category:promotions in:inbox AND -in:starred older_than:",
]

DEFAULT_DELAYS = [
    {"index": 0, "type": "year", "value": 1},
]

BATCH_LIMIT = 100
API_SLEEP_SECS = 1.0


@dataclass
class CleanupResult:
    """Result of a cleanup run."""
    total_threads_removed: int = 0
    queries_executed: list[str] = field(default_factory=list)
    dry_run: bool = False


def build_query(base_query: str, delay: dict) -> str:
    """Build the full Gmail search query from a base query and delay config.

    Args:
        base_query: The base query string (may include trailing 'older_than:').
        delay: Dict with 'index', 'type' ('year'|'month'|'day'), 'value'.

    Returns:
        Complete query string.

    Raises:
        ValueError: If delay type is not supported.
    """
    unit_char = {"year": "y", "month": "m", "day": "d"}.get(delay["type"])
    if unit_char is None:
        raise ValueError(f"Unsupported delay type: {delay['type']}")
    return f"{base_query}{delay['value']}{unit_char}"


def build_queries(
    queries: Optional[list[str]] = None,
    delays: Optional[list[dict]] = None,
) -> list[str]:
    """Build all queries from config arrays.

    Args:
        queries: List of base query strings. Defaults to DEFAULT_QUERIES.
        delays: List of delay configs. Defaults to DEFAULT_DELAYS.

    Returns:
        List of complete Gmail search queries.
    """
    if queries is None:
        queries = DEFAULT_QUERIES
    if delays is None:
        delays = DEFAULT_DELAYS

    delay_map = {d["index"]: d for d in delays}
    result = []

    for i, base in enumerate(queries):
        delay = delay_map.get(i)
        if delay:
            result.append(build_query(base, delay))
        else:
            # If no delay configured, use the base query as-is
            result.append(base)

    return result


def cleanup(
    service,
    queries: Optional[list[str]] = None,
    delays: Optional[list[dict]] = None,
    batch_limit: int = BATCH_LIMIT,
    dry_run: bool = False,
) -> CleanupResult:
    """Execute the Gmail cleanup process.

    Args:
        service: Authenticated Gmail API service resource.
        queries: List of base query strings.
        delays: List of delay configs.
        batch_limit: Max threads to process per API call.
        dry_run: If True, only log what would be done.

    Returns:
        CleanupResult with statistics.
    """
    result = CleanupResult(dry_run=dry_run)
    full_queries = build_queries(queries, delays)

    for query in full_queries:
        logger.info("Processing query: %s", query)
        result.queries_executed.append(query)
        processed = _process_query(service, query, batch_limit, dry_run)
        result.total_threads_removed += processed

    return result


def _process_query(
    service,
    query: str,
    batch_limit: int,
    dry_run: bool,
) -> int:
    """Process a single query, moving matching threads to trash.

    Args:
        service: Authenticated Gmail API service.
        query: Full Gmail search query.
        batch_limit: Max results per page.
        dry_run: If True, only log.

    Returns:
        Number of threads processed.
    """
    processed = 0
    page_token: Optional[str] = None

    while True:
        # List threads matching the query
        request_params = {
            "q": query,
            "maxResults": batch_limit,
        }
        if page_token:
            request_params["pageToken"] = page_token

        response = service.users().threads().list(
            userId="me", **request_params
        ).execute()

        threads = response.get("threads", [])
        if not threads:
            break

        thread_ids = [t["id"] for t in threads]

        if dry_run:
            logger.info(
                "[DRY-RUN] Would trash %d threads: %s",
                len(thread_ids),
                ", ".join(thread_ids[:5]),
            )
        else:
            # Trash in batch by modifying each thread
            for tid in thread_ids:
                service.users().threads().trash(userId="me", id=tid).execute()
            logger.info("Trashed %d threads", len(thread_ids))

        processed += len(thread_ids)

        # Pagination
        page_token = response.get("nextPageToken")
        if not page_token:
            break

        # Sleep to avoid hitting API rate limits
        time.sleep(API_SLEEP_SECS)

    return processed
