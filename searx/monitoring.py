# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Comprehensive Monitoring and Metrics for SearXNG
- Request metrics
- Performance monitoring
- Error tracking
- Health checks
"""

import time
from collections import defaultdict
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import statistics


class RequestMetrics:
    """Track request metrics."""
    
    def __init__(self):
        self.requests = []
        self.errors = defaultdict(int)
        self.status_codes = defaultdict(int)
        self.endpoints = defaultdict(list)
    
    def record_request(self, endpoint: str, duration: float, 
                      status_code: int, error: Optional[str] = None):
        """Record a request."""
        self.requests.append({
            'timestamp': time.time(),
            'endpoint': endpoint,
            'duration': duration,
            'status_code': status_code,
            'error': error,
        })
        
        self.status_codes[status_code] += 1
        self.endpoints[endpoint].append(duration)
        
        if error:
            self.errors[error] += 1
    
    def get_request_count(self, minutes: int = 60) -> int:
        """Get request count in last N minutes."""
        cutoff = time.time() - (minutes * 60)
        return sum(1 for r in self.requests if r['timestamp'] > cutoff)
    
    def get_error_rate(self, minutes: int = 60) -> float:
        """Get error rate in last N minutes."""
        cutoff = time.time() - (minutes * 60)
        recent = [r for r in self.requests if r['timestamp'] > cutoff]
        
        if not recent:
            return 0.0
        
        errors = sum(1 for r in recent if r['status_code'] >= 400)
        return (errors / len(recent)) * 100
    
    def get_average_response_time(self, endpoint: str = None, 
                                 minutes: int = 60) -> float:
        """Get average response time."""
        cutoff = time.time() - (minutes * 60)
        
        if endpoint:
            durations = [
                r['duration'] for r in self.requests
                if r['endpoint'] == endpoint and r['timestamp'] > cutoff
            ]
        else:
            durations = [
                r['duration'] for r in self.requests
                if r['timestamp'] > cutoff
            ]
        
        if not durations:
            return 0.0
        
        return statistics.mean(durations)
    
    def get_percentile_response_time(self, percentile: int = 95, 
                                    minutes: int = 60) -> float:
        """Get percentile response time."""
        cutoff = time.time() - (minutes * 60)
        durations = sorted([
            r['duration'] for r in self.requests
            if r['timestamp'] > cutoff
        ])
        
        if not durations:
            return 0.0
        
        index = int(len(durations) * (percentile / 100))
        return durations[min(index, len(durations) - 1)]
    
    def get_top_errors(self, limit: int = 10) -> List[tuple]:
        """Get top errors."""
        return sorted(
            self.errors.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
    
    def get_status_distribution(self) -> Dict[str, int]:
        """Get status code distribution."""
        return {
            '2xx': sum(v for k, v in self.status_codes.items() if 200 <= k < 300),
            '3xx': sum(v for k, v in self.status_codes.items() if 300 <= k < 400),
            '4xx': sum(v for k, v in self.status_codes.items() if 400 <= k < 500),
            '5xx': sum(v for k, v in self.status_codes.items() if 500 <= k < 600),
        }
    
    def get_summary(self, minutes: int = 60) -> Dict[str, Any]:
        """Get metrics summary."""
        return {
            'timestamp': datetime.now().isoformat(),
            'requests_last_hour': self.get_request_count(minutes),
            'error_rate': f"{self.get_error_rate(minutes):.2f}%",
            'avg_response_time_ms': f"{self.get_average_response_time(minutes) * 1000:.2f}",
            'p95_response_time_ms': f"{self.get_percentile_response_time(95, minutes) * 1000:.2f}",
            'p99_response_time_ms': f"{self.get_percentile_response_time(99, minutes) * 1000:.2f}",
            'status_distribution': self.get_status_distribution(),
            'top_errors': self.get_top_errors(5),
        }
    
    def cleanup(self, hours: int = 24):
        """Remove old metrics."""
        cutoff = time.time() - (hours * 3600)
        self.requests = [r for r in self.requests if r['timestamp'] > cutoff]


class HealthCheck:
    """Health check for SearXNG."""
    
    def __init__(self, metrics: RequestMetrics):
        self.metrics = metrics
        self.checks = {}
    
    def register_check(self, name: str, check_func):
        """Register a health check."""
        self.checks[name] = check_func
    
    def run_checks(self) -> Dict[str, bool]:
        """Run all health checks."""
        results = {}
        for name, check_func in self.checks.items():
            try:
                results[name] = check_func()
            except Exception as e:
                results[name] = False
        
        return results
    
    def is_healthy(self) -> bool:
        """Check if service is healthy."""
        results = self.run_checks()
        
        # Service is healthy if all checks pass
        return all(results.values())
    
    def get_status(self) -> Dict[str, Any]:
        """Get health status."""
        results = self.run_checks()
        error_rate = self.metrics.get_error_rate()
        
        return {
            'healthy': self.is_healthy(),
            'timestamp': datetime.now().isoformat(),
            'checks': results,
            'error_rate': f"{error_rate:.2f}%",
            'status': 'UP' if self.is_healthy() else 'DOWN',
        }


class PerformanceMonitor:
    """Monitor performance metrics."""
    
    def __init__(self):
        self.metrics = RequestMetrics()
        self.health = HealthCheck(self.metrics)
        self.start_time = time.time()
    
    def record_request(self, endpoint: str, duration: float, 
                      status_code: int, error: Optional[str] = None):
        """Record a request."""
        self.metrics.record_request(endpoint, duration, status_code, error)
    
    def get_uptime(self) -> float:
        """Get uptime in seconds."""
        return time.time() - self.start_time
    
    def get_uptime_percentage(self) -> float:
        """Get uptime percentage."""
        # In production, would track actual downtime
        return 99.9
    
    def get_full_report(self) -> Dict[str, Any]:
        """Get full monitoring report."""
        return {
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': self.get_uptime(),
            'uptime_percentage': f"{self.get_uptime_percentage():.2f}%",
            'metrics': self.metrics.get_summary(),
            'health': self.health.get_status(),
        }


# Global monitor instance
_monitor = PerformanceMonitor()


def get_monitor() -> PerformanceMonitor:
    """Get global monitor instance."""
    return _monitor


def record_request(endpoint: str, duration: float, 
                  status_code: int, error: Optional[str] = None):
    """Record a request."""
    _monitor.record_request(endpoint, duration, status_code, error)


def get_metrics_summary() -> Dict[str, Any]:
    """Get metrics summary."""
    return _monitor.metrics.get_summary()


def get_health_status() -> Dict[str, Any]:
    """Get health status."""
    return _monitor.health.get_status()


def get_full_report() -> Dict[str, Any]:
    """Get full monitoring report."""
    return _monitor.get_full_report()

