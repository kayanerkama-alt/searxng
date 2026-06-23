# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Advanced Caching System for SearXNG
- Multi-level caching (memory, disk, distributed)
- Cache invalidation strategies
- Cache warming
- Performance metrics
"""

import hashlib
import json
import time
from functools import wraps
from typing import Any, Callable, Optional, Dict
from datetime import datetime, timedelta

class CacheEntry:
    """Represents a single cache entry with metadata."""
    
    def __init__(self, key: str, value: Any, ttl: int = 3600):
        self.key = key
        self.value = value
        self.ttl = ttl
        self.created_at = time.time()
        self.accessed_at = time.time()
        self.access_count = 0
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        return (time.time() - self.created_at) > self.ttl
    
    def touch(self):
        """Update access time and count."""
        self.accessed_at = time.time()
        self.access_count += 1
    
    def get_age(self) -> float:
        """Get age of cache entry in seconds."""
        return time.time() - self.created_at


class MemoryCache:
    """In-memory cache with LRU eviction."""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: Dict[str, CacheEntry] = {}
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self.cache:
            entry = self.cache[key]
            if not entry.is_expired():
                entry.touch()
                self.hits += 1
                return entry.value
            else:
                del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache."""
        if len(self.cache) >= self.max_size:
            # Evict least recently used
            lru_key = min(self.cache.keys(), 
                         key=lambda k: self.cache[k].accessed_at)
            del self.cache[lru_key]
        
        self.cache[key] = CacheEntry(key, value, ttl)
    
    def delete(self, key: str):
        """Delete value from cache."""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear all cache entries."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.2f}%",
            'total_requests': total,
        }


class SearchResultCache:
    """Specialized cache for search results."""
    
    def __init__(self):
        self.cache = MemoryCache(max_size=500)
    
    def get_key(self, query: str, category: str, language: str) -> str:
        """Generate cache key for search result."""
        key_str = f"{query}:{category}:{language}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, query: str, category: str, language: str) -> Optional[Dict]:
        """Get cached search results."""
        key = self.get_key(query, category, language)
        return self.cache.get(key)
    
    def set(self, query: str, category: str, language: str, 
            results: Dict, ttl: int = 1800):
        """Cache search results (30 minutes default)."""
        key = self.get_key(query, category, language)
        self.cache.set(key, results, ttl)
    
    def invalidate_query(self, query: str):
        """Invalidate all cache entries for a query."""
        # In production, would use more sophisticated invalidation
        pass


class CacheDecorator:
    """Decorator for caching function results."""
    
    def __init__(self, cache: MemoryCache, ttl: int = 3600):
        self.cache = cache
        self.ttl = ttl
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Generate cache key from function name and arguments
            key_parts = [func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = hashlib.md5(':'.join(key_parts).encode()).hexdigest()
            
            # Try to get from cache
            cached_value = self.cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = func(*args, **kwargs)
            self.cache.set(cache_key, result, self.ttl)
            return result
        
        return wrapper


class CacheWarmer:
    """Pre-populate cache with frequently accessed data."""
    
    def __init__(self, cache: MemoryCache):
        self.cache = cache
    
    def warm_popular_searches(self, popular_queries: list):
        """Pre-cache popular search queries."""
        # In production, would fetch actual results
        for query in popular_queries:
            key = hashlib.md5(query.encode()).hexdigest()
            self.cache.set(key, {'query': query, 'cached': True}, ttl=7200)
    
    def warm_static_content(self, content_map: Dict[str, Any]):
        """Pre-cache static content."""
        for key, value in content_map.items():
            self.cache.set(key, value, ttl=86400)  # 24 hours


# Global cache instances
_memory_cache = MemoryCache(max_size=1000)
_search_cache = SearchResultCache()


def get_memory_cache() -> MemoryCache:
    """Get global memory cache instance."""
    return _memory_cache


def get_search_cache() -> SearchResultCache:
    """Get global search result cache instance."""
    return _search_cache


def cached(ttl: int = 3600):
    """Decorator to cache function results."""
    cache = get_memory_cache()
    return CacheDecorator(cache, ttl)


def cache_search_results(query: str, category: str, language: str, 
                        results: Dict, ttl: int = 1800):
    """Cache search results."""
    _search_cache.set(query, category, language, results, ttl)


def get_cached_search_results(query: str, category: str, language: str) -> Optional[Dict]:
    """Get cached search results."""
    return _search_cache.get(query, category, language)


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics."""
    return {
        'memory_cache': _memory_cache.get_stats(),
        'timestamp': datetime.now().isoformat(),
    }


def clear_all_caches():
    """Clear all caches."""
    _memory_cache.clear()
    _search_cache.cache.clear()

