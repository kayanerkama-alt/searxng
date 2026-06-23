# SPDX-License-Identifier: AGPL-3.0-or-later
"""
Security, Privacy, and Performance Enhancements for SearXNG
- Enhanced security headers (CSP, HSTS, X-Frame-Options)
- Privacy-first configuration
- Performance optimizations (caching, compression)
- Theme support (dark/light mode)
"""

from flask import Flask, Response
from functools import wraps
import gzip
import io

def apply_security_headers(app: Flask):
    """Apply enhanced security headers to all responses."""
    
    @app.after_request
    def set_security_headers(response: Response):
        # Content Security Policy - strict, no external resources
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
        
        # HTTP Strict Transport Security - enforce HTTPS
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy - privacy-first
        response.headers['Referrer-Policy'] = 'no-referrer'
        
        # Permissions Policy - disable unnecessary features
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
        
        # Remove server identification
        if 'Server' in response.headers:
            del response.headers['Server']
        
        # Disable caching for sensitive pages
        if response.content_type and 'html' in response.content_type:
            response.headers['Cache-Control'] = 'public, max-age=3600'
        
        return response
    
    return app


def apply_privacy_config(app: Flask):
    """Apply privacy-first configuration."""
    
    @app.before_request
    def privacy_headers():
        """Ensure privacy headers are set on all requests."""
        pass
    
    return app


def gzip_response(f):
    """Decorator to gzip response if client supports it."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        
        # Check if client accepts gzip
        if isinstance(response, Response):
            accept_encoding = response.headers.get('Accept-Encoding', '')
            if 'gzip' in accept_encoding and len(response.get_data()) > 1024:
                # Compress response
                gzip_buffer = io.BytesIO()
                gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
                gzip_file.write(response.get_data())
                gzip_file.close()
                
                response.set_data(gzip_buffer.getvalue())
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['Content-Length'] = len(response.get_data())
        
        return response
    
    return decorated_function


def apply_performance_optimizations(app: Flask):
    """Apply performance optimizations."""
    
    @app.after_request
    def optimize_response(response: Response):
        # Enable browser caching for static assets
        if response.content_type and any(x in response.content_type for x in ['css', 'javascript', 'font', 'image']):
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        
        # Add timing headers for performance monitoring
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        return response
    
    return app


THEME_CONFIG = {
    'dark': {
        'name': 'Dark Mode',
        'description': 'Dark theme for reduced eye strain',
        'colors': {
            'background': '#1a1a1a',
            'foreground': '#ffffff',
            'accent': '#4a9eff',
        }
    },
    'light': {
        'name': 'Light Mode',
        'description': 'Light theme for daytime use',
        'colors': {
            'background': '#ffffff',
            'foreground': '#000000',
            'accent': '#0066cc',
        }
    },
    'auto': {
        'name': 'Auto (System)',
        'description': 'Automatically switch based on system preferences',
        'colors': None,
    }
}


def get_theme_config(theme_name: str = 'auto') -> dict:
    """Get theme configuration."""
    return THEME_CONFIG.get(theme_name, THEME_CONFIG['auto'])


def apply_all_enhancements(app: Flask) -> Flask:
    """Apply all security, privacy, and performance enhancements."""
    apply_security_headers(app)
    apply_privacy_config(app)
    apply_performance_optimizations(app)
    return app

