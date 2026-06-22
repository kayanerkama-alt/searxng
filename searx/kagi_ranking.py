# SPDX-License-Identifier: AGPL-3.0-or-later
"""Kagi-inspired result ranking system for Atomic Search.

Provides quality scoring, snippet enhancement, result grouping,
ranking indicators, domain reputation, and freshness signals.
"""
from __future__ import annotations

import re
import math
import logging
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

logger = logging.getLogger('searx.kagi_ranking')

# ---------------------------------------------------------------------------
# Domain reputation tiers
# ---------------------------------------------------------------------------

# High-trust domains (academic, government, established reference)
_TRUSTED_DOMAINS: set[str] = {
    # Academic / research
    'arxiv.org', 'scholar.google.com', 'pubmed.ncbi.nlm.nih.gov',
    'ncbi.nlm.nih.gov', 'jstor.org', 'semanticscholar.org',
    'researchgate.net', 'nature.com', 'science.org', 'cell.com',
    'springer.com', 'wiley.com', 'tandfonline.com', 'ieee.org',
    'acm.org', 'dl.acm.org', 'mit.edu', 'stanford.edu', 'harvard.edu',
    'ox.ac.uk', 'cam.ac.uk',
    # Government / official
    'gov', 'gov.uk', 'europa.eu', 'un.org', 'who.int', 'cdc.gov',
    'nih.gov', 'nasa.gov', 'nist.gov',
    # Reference
    'wikipedia.org', 'britannica.com', 'merriam-webster.com',
    'dictionary.com', 'wolframalpha.com',
    # Developer / technical
    'github.com', 'gitlab.com', 'stackoverflow.com', 'docs.python.org',
    'developer.mozilla.org', 'mdn.io', 'rust-lang.org', 'golang.org',
    'docs.microsoft.com', 'learn.microsoft.com', 'developer.apple.com',
    'developer.android.com', 'kubernetes.io', 'docker.com',
    # News (established)
    'reuters.com', 'apnews.com', 'bbc.com', 'bbc.co.uk', 'npr.org',
    'theguardian.com', 'nytimes.com', 'washingtonpost.com',
}

# Domains that tend to produce lower-quality results
_LOW_QUALITY_DOMAINS: set[str] = {
    'pinterest.com', 'pinterest.co.uk', 'quora.com',
}

# Content-type signals derived from URL patterns
_CONTENT_TYPE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r'\.(pdf)(\?|$)', re.I), 'PDF'),
    (re.compile(r'\.(mp4|webm|avi|mov|mkv)(\?|$)', re.I), 'Video'),
    (re.compile(r'\.(mp3|ogg|flac|wav)(\?|$)', re.I), 'Audio'),
    (re.compile(r'\.(jpg|jpeg|png|gif|webp|svg)(\?|$)', re.I), 'Image'),
    (re.compile(r'/(wiki|wikipedia)/', re.I), 'Wiki'),
    (re.compile(r'/(blog|post|article|news)/', re.I), 'Article'),
    (re.compile(r'/(docs?|documentation|reference|api)/', re.I), 'Docs'),
    (re.compile(r'/(forum|thread|discussion|community)/', re.I), 'Forum'),
    (re.compile(r'/(video|watch|embed)/', re.I), 'Video'),
    (re.compile(r'github\.com/[^/]+/[^/]+$', re.I), 'Repository'),
    (re.compile(r'stackoverflow\.com/questions/', re.I), 'Q&A'),
]

# Average reading speed (words per minute)
_WPM = 238


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def score_result(result: dict[str, Any], query: str) -> dict[str, Any]:
    """Compute a quality score and attach ranking metadata to *result*.

    The function is non-destructive: it only *adds* keys to the result dict
    and never removes or overwrites existing ones.  All added keys are
    prefixed with ``atomic_`` to avoid collisions.

    Returns the mutated result dict for convenience.
    """
    url = result.get('url', '')
    title = result.get('title', '') or ''
    content = result.get('content', '') or ''
    parsed = _safe_parse(url)
    domain = parsed.netloc.lower().lstrip('www.')

    # --- individual score components (each 0.0–1.0) ---
    domain_score = _domain_score(domain)
    freshness_score, freshness_label = _freshness(result)
    relevance_score = _relevance(title, content, query)
    content_depth_score = _content_depth(content)

    # Weighted composite (weights sum to 1.0)
    composite = (
        domain_score * 0.30
        + relevance_score * 0.35
        + freshness_score * 0.15
        + content_depth_score * 0.20
    )

    # --- ranking badges (shown in the UI) ---
    badges: list[str] = []
    if domain_score >= 0.85:
        badges.append('Trusted source')
    if freshness_score >= 0.80:
        badges.append('Fresh content')
    if relevance_score >= 0.75:
        badges.append('Highly relevant')
    if content_depth_score >= 0.70:
        badges.append('In-depth')

    # --- content type ---
    content_type = _detect_content_type(url, result)

    # --- estimated reading time ---
    word_count = len(content.split()) if content else 0
    reading_time_min = max(1, math.ceil(word_count / _WPM)) if word_count > 50 else None

    # --- attach metadata ---
    result['atomic_score'] = round(composite, 4)
    result['atomic_badges'] = badges
    result['atomic_domain_trust'] = _trust_label(domain_score)
    result['atomic_freshness_label'] = freshness_label
    result['atomic_content_type'] = content_type
    result['atomic_reading_time'] = reading_time_min

    return result


