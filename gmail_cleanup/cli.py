"""
Command-line interface for Gmail Cleanup Script.

Usage:
    gmail-cleanup [--dry-run] [--verbose]
    gmail-cleanup --help
"""

from __future__ import annotations

import argparse
import logging
import os
import sys

from . import __version__
from .cleaner import DEFAULT_DELAYS, DEFAULT_QUERIES, cleanup

logger = logging.getLogger(__name__)

# Paths where Google credentials might live
CREDENTIALS_PATHS = [
    os.path.expanduser("~/.credentials/gmail-cleanup.json"),
    os.path.expanduser("~/.gmail/credentials.json"),
    "credentials.json",
    "client_secret.json",
]

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def _get_credentials():
    """Try to load Google API credentials from common paths.

    Returns:
        Credentials object or None.
    """
    from google.auth import default as google_default
    from google.auth.exceptions import DefaultCredentialsError

    # Try application-default credentials first
    try:
        creds, project = google_default(scopes=SCOPES)
        logger.debug("Using ADC credentials (project=%s)", project)
        return creds
    except DefaultCredentialsError:
        pass

    # Try explicit credential files
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    for path in CREDENTIALS_PATHS:
        if os.path.exists(path):
            logger.debug("Found credentials at %s", path)
            creds = Credentials.from_authorized_user_file(path, SCOPES)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            if creds and creds.valid:
                return creds

    return None


def _get_service(creds):
    """Build an authenticated Gmail API service."""
    from googleapiclient.discovery import build

    return build("gmail", "v1", credentials=creds)


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="gmail-cleanup",
        description="Clean up your Gmail inbox automatically.",
        epilog="Powered by Ranuk IT Solutions | ranuk.dev",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate cleanup without actually deleting anything.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose/debug logging.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 = success).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Try to authenticate
    creds = _get_credentials()
    if creds is None:
        logger.error(
            "No Google API credentials found.\n"
            "Please set up authentication:\n"
            "  1. Go to https://console.cloud.google.com/apis/credentials\n"
            "  2. Create a desktop OAuth 2.0 client ID\n"
            "  3. Download as ~/.credentials/gmail-cleanup.json\n"
            "  Or set GOOGLE_APPLICATION_CREDENTIALS env var."
        )
        return 1

    service = _get_service(creds)

    logger.info(
        "Starting Gmail cleanup (dry_run=%s)...", args.dry_run
    )

    result = cleanup(service, dry_run=args.dry_run)

    logger.info(
        "Cleanup complete. Queries executed: %d, threads affected: %d%s",
        len(result.queries_executed),
        result.total_threads_removed,
        " (dry-run)" if args.dry_run else "",
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
