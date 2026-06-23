# SPDX-License-Identifier: AGPL-3.0-or-later
"""Performance optimization for Atomic Search."""

from __future__ import annotations
import time
import hashlib
from typing import Any, Optional
from functools import wraps
from collections import OrderedDict


class PerformanceMonitor:
    """Monitors and optimizes performance."""
    
    def __init__(self):
        self.metrics = {}
        self.start_time = time.time()
    
    def record_metric(self, name: str, value: float, unit: str = "ms"):
        """Record a performance metric."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append({
            'value': value,
            'unit': unit,
            'timestamp': time.time()
        })
    
    def get_average(self, name: str) -> Optional[float]:
        """Get average value for a metric."""
        if name not in self.metrics or not self.metrics[name]:
            return None
        values = [m['value'] for m in self.metrics[name]]
        return sum(values) / len(values)
    
    def get_metrics_summary(self) -> dict[str, Any]:
        """Get summary of all metrics."""
        return {
            name: {
                'average': self.get_average(name),
                'count': len(values),
                'latest': values[-1]['value'] if values else None
            }
            for name, values in self.metrics.items()
        }


class ResultCache:
    """LRU cache for search results."""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl  # Time to live in seconds
        self.timestamps = {}
    
    def _make_key(self, query: str, params: dict) -> str:
        """Create cache key from query and parameters."""
        key_str = f"{query}:{str(sorted(params.items()))}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, query: str, params: dict) -> Optional[Any]:
        """Get cached result if available and not expired."""
        key = self._make_key(query, params)
        
        if key not in self.cache:
            return None
        
        # Check if expired
        if time.time() - self.timestamps[key] > self.ttl:
            del self.cache[key]
            del self.timestamps[key]
            return None
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def set(self, query: str, params: dict, result: Any):
        """Cache a result."""
        key = self._make_key(query, params)
        
        # Remove oldest if at capacity
        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]
        
        self.cache[key] = result
        self.timestamps[key] = time.time()
        self.cache.move_to_end(key)
    
    def clear(self):
        """Clear the cache."""
        self.cache.clear()
        self.timestamps.clear()


class QueryOptimizer:
    """Optimizes search queries for performance."""
    
    @staticmethod
    def optimize(query: str, max_length: int = 500) -> str:
        """Optimize query for faster processing."""
        # Remove extra whitespace
        query = ' '.join(query.split())
        
        # Limit query length
        if len(query) > max_length:
            query = query[:max_length]
        
        # Remove common stop words that don't affect search
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        words = query.split()
        optimized = [w for w in words if w.lower() not in stop_words or len(words) <= 2]
        
        return ' '.join(optimized)
    
    @staticmethod
    def deduplicate_results(results: list[dict]) -> list[dict]:
        """Remove duplicate results."""
        seen_urls = set()
        deduplicated = []
        
        for result in results:
            url = result.get('url', '')
            if url not in seen_urls:
                seen_urls.add(url)
                deduplicated.append(result)
        
        return deduplicated
    
    @staticmethod
    def optimize_snippets(snippet: str, max_length: int = 200) -> str:
        """Optimize snippet for display."""
        if len(snippet) > max_length:
            snippet = snippet[:max_length].rsplit(' ', 1)[0] + '...'
        return snippet


class CompressionOptimizer:
    """Handles compression optimization."""
    
    @staticmethod
    def should_compress(content_type: str) -> bool:
        """Determine if content should be compressed."""
        compressible_types = {
            'text/html',
            'text/css',
            'text/javascript',
            'application/javascript',
            'application/json',
            'text/xml',
            'application/xml',
            'text/plain'
        }
        return any(ct in content_type for ct in compressible_types)
    
    @staticmethod
    def get_compression_headers() -> dict[str, str]:
        """Get headers for compression support."""
        return {
            'Vary': 'Accept-Encoding',
            'Content-Encoding': 'gzip'
        }


class PerformanceConfig:
    """Configuration for performance optimization."""
    
    # Enable result caching
    ENABLE_CACHING = True
    
    # Cache size (number of results)
    CACHE_SIZE = 1000
    
    # Cache TTL (seconds)
    CACHE_TTL = 3600
    
    # Enable query optimization
    ENABLE_QUERY_OPTIMIZATION = True
    
    # Enable result deduplication
    ENABLE_DEDUPLICATION = True
    
    # Enable compression
    ENABLE_COMPRESSION = True
    
    # Maximum query length
    MAX_QUERY_LENGTH = 500
    
    # Maximum snippet length
    MAX_SNIPPET_LENGTH = 200
    
    # Enable lazy loading for images
    LAZY_LOAD_IMAGES = True
    
    # Enable service worker for offline support
    ENABLE_SERVICE_WORKER = True
    
    # Connection pool size
    CONNECTION_POOL_SIZE = 10
    
    # Request timeout (seconds)
    REQUEST_TIMEOUT = 10
    
    # Enable HTTP/2
    ENABLE_HTTP2 = True


def performance_timer(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        print(f"{func.__name__} took {elapsed:.2f}ms")
        return result
    return wrapper

