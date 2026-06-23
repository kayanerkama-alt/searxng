# SPDX-License-Identifier: AGPL-3.0-or-later
"""Privacy hardening for Atomic Search."""

from __future__ import annotations
import hashlib
import re
from typing import Any
from flask import Response


class PrivacyHardener:
    """Implements privacy-first features for Atomic Search."""

    # PII patterns to sanitize
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN = re.compile(r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b')
    SSN_PATTERN = re.compile(r'\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4}\b')
    CREDIT_CARD_PATTERN = re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b')

    @staticmethod
    def sanitize_query(query: str) -> str:
        """Remove PII from search queries."""
        # Remove email addresses
        query = PrivacyHardener.EMAIL_PATTERN.sub('[email]', query)
        # Remove phone numbers
        query = PrivacyHardener.PHONE_PATTERN.sub('[phone]', query)
        # Remove SSN
        query = PrivacyHardener.SSN_PATTERN.sub('[ssn]', query)
        # Remove credit card numbers
        query = PrivacyHardener.CREDIT_CARD_PATTERN.sub('[card]', query)
        return query

    @staticmethod
    def hash_ip(ip_address: str, salt: str = "atomic-search") -> str:
        """Hash IP address for anonymization."""
        return hashlib.sha256(f"{ip_address}{salt}".encode()).hexdigest()[:16]

    @staticmethod
    def add_privacy_headers(response: Response) -> Response:
        """Add privacy-focused security headers."""
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer policy - no referrer leakage
        response.headers['Referrer-Policy'] = 'no-referrer'
        
        # Permissions policy - block tracking APIs
        response.headers['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=(), '
            'payment=(), '
            'usb=(), '
            'magnetometer=(), '
            'gyroscope=(), '
            'accelerometer=()'
        )
        
        # Content Security Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        
        # HSTS - enforce HTTPS
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        # Disable DNS prefetch
        response.headers['X-DNS-Prefetch-Control'] = 'off'
        
        # Disable client-side caching of sensitive data
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response

    @staticmethod
    def set_secure_cookies(response: Response) -> Response:
        """Configure secure cookie settings."""
        # This is typically handled by Flask session config, but we ensure it here
        response.headers['Set-Cookie'] = (
            'Path=/; '
            'HttpOnly; '
            'Secure; '
            'SameSite=Strict'
        )
        return response


class PrivacyConfig:
    """Configuration for privacy features."""
    
    # Enable query sanitization
    SANITIZE_QUERIES = True
    
    # Enable IP anonymization
    ANONYMIZE_IPS = True
    
    # Enable privacy headers
    ADD_PRIVACY_HEADERS = True
    
    # Query sanitization level (0=none, 1=basic, 2=strict)
    SANITIZATION_LEVEL = 2
    
    # Log retention (days) - 0 = no logs
    LOG_RETENTION_DAYS = 0
    
    # Enable DNS over HTTPS
    DOH_ENABLED = True
    
    # Block tracking pixels
    BLOCK_TRACKING_PIXELS = True
    
    # Remove tracking parameters from URLs
    REMOVE_TRACKING_PARAMS = True
    
    # Tracking parameters to remove
    TRACKING_PARAMS = {
        'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
        'fbclid', 'gclid', 'msclkid', 'mc_cid', 'mc_eid',
        'pk_campaign', 'pk_kwd', 'pk_source', 'pk_medium',
        'ref', 'referrer', 'source'
    }


def remove_tracking_params(url: str) -> str:
    """Remove tracking parameters from URLs."""
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=True)
    
    # Remove tracking parameters
    filtered_params = {
        k: v for k, v in params.items()
        if k.lower() not in PrivacyConfig.TRACKING_PARAMS
    }
    
    # Reconstruct URL
    new_query = urlencode(filtered_params, doseq=True)
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

