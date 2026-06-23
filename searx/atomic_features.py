# SPDX-License-Identifier: AGPL-3.0-or-later
"""Advanced features for Atomic Search."""

from __future__ import annotations
from typing import Any, Optional
from datetime import datetime, timedelta
import json


class AdvancedSearchFilters:
    """Advanced search filtering capabilities."""
    
    # Supported date ranges
    DATE_RANGES = {
        'today': (datetime.now() - timedelta(days=1), datetime.now()),
        'week': (datetime.now() - timedelta(days=7), datetime.now()),
        'month': (datetime.now() - timedelta(days=30), datetime.now()),
        'year': (datetime.now() - timedelta(days=365), datetime.now()),
        'anytime': (None, None)
    }
    
    # Supported result types
    RESULT_TYPES = {
        'all', 'web', 'images', 'videos', 'news', 'maps', 'shopping'
    }
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'zh', 'ko',
        'ar', 'hi', 'tr', 'pl', 'nl', 'sv', 'no', 'da', 'fi', 'hu'
    }
    
    @staticmethod
    def apply_date_filter(results: list[dict], date_range: str) -> list[dict]:
        """Filter results by date range."""
        if date_range not in AdvancedSearchFilters.DATE_RANGES:
            return results
        
        start_date, end_date = AdvancedSearchFilters.DATE_RANGES[date_range]
        if start_date is None:
            return results
        
        filtered = []
        for result in results:
            if 'published_date' in result:
                try:
                    pub_date = datetime.fromisoformat(result['published_date'])
                    if start_date <= pub_date <= end_date:
                        filtered.append(result)
                except (ValueError, TypeError):
                    filtered.append(result)
            else:
                filtered.append(result)
        
        return filtered
    
    @staticmethod
    def apply_type_filter(results: list[dict], result_type: str) -> list[dict]:
        """Filter results by type."""
        if result_type == 'all' or result_type not in AdvancedSearchFilters.RESULT_TYPES:
            return results
        
        return [r for r in results if r.get('type') == result_type]
    
    @staticmethod
    def apply_language_filter(results: list[dict], language: str) -> list[dict]:
        """Filter results by language."""
        if language not in AdvancedSearchFilters.SUPPORTED_LANGUAGES:
            return results
        
        return [r for r in results if r.get('language') == language]


class QuickActions:
    """Quick action features for common queries."""
    
    @staticmethod
    def is_calculator_query(query: str) -> bool:
        """Check if query is a math expression."""
        import re
        return bool(re.match(r'^[\d\s+\-*/().]+$', query.strip()))
    
    @staticmethod
    def evaluate_math(expression: str) -> Optional[str]:
        """Safely evaluate math expression."""
        try:
            # Only allow safe operations
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                return None
            result = eval(expression, {"__builtins__": {}}, {})
            return str(result)
        except:
            return None
    
    @staticmethod
    def is_unit_conversion(query: str) -> bool:
        """Check if query is a unit conversion."""
        conversions = ['km to miles', 'kg to lbs', 'celsius to fahrenheit', 'inches to cm']
        return any(conv in query.lower() for conv in conversions)
    
    @staticmethod
    def is_currency_conversion(query: str) -> bool:
        """Check if query is currency conversion."""
        return 'to' in query.lower() and any(
            curr in query.upper() for curr in ['USD', 'EUR', 'GBP', 'JPY', 'INR']
        )
    
    @staticmethod
    def is_weather_query(query: str) -> bool:
        """Check if query is asking for weather."""
        weather_keywords = ['weather', 'temperature', 'forecast', 'rain', 'snow', 'wind']
        return any(kw in query.lower() for kw in weather_keywords)


class SearchSuggestions:
    """Provides search suggestions from multiple sources."""
    
    SUGGESTION_SOURCES = {
        'wikipedia': 'https://en.wikipedia.org/w/api.php',
        'duckduckgo': 'https://duckduckgo.com/ac/',
        'google': 'https://www.google.com/complete/search'
    }
    
    @staticmethod
    def get_suggestions(query: str, source: str = 'wikipedia') -> list[str]:
        """Get search suggestions."""
        # This would integrate with actual APIs
        # For now, return empty list
        return []


