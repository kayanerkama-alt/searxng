# SPDX-License-Identifier: AGPL-3.0-or-later
"""Advanced search features for Atomic Search.

Provides search operator parsing, quick-action detection, and
client-side feature helpers (saved searches, shortcuts).
"""
from __future__ import annotations

import re
import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger('searx.advanced_features')

# ---------------------------------------------------------------------------
# Search operator parsing
# ---------------------------------------------------------------------------

# Supported operators and their canonical names
_OPERATOR_RE = re.compile(
    r'(?P<op>site|filetype|intitle|inurl|intext|before|after|lang|category)'
    r':(?P<val>"[^"]*"|\'[^\']*\'|\S+)',
    re.I,
)

_QUICK_ACTION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    # Calculator: "2 + 2", "sqrt(16)", "42 * 7"
    (re.compile(r'^[\d\s\+\-\*\/\(\)\.\^%]+$'), 'calculator'),
    # Unit conversion: "10 km to miles", "5 kg in lbs"
    (re.compile(r'\b\d+(\.\d+)?\s+\w+\s+(to|in)\s+\w+\b', re.I), 'unit_converter'),
    # Weather: "weather in London", "weather Paris"
    (re.compile(r'\bweather\b', re.I), 'weather'),
    # Stock ticker: "AAPL stock", "$TSLA"
    (re.compile(r'(\$[A-Z]{1,5}|\b[A-Z]{1,5}\s+stock\b)'), 'stocks'),
    # Define: "define serendipity", "what is entropy"
    (re.compile(r'^(define|what is|meaning of)\s+\w+', re.I), 'definition'),
    # Time: "time in Tokyo", "current time New York"
    (re.compile(r'\btime\s+in\b', re.I), 'time'),
    # Currency: "100 USD to EUR", "convert 50 GBP"
    (re.compile(r'\b\d+\s+[A-Z]{3}\s+(to|in)\s+[A-Z]{3}\b'), 'currency'),
]


@dataclass
class ParsedQuery:
    """Structured representation of a parsed search query."""

    raw: str
    clean: str = ''                          # query with operators stripped
    operators: dict[str, list[str]] = field(default_factory=dict)
    quick_action: str | None = None          # detected quick-action type
    has_operators: bool = False


def parse_query(raw_query: str) -> ParsedQuery:
    """Parse *raw_query* into a :class:`ParsedQuery`.

    Extracts structured operators (``site:``, ``filetype:``, etc.) and
    detects quick-action intent (calculator, weather, etc.).
    """
    pq = ParsedQuery(raw=raw_query)
    operators: dict[str, list[str]] = {}
    clean = raw_query

    for m in _OPERATOR_RE.finditer(raw_query):
        op = m.group('op').lower()
        val = m.group('val').strip('"\'')
        operators.setdefault(op, []).append(val)
        clean = clean.replace(m.group(0), '', 1)

    pq.operators = operators
    pq.has_operators = bool(operators)
    pq.clean = clean.strip()

    # Detect quick actions on the *clean* query
    for pattern, action in _QUICK_ACTION_PATTERNS:
        if pattern.search(pq.clean):
            pq.quick_action = action
            break

    return pq


def build_operator_filters(pq: ParsedQuery) -> dict[str, Any]:
    """Convert parsed operators into a filter dict for engine queries."""
    filters: dict[str, Any] = {}

    if 'site' in pq.operators:
        filters['site'] = pq.operators['site'][0]

    if 'filetype' in pq.operators:
        filters['filetype'] = pq.operators['filetype'][0].lstrip('.')

    if 'intitle' in pq.operators:
        filters['intitle'] = pq.operators['intitle']

    if 'inurl' in pq.operators:
        filters['inurl'] = pq.operators['inurl']

    if 'before' in pq.operators:
        filters['time_before'] = pq.operators['before'][0]

    if 'after' in pq.operators:
        filters['time_after'] = pq.operators['after'][0]

    if 'lang' in pq.operators:
        filters['language'] = pq.operators['lang'][0]

    if 'category' in pq.operators:
        filters['category'] = pq.operators['category'][0]

    return filters


# ---------------------------------------------------------------------------
# Custom search shortcuts
# ---------------------------------------------------------------------------

# Built-in shortcuts (user-extensible via preferences)
DEFAULT_SHORTCUTS: dict[str, str] = {
    'gh': 'site:github.com',
    'so': 'site:stackoverflow.com',
    'yt': 'site:youtube.com',
    'wp': 'site:wikipedia.org',
    'rd': 'site:reddit.com',
    'hn': 'site:news.ycombinator.com',
    'arxiv': 'site:arxiv.org',
    'pypi': 'site:pypi.org',
    'npm': 'site:npmjs.com',
    'mdn': 'site:developer.mozilla.org',
}


def expand_shortcuts(query: str, shortcuts: dict[str, str] | None = None) -> str:
    """Expand a leading shortcut token in *query*.

    Example: ``"gh searxng"`` → ``"site:github.com searxng"``
    """
    effective = {**DEFAULT_SHORTCUTS, **(shortcuts or {})}
    parts = query.split(None, 1)
    if not parts:
        return query
    token = parts[0].lower().rstrip(':')
    if token in effective:
        rest = parts[1] if len(parts) > 1 else ''
        return f'{effective[token]} {rest}'.strip()
    return query


# ---------------------------------------------------------------------------
# Search suggestion enrichment
# ---------------------------------------------------------------------------


def enrich_suggestions(suggestions: list[str], query: str) -> list[dict[str, str]]:
    """Attach metadata to raw suggestion strings.

    Returns a list of dicts with ``title`` and ``hint`` keys so the
    template can render richer suggestion chips.
    """
    enriched = []
    pq = parse_query(query)

    for suggestion in suggestions:
        hint = ''
        # If the suggestion adds an operator, label it
        if ':' in suggestion and not ':' in query:
            hint = 'operator'
        elif pq.quick_action:
            hint = pq.quick_action
        enriched.append({'title': suggestion, 'hint': hint})

    return enriched


# ---------------------------------------------------------------------------
# Advanced filter helpers (used by the UI)
# ---------------------------------------------------------------------------


def get_available_filters() -> dict[str, list[dict[str, str]]]:
    """Return the set of advanced filter options for the search UI."""
    return {
        'time_range': [
            {'value': '', 'label': 'Any time'},
            {'value': 'day', 'label': 'Past 24 hours'},
            {'value': 'week', 'label': 'Past week'},
            {'value': 'month', 'label': 'Past month'},
            {'value': 'year', 'label': 'Past year'},
        ],
        'content_type': [
            {'value': '', 'label': 'All types'},
            {'value': 'Article', 'label': 'Articles'},
            {'value': 'Video', 'label': 'Videos'},
            {'value': 'PDF', 'label': 'PDFs'},
            {'value': 'Image', 'label': 'Images'},
            {'value': 'Docs', 'label': 'Documentation'},
            {'value': 'Repository', 'label': 'Repositories'},
            {'value': 'Q&A', 'label': 'Q&A'},
        ],
        'safe_search': [
            {'value': '0', 'label': 'Off'},
            {'value': '1', 'label': 'Moderate'},
            {'value': '2', 'label': 'Strict'},
        ],
    }
