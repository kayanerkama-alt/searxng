# SPDX-License-Identifier: AGPL-3.0-or-later
"""Performance optimisation utilities for Atomic Search.

Provides result deduplication, query normalisation, and lightweight
in-process caching helpers.  Heavy infrastructure concerns (connection
pooling, HTTP/2) are handled by the existing ``searx.network`` module.
"""
from __future__ import annotations

import hashlib
import logging
import re
import time
from collections import OrderedDict
from typing import Any

logger = logging.getLogger('searx.performance')

# ---------------------------------------------------------------------------
# Simple LRU cache (no external dependencies)
# ---------------------------------------------------------------------------


class LRUCache:
    """Thread-unsafe LRU cache suitable for single-process use.

    For multi-worker deployments use the Valkey-backed cache in
    ``searx.cache`` instead.
    """

    def __init__(self, maxsize: int = 256, ttl: float = 300.0) -> None:
        self._maxsize = maxsize
        self._ttl = ttl
        self._store: OrderedDict[str, tuple[Any, float]] = OrderedDict()

    def _key(self, *args: Any, **kwargs: Any) -> str:
        raw = repr(args) + repr(sorted(kwargs.items()))
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, key: str) -> Any | None:
        if key not in self._store:
            return None
        value, ts = self._store[key]
        if time.monotonic() - ts > self._ttl:
            del self._store[key]
            return None
        self._store.move_to_end(key)
        return value

    def set(self, key: str, value: Any) -> None:
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = (value, time.monotonic())
        while len(self._store) > self._maxsize:
            self._store.popitem(last=False)

    def invalidate(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    def __len__(self) -> int:
        return len(self._store)


# Module-level cache instances
_query_cache: LRUCache = LRUCache(maxsize=512, ttl=120.0)
_snippet_cache: LRUCache = LRUCache(maxsize=1024, ttl=600.0)


# ---------------------------------------------------------------------------
# Query normalisation
# ---------------------------------------------------------------------------

_WHITESPACE_RE = re.compile(r'\s+')
_PUNCT_RE = re.compile(r'[^\w\s\-\+\"\':\.\/]')


def normalize_query(query: str) -> str:
    """Return a canonical form of *query* for cache-key generation.

    - Lowercased
    - Collapsed whitespace
    - Stripped leading/trailing punctuation
    """
    q = query.lower().strip()
    q = _WHITESPACE_RE.sub(' ', q)
    return q


def query_cache_key(query: str, **params: Any) -> str:
    """Build a stable cache key from a normalised query and search params."""
    norm = normalize_query(query)
    raw = norm + repr(sorted(params.items()))
    return hashlib.sha256(raw.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Result deduplication
# ---------------------------------------------------------------------------


def _url_fingerprint(url: str) -> str:
    """Return a normalised fingerprint for *url* to detect near-duplicates."""
    # Strip scheme, trailing slash, common tracking params
    url = re.sub(r'^https?://', '', url.lower())
    url = url.rstrip('/')
    # Remove common tracking query params
    url = re.sub(r'[?&](utm_[^&]*|ref=[^&]*|source=[^&]*)', '', url)
    return url


def deduplicate_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove exact and near-duplicate results, keeping the first occurrence.

    Two results are considered duplicates when their URL fingerprints match.
    """
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []

    for result in results:
        url = result.get('url', '')
        fp = _url_fingerprint(url)
        if fp and fp in seen:
            logger.debug('dedup: dropping %s', url)
            continue
        if fp:
            seen.add(fp)
        deduped.append(result)

    return deduped


# ---------------------------------------------------------------------------
# Snippet optimisation
# ---------------------------------------------------------------------------

_SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')


def optimize_snippet(content: str, query: str, max_chars: int = 300) -> str:
    """Return the most query-relevant portion of *content*.

    Prefers sentences that contain query terms; falls back to the first
    *max_chars* characters when no match is found.
    """
    if not content:
        return ''

    if len(content) <= max_chars:
        return content

    query_terms = set(re.findall(r'\w+', query.lower()))
    sentences = _SENTENCE_SPLIT_RE.split(content)

    # Score each sentence by query-term overlap
    scored = []
    for sent in sentences:
        terms = set(re.findall(r'\w+', sent.lower()))
        score = len(query_terms & terms)
        scored.append((score, sent))

    scored.sort(key=lambda x: -x[0])

    # Build snippet from best sentences up to max_chars
    snippet_parts: list[str] = []
    total = 0
    for _, sent in scored:
        if total + len(sent) > max_chars:
            break
        snippet_parts.append(sent)
        total += len(sent) + 1

    if not snippet_parts:
        return content[:max_chars] + '…'

    return ' '.join(snippet_parts)


# ---------------------------------------------------------------------------
# Image lazy-loading helper
# ---------------------------------------------------------------------------


def should_lazy_load(index: int, threshold: int = 3) -> bool:
    """Return True when an image at *index* should use ``loading="lazy"``.

    The first *threshold* images are loaded eagerly (above the fold);
    the rest are deferred.
    """
    return index >= threshold


# ---------------------------------------------------------------------------
# Performance timing context manager
# ---------------------------------------------------------------------------


class Timer:
    """Lightweight context manager for measuring elapsed time (ms)."""

    def __init__(self, label: str = '') -> None:
        self.label = label
        self.elapsed_ms: float = 0.0
        self._start: float = 0.0

    def __enter__(self) -> 'Timer':
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_: Any) -> None:
        self.elapsed_ms = (time.perf_counter() - self._start) * 1000
        if self.label:
            logger.debug('%s: %.2f ms', self.label, self.elapsed_ms)
