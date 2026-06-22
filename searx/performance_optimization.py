# SPDX-License-Identifier: AGPL-3.0-or-later
"""Performance optimization for Atomic Search"""

import time
from functools import wraps
from typing import Callable, Any, Dict
import logging

logger = logging.getLogger('searx.performance')

class PerformanceMonitor:
    """Monitor and log performance metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, list] = {}
    
    def record(self, name: str, duration: float) -> None:
        """Record a performance metric"""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(duration)
    
    def get_stats(self, name: str) -> Dict[str, float]:
        """Get statistics for a metric"""
        if name not in self.metrics or not self.metrics[name]:
            return {}
        
        times = self.metrics[name]
        return {
            'count': len(times),
            'min': min(times),
            'max': max(times),
            'avg': sum(times) / len(times),
            'total': sum(times),
        }
    
    def clear(self) -> None:
        """Clear all metrics"""
        self.metrics.clear()

# Global monitor instance
monitor = PerformanceMonitor()

def measure_performance(name: str) -> Callable:
    """Decorator to measure function performance"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.perf_counter() - start
                monitor.record(name, duration)
                if duration > 1.0:  # Log slow operations
                    logger.warning(f"{name} took {duration:.3f}s")
        return wrapper
    return decorator

def get_optimization_config() -> Dict[str, Any]:
    """Return performance optimization configuration"""
    return {
        # Caching
        'enable_result_cache': True,
        'cache_ttl': 3600,  # 1 hour
        'cache_max_size': 1000,
        
        # Compression
        'enable_gzip': True,
        'enable_brotli': True,
        'compression_level': 6,
        
        # Connection pooling
        'connection_pool_size': 100,
        'connection_pool_timeout': 30,
        
        # Request optimization
        'request_timeout': 5,
        'max_retries': 2,
        'enable_http2': True,
        
        # Database
        'enable_query_cache': True,
        'query_cache_ttl': 300,
        
        # Frontend
        'minify_css': True,
        'minify_js': True,
        'enable_lazy_loading': True,
        'enable_service_worker': True,
    }

def optimize_query(query: str) -> str:
    """Optimize search query for performance"""
    # Remove extra whitespace
    query = ' '.join(query.split())
    
    # Limit query length
    max_length = 500
    if len(query) > max_length:
        query = query[:max_length]
    
    return query

def get_performance_stats() -> Dict[str, Any]:
    """Get all performance statistics"""
    stats = {}
    for name in monitor.metrics.keys():
        stats[name] = monitor.get_stats(name)
    return stats

