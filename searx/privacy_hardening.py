# SPDX-License-Identifier: AGPL-3.0-or-later
"""Privacy and security hardening for Atomic Search"""

import hashlib
import secrets
from typing import Dict, Any

def get_privacy_headers() -> Dict[str, str]:
    """Return privacy-focused HTTP headers"""
    return {
        # Prevent tracking
        'Referrer-Policy': 'no-referrer',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=(), payment=()',
        
        # Security
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        
        # Privacy
        'X-Permitted-Cross-Domain-Policies': 'none',
        'Cross-Origin-Opener-Policy': 'same-origin',
        'Cross-Origin-Embedder-Policy': 'require-corp',
        
        # Cache control
        'Cache-Control': 'public, max-age=3600',
        'Pragma': 'no-cache',
    }

def sanitize_query(query: str) -> str:
    """Remove potentially sensitive information from queries"""
    # Remove common PII patterns
    import re
    
    # Remove email addresses
    query = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[email]', query)
    
    # Remove phone numbers
    query = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[phone]', query)
    
    # Remove credit card patterns
    query = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '[card]', query)
    
    # Remove SSN patterns
    query = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[ssn]', query)
    
    return query

def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token"""
    return secrets.token_urlsafe(length)

def hash_ip_address(ip: str, salt: str = '') -> str:
    """Hash IP address for privacy while maintaining consistency"""
    combined = f"{ip}{salt}".encode()
    return hashlib.sha256(combined).hexdigest()[:16]

def get_privacy_config() -> Dict[str, Any]:
    """Return privacy configuration"""
    return {
        'enable_image_proxy': True,
        'enable_referrer_policy': True,
        'enable_csp': True,
        'sanitize_queries': True,
        'hash_ips': True,
        'disable_cookies': False,  # Some cookies needed for preferences
        'secure_cookies_only': True,
        'httponly_cookies': True,
        'samesite_cookies': 'Strict',
        'max_cookie_age': 31536000,  # 1 year
    }

def apply_privacy_headers(response) -> None:
    """Apply privacy headers to Flask response"""
    headers = get_privacy_headers()
    for header, value in headers.items():
        response.headers[header] = value

