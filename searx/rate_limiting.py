# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Advanced Rate Limiting for SearXNG
- Per-IP rate limiting
- Per-user rate limiting
- Adaptive rate limiting based on load
- DDoS protection
"""

import time
from collections import defaultdict
from typing import Dict, Tuple, Optional
from datetime import datetime, timedelta
import hashlib


class RateLimitBucket:
    """Token bucket for rate limiting."""
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize rate limit bucket.
        
        Args:
            capacity: Maximum tokens in bucket
            refill_rate: Tokens per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()
    
    def refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.refill_rate
        )
        self.last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens."""
        self.refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def get_tokens(self) -> float:
        """Get current token count."""
        self.refill()
        return self.tokens


class RateLimiter:
    """Rate limiter for API requests."""
    
    def __init__(self, 
                 requests_per_minute: int = 60,
                 requests_per_hour: int = 1000,
                 burst_size: int = 10):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_minute: Max requests per minute
            requests_per_hour: Max requests per hour
            burst_size: Allow burst of N requests
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.burst_size = burst_size
        
        # Per-IP tracking
        self.ip_buckets: Dict[str, RateLimitBucket] = {}
        self.ip_hourly: Dict[str, list] = defaultdict(list)
        
        # Statistics
        self.total_requests = 0
        self.blocked_requests = 0
    
    def get_client_ip(self, request) -> str:
        """Extract client IP from request."""
        # Check for X-Forwarded-For header (proxy)
        if hasattr(request, 'headers'):
            forwarded = request.headers.get('X-Forwarded-For')
            if forwarded:
                return forwarded.split(',')[0].strip()
        
        # Fall back to remote address
        if hasattr(request, 'remote_addr'):
            return request.remote_addr
        
        return 'unknown'
    
    def is_rate_limited(self, client_ip: str) -> Tuple[bool, Optional[str]]:
        """
        Check if client is rate limited.
        
        Returns:
            (is_limited, reason)
        """
        self.total_requests += 1
        
        # Check per-minute limit
        if client_ip not in self.ip_buckets:
            self.ip_buckets[client_ip] = RateLimitBucket(
                capacity=self.burst_size,
                refill_rate=self.requests_per_minute / 60
            )
        
        bucket = self.ip_buckets[client_ip]
        if not bucket.consume(1):
            self.blocked_requests += 1
            return True, "Rate limit exceeded (per minute)"
        
        # Check per-hour limit
        now = time.time()
        hour_ago = now - 3600
        
        # Clean old entries
        self.ip_hourly[client_ip] = [
            t for t in self.ip_hourly[client_ip] if t > hour_ago
        ]
        
        if len(self.ip_hourly[client_ip]) >= self.requests_per_hour:
            self.blocked_requests += 1
            return True, "Rate limit exceeded (per hour)"
        
        self.ip_hourly[client_ip].append(now)
        return False, None
    
    def get_remaining_requests(self, client_ip: str) -> Dict[str, int]:
        """Get remaining requests for client."""
        bucket = self.ip_buckets.get(client_ip)
        minute_remaining = int(bucket.get_tokens()) if bucket else self.requests_per_minute
        
        hour_remaining = self.requests_per_hour - len(self.ip_hourly.get(client_ip, []))
        
        return {
            'per_minute': max(0, minute_remaining),
            'per_hour': max(0, hour_remaining),
        }
    
    def get_stats(self) -> Dict:
        """Get rate limiter statistics."""
        total = self.total_requests
        blocked_rate = (self.blocked_requests / total * 100) if total > 0 else 0
        
        return {
            'total_requests': total,
            'blocked_requests': self.blocked_requests,
            'blocked_rate': f"{blocked_rate:.2f}%",
            'active_ips': len(self.ip_buckets),
            'requests_per_minute': self.requests_per_minute,
            'requests_per_hour': self.requests_per_hour,
        }
    
    def reset_client(self, client_ip: str):
        """Reset rate limit for a client."""
        if client_ip in self.ip_buckets:
            del self.ip_buckets[client_ip]
        if client_ip in self.ip_hourly:
            del self.ip_hourly[client_ip]
    
    def reset_all(self):
        """Reset all rate limits."""
        self.ip_buckets.clear()
        self.ip_hourly.clear()
        self.total_requests = 0
        self.blocked_requests = 0


class AdaptiveRateLimiter(RateLimiter):
    """Rate limiter that adapts based on server load."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_history = []
        self.adaptive_limit = self.requests_per_minute
    
    def update_load(self, current_load: float):
        """Update server load and adjust limits."""
        self.load_history.append((time.time(), current_load))
        
        # Keep only last hour of data
        hour_ago = time.time() - 3600
        self.load_history = [
            (t, l) for t, l in self.load_history if t > hour_ago
        ]
        
        # Adjust limits based on load
        if current_load > 0.8:
            # High load: reduce limit by 20%
            self.adaptive_limit = int(self.requests_per_minute * 0.8)
        elif current_load > 0.6:
            # Medium load: reduce limit by 10%
            self.adaptive_limit = int(self.requests_per_minute * 0.9)
        else:
            # Low load: use normal limit
            self.adaptive_limit = self.requests_per_minute
    
    def get_average_load(self) -> float:
        """Get average server load."""
        if not self.load_history:
            return 0.0
        
        loads = [l for _, l in self.load_history]
        return sum(loads) / len(loads)


# Global rate limiter instance
_rate_limiter = RateLimiter(
    requests_per_minute=60,
    requests_per_hour=1000,
    burst_size=10
)


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance."""
    return _rate_limiter


def check_rate_limit(client_ip: str) -> Tuple[bool, Optional[str]]:
    """Check if client is rate limited."""
    return _rate_limiter.is_rate_limited(client_ip)


def get_rate_limit_stats() -> Dict:
    """Get rate limiter statistics."""
    return _rate_limiter.get_stats()


def reset_rate_limits():
    """Reset all rate limits."""
    _rate_limiter.reset_all()