class AccessibilityFeatures:
    """Accessibility features for Atomic Search."""
    
    # Supported accessibility modes
    MODES = {
        'high_contrast': {
            'description': 'High contrast mode for better visibility',
            'colors': {
                'background': '#000000',
                'text': '#FFFFFF',
                'links': '#FFFF00'
            }
        },
        'large_text': {
            'description': 'Larger text for easier reading',
            'font_size_multiplier': 1.5
        },
        'dyslexia_font': {
            'description': 'Dyslexia-friendly font',
            'font_family': 'OpenDyslexic'
        },
        'reduced_motion': {
            'description': 'Reduce animations and transitions',
            'animations_enabled': False
        },
        'screen_reader': {
            'description': 'Optimized for screen readers',
            'aria_labels': True,
            'semantic_html': True
        }
    }
    
    @staticmethod
    def get_accessibility_config(mode: str) -> Optional[dict]:
        """Get accessibility configuration."""
        return AccessibilityFeatures.MODES.get(mode)


class SearchHistory:
    """Client-side search history management."""
    
    MAX_HISTORY_ITEMS = 100
    HISTORY_RETENTION_DAYS = 30
    
    @staticmethod
    def add_to_history(query: str, results_count: int) -> dict:
        """Add search to history."""
        return {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'results_count': results_count
        }
    
    @staticmethod
    def cleanup_old_history(history: list[dict], days: int = 30) -> list[dict]:
        """Remove old history entries."""
        cutoff = datetime.now() - timedelta(days=days)
        return [
            h for h in history
            if datetime.fromisoformat(h['timestamp']) > cutoff
        ]


class ResultEnhancements:
    """Enhancements for search results."""
    
    @staticmethod
    def add_metadata(result: dict) -> dict:
        """Add metadata to result."""
        result['metadata'] = {
            'domain': result.get('url', '').split('/')[2] if result.get('url') else '',
            'content_length': len(result.get('content', '')),
            'has_image': 'image' in result.get('type', '').lower(),
            'is_news': 'news' in result.get('type', '').lower()
        }
        return result
    
    @staticmethod
    def calculate_reliability_score(result: dict) -> float:
        """Calculate reliability score for result."""
        score = 0.5  # Base score
        
        # Boost for known reliable domains
        reliable_domains = {
            'wikipedia.org': 0.95,
            'github.com': 0.90,
            'stackoverflow.com': 0.85,
            'medium.com': 0.75
        }
        
        domain = result.get('metadata', {}).get('domain', '')
        for reliable_domain, boost in reliable_domains.items():
            if reliable_domain in domain:
                score = boost
                break
        
        return score
    
    @staticmethod
    def generate_preview(result: dict, max_length: int = 150) -> str:
        """Generate preview for result."""
        content = result.get('content', '')
        if len(content) > max_length:
            return content[:max_length].rsplit(' ', 1)[0] + '...'
        return content


class AtomicSearchConfig:
    """Configuration for Atomic Search features."""
    
    # Feature flags
    ENABLE_ADVANCED_FILTERS = True
    ENABLE_QUICK_ACTIONS = True
    ENABLE_SUGGESTIONS = True
    ENABLE_ACCESSIBILITY = True
    ENABLE_SEARCH_HISTORY = True
    ENABLE_RESULT_ENHANCEMENTS = True
    
    # Search history
    HISTORY_ENABLED = True
    HISTORY_LOCAL_ONLY = True  # Store only on client
    HISTORY_AUTO_DELETE_DAYS = 30
    
    # Quick actions
    CALCULATOR_ENABLED = True
    UNIT_CONVERTER_ENABLED = True
    CURRENCY_CONVERTER_ENABLED = True
    WEATHER_ENABLED = True
    
    # Suggestions
    SUGGESTION_SOURCES = ['wikipedia', 'duckduckgo']
    SUGGESTION_COUNT = 5
    
    # Accessibility
    DEFAULT_ACCESSIBILITY_MODE = None
    ACCESSIBILITY_MODES_ENABLED = True

