"""Unit tests for the gmail_cleanup.cleaner module."""

from __future__ import annotations

import pytest

from gmail_cleanup.cleaner import (
    DEFAULT_DELAYS,
    DEFAULT_QUERIES,
    build_query,
    build_queries,
)


class TestBuildQuery:
    """Tests for build_query()."""

    def test_year_delay(self):
        query = build_query("category:promotions in:inbox AND -in:starred older_than:", {"index": 0, "type": "year", "value": 1})
        assert query == "category:promotions in:inbox AND -in:starred older_than:1y"

    def test_month_delay(self):
        query = build_query("category:social older_than:", {"index": 0, "type": "month", "value": 6})
        assert query == "category:social older_than:6m"

    def test_day_delay(self):
        query = build_query("label:newsletter older_than:", {"index": 0, "type": "day", "value": 30})
        assert query == "label:newsletter older_than:30d"

    def test_invalid_delay_type(self):
        with pytest.raises(ValueError, match="Unsupported delay type"):
            build_query("test:", {"index": 0, "type": "century", "value": 1})

    def test_base_query_without_trailing_colon(self):
        query = build_query("from:example.com", {"index": 0, "type": "year", "value": 2})
        assert query == "from:example.com2y"


class TestBuildQueries:
    """Tests for build_queries()."""

    def test_default_queries(self):
        queries = build_queries()
        assert len(queries) == 1
        assert queries[0] == "category:promotions in:inbox AND -in:starred older_than:1y"

    def test_custom_queries(self):
        queries = build_queries(
            queries=[
                "category:promotions older_than:",
                "category:social older_than:",
            ],
            delays=[
                {"index": 0, "type": "year", "value": 1},
                {"index": 1, "type": "month", "value": 6},
            ],
        )
        assert queries == [
            "category:promotions older_than:1y",
            "category:social older_than:6m",
        ]

    def test_partial_delays(self):
        """Query without a matching delay should be returned as-is."""
        queries = build_queries(
            queries=["query_with_delay:", "query_without_delay"],
            delays=[{"index": 0, "type": "year", "value": 1}],
        )
        assert queries == [
            "query_with_delay:1y",
            "query_without_delay",
        ]

    def test_invalid_type_in_delay(self):
        with pytest.raises(ValueError):
            build_queries(
                queries=["test:"],
                delays=[{"index": 0, "type": "fortnight", "value": 1}],
            )

    def test_defaults_match_original_js(self):
        """Verify the default config matches the original JS behaviour."""
        queries = build_queries()
        assert len(queries) == len(DEFAULT_QUERIES)
        # Original JS: "category:promotions in:inbox AND -in:starred older_than:" + "1" + "y"
        expected = "category:promotions in:inbox AND -in:starred older_than:1y"
        assert queries[0] == expected


class TestCleanupResult:
    """Tests for CleanupResult dataclass."""

    def test_default_values(self):
        from gmail_cleanup.cleaner import CleanupResult
        r = CleanupResult()
        assert r.total_threads_removed == 0
        assert r.queries_executed == []
        assert r.dry_run is False

    def test_dry_run_flag(self):
        from gmail_cleanup.cleaner import CleanupResult
        r = CleanupResult(dry_run=True)
        assert r.dry_run is True
