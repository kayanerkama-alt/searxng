"""
Atomic Search - Advanced Features Module
Includes: Spam Detection, Weather Integration, User Preferences
"""

import re
from urllib.parse import urlparse
from datetime import datetime
import json

class SpamDetector:
    """Detects and filters SEO spam and low-quality domains"""
    
    # Common spam patterns and domains
    SPAM_PATTERNS = [
        r'\.tk$',  # Free TK domains often spam
        r'\.ml$',  # Free ML domains often spam
        r'\.ga$',  # Free GA domains often spam
        r'\.cf$',  # Free CF domains often spam
        r'pinterest\.com',  # Often low-quality results
        r'pinterest\.co\.uk',
        r'quora\.com',  # Often low-quality answers
        r'reddit\.com/r/.*',  # Subreddit spam
        r'medium\.com',  # Often low-quality content
        r'linkedin\.com/pulse',  # LinkedIn spam articles
        r'facebook\.com',  # Social media spam
        r'instagram\.com',
        r'tiktok\.com',
        r'youtube\.com',  # Video spam
        r'amazon\.com/.*\?tag=',  # Affiliate spam
        r'ebay\.com',  # Auction spam
        r'aliexpress\.com',  # Dropship spam
        r'wish\.com',  # Dropship spam
        r'dhgate\.com',  # Dropship spam
    ]
    
    SPAM_KEYWORDS = [
        'click here',
        'buy now',
        'limited offer',
        'act now',
        'exclusive deal',
        'make money fast',
        'work from home',
        'free money',
        'guaranteed',
        'no credit card',
        'unbelievable',
        'too good to be true',
    ]
    
    @staticmethod
    def is_spam(url, title='', snippet=''):
        """Check if a result is likely spam"""
        try:
            domain = urlparse(url).netloc.lower()
            
            # Check domain patterns
            for pattern in SpamDetector.SPAM_PATTERNS:
                if re.search(pattern, domain):
                    return True
            
            # Check title and snippet for spam keywords
            text = (title + ' ' + snippet).lower()
            spam_count = sum(1 for keyword in SpamDetector.SPAM_KEYWORDS if keyword in text)
            
            if spam_count >= 2:
                return True
            
            return False
        except:
            return False
    
    @staticmethod
    def get_spam_score(url, title='', snippet=''):
        """Get a spam score from 0-100"""
        score = 0
        try:
            domain = urlparse(url).netloc.lower()
            
            # Domain patterns
            for pattern in SpamDetector.SPAM_PATTERNS:
                if re.search(pattern, domain):
                    score += 30
            
            # Keyword analysis
            text = (title + ' ' + snippet).lower()
            spam_count = sum(1 for keyword in SpamDetector.SPAM_KEYWORDS if keyword in text)
            score += spam_count * 15
            
            # URL length (very long URLs often spam)
            if len(url) > 200:
                score += 10
            
            # Excessive parameters
            if url.count('?') > 1 or url.count('&') > 5:
                score += 15
            
            return min(score, 100)
        except:
            return 0


class WeatherIntegration:
    """Integrates weather information into search results"""
    
    @staticmethod
    def extract_weather_query(query):
        """Check if query is weather-related"""
        weather_keywords = [
            'weather', 'temperature', 'forecast', 'rain', 'snow',
            'wind', 'humidity', 'celsius', 'fahrenheit', 'climate',
            'storm', 'sunny', 'cloudy', 'precipitation'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in weather_keywords)
    
    @staticmethod
    def get_weather_context(query):
        """Extract location from weather query"""
        # Simple location extraction
        location_patterns = [
            r'weather in (\w+)',
            r'(\w+) weather',
            r'forecast for (\w+)',
            r'(\w+) forecast',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None


class UserPreferences:
    """Manages user preferences and ranking"""
    
    @staticmethod
    def calculate_ranking_boost(domain, user_prefs):
        """Calculate ranking boost based on user preferences"""
        if not user_prefs or domain not in user_prefs:
            return 0
        
        pref = user_prefs[domain]
        clicks = pref.get('clicks', 0)
        last_click = pref.get('lastClick', 0)
        
        # Base boost from clicks
        boost = clicks * 10
        
        # Time decay (reduce boost after 7 days)
        if last_click:
            days_since = (datetime.now().timestamp() - last_click / 1000) / (24 * 3600)
            if days_since > 7:
                decay = max(0, days_since - 7) * 0.5
                boost -= decay
        
        return max(0, boost)
    
    @staticmethod
    def serialize_prefs(prefs):
        """Serialize preferences to JSON"""
        return json.dumps(prefs)
    
    @staticmethod
    def deserialize_prefs(prefs_json):
        """Deserialize preferences from JSON"""
        try:
            return json.loads(prefs_json)
        except:
            return {}


class ResultRanker:
    """Advanced result ranking system"""
    
    @staticmethod
    def calculate_score(result, user_prefs=None, spam_detector=True):
        """Calculate comprehensive score for a result"""
        score = 0
        
        try:
            url = result.get('url', '')
            title = result.get('title', '')
            snippet = result.get('content', '')
            domain = urlparse(url).netloc
            
            # Base score from search engine ranking
            score += 50
            
            # Spam penalty
            if spam_detector:
                spam_score = SpamDetector.get_spam_score(url, title, snippet)
                score -= spam_score * 0.5
            
            # User preference boost
            if user_prefs:
                boost = UserPreferences.calculate_ranking_boost(domain, user_prefs)
                score += boost
            
            # Quality signals
            # Prefer HTTPS
            if url.startswith('https://'):
                score += 5
            
            # Prefer shorter URLs
            if len(url) < 100:
                score += 3
            
            # Prefer established domains
            if domain.count('.') >= 2:
                score += 2
            
            return max(0, score)
        except:
            return 50
    
    @staticmethod
    def rerank_results(results, user_prefs=None):
        """Rerank results based on comprehensive scoring"""
        scored_results = []
        
        for result in results:
            score = ResultRanker.calculate_score(result, user_prefs)
            scored_results.append((score, result))
        
        # Sort by score descending
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        return [result for _, result in scored_results]