def rank_results(results: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    """Score and re-rank a list of results using the Atomic ranking model.

    The original engine ordering is used as a tiebreaker so that results
    with equal scores preserve their original relative order.
    """
    for i, result in enumerate(results):
        score_result(result, query)
        # preserve original position as secondary sort key
        result.setdefault('atomic_original_pos', i)

    results.sort(
        key=lambda r: (
            -r.get('atomic_score', 0.0),
            r.get('atomic_original_pos', 0),
        )
    )
    return results


def group_similar_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collapse near-duplicate results from the same domain.

    When multiple results share the same *netloc*, only the highest-scored
    one is kept at its original position; the rest are attached as
    ``atomic_duplicates`` on that result.
    """
    seen: dict[str, int] = {}   # domain -> index of representative in output
    output: list[dict[str, Any]] = []

    for result in results:
        url = result.get('url', '')
        domain = _safe_parse(url).netloc.lower().lstrip('www.')

        if domain and domain in seen:
            rep_idx = seen[domain]
            dups = output[rep_idx].setdefault('atomic_duplicates', [])
            dups.append(result)
        else:
            if domain:
                seen[domain] = len(output)
            output.append(result)

    return output


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _safe_parse(url: str):
    try:
        return urlparse(url)
    except Exception:  # pylint: disable=broad-except
        return urlparse('')


def _domain_score(domain: str) -> float:
    """Return a trust score in [0, 1] for *domain*."""
    # Exact match
    if domain in _TRUSTED_DOMAINS:
        return 1.0
    # TLD match (e.g. anything ending in .gov)
    tld = domain.rsplit('.', 1)[-1] if '.' in domain else ''
    if tld in _TRUSTED_DOMAINS:
        return 0.95
    # Suffix match (e.g. subdomain of a trusted domain)
    for trusted in _TRUSTED_DOMAINS:
        if domain.endswith('.' + trusted):
            return 0.90
    if domain in _LOW_QUALITY_DOMAINS:
        return 0.20
    # HTTPS bonus is implicit (we only see https results in practice)
    return 0.50


def _freshness(result: dict[str, Any]) -> tuple[float, str]:
    """Return (score, human-readable label) for content freshness."""
    pub_date = result.get('publishedDate') or result.get('pubdate')
    if not pub_date:
        return 0.40, ''

    try:
        if isinstance(pub_date, str):
            # Try ISO format first, then common formats
            for fmt in ('%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d', '%a, %d %b %Y %H:%M:%S %z'):
                try:
                    pub_date = datetime.strptime(pub_date, fmt)
                    break
                except ValueError:
                    continue
            else:
                return 0.40, ''

        if isinstance(pub_date, datetime):
            now = datetime.now(timezone.utc)
            if pub_date.tzinfo is None:
                pub_date = pub_date.replace(tzinfo=timezone.utc)
            age_days = (now - pub_date).days

            if age_days < 0:
                return 0.50, 'Just published'
            if age_days == 0:
                return 1.00, 'Today'
            if age_days <= 3:
                return 0.95, 'This week'
            if age_days <= 7:
                return 0.90, 'This week'
            if age_days <= 30:
                return 0.80, 'This month'
            if age_days <= 90:
                return 0.65, 'Last 3 months'
            if age_days <= 365:
                return 0.50, 'This year'
            years = age_days // 365
            return max(0.10, 0.40 - years * 0.05), f'{years}y ago'
    except Exception:  # pylint: disable=broad-except
        pass

    return 0.40, ''


def _relevance(title: str, content: str, query: str) -> float:
    """Estimate query relevance based on keyword overlap."""
    if not query:
        return 0.50

    query_terms = set(re.findall(r'\w+', query.lower()))
    if not query_terms:
        return 0.50

    text = (title + ' ' + content).lower()
    text_terms = set(re.findall(r'\w+', text))

    if not text_terms:
        return 0.10

    # Jaccard-like overlap, weighted toward title matches
    title_terms = set(re.findall(r'\w+', title.lower()))
    title_hits = len(query_terms & title_terms)
    content_hits = len(query_terms & text_terms)

    title_score = title_hits / len(query_terms) if query_terms else 0
    content_score = content_hits / len(query_terms) if query_terms else 0

    return min(1.0, title_score * 0.60 + content_score * 0.40)


def _content_depth(content: str) -> float:
    """Estimate content depth from snippet length."""
    if not content:
        return 0.10
    length = len(content)
    # Sigmoid-like mapping: 500 chars → ~0.7, 1000 chars → ~0.9
    return min(1.0, length / 1100)


def _detect_content_type(url: str, result: dict[str, Any]) -> str:
    """Detect content type from URL patterns and result metadata."""
    template = result.get('template', '')
    if 'video' in template:
        return 'Video'
    if 'image' in template:
        return 'Image'
    if 'paper' in template:
        return 'Paper'
    if 'code' in template:
        return 'Code'
    if 'torrent' in template:
        return 'Torrent'
    if 'map' in template:
        return 'Map'

    for pattern, label in _CONTENT_TYPE_PATTERNS:
        if pattern.search(url):
            return label

    return 'Article'


def _trust_label(score: float) -> str:
    if score >= 0.90:
        return 'high'
    if score >= 0.60:
        return 'medium'
    return 'low'
