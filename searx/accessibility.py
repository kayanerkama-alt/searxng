# SPDX-License-Identifier: AGPL-3.0-or-later
"""Accessibility utilities for Atomic Search (WCAG 2.1 AA).

Provides helpers for:
- ARIA label generation
- Colour contrast checking
- Keyboard navigation metadata
- Screen-reader-friendly text formatting
- Focus management hints
"""
from __future__ import annotations

import math
import re
import logging
from typing import Any

logger = logging.getLogger('searx.accessibility')

# ---------------------------------------------------------------------------
# WCAG 2.1 colour contrast
# ---------------------------------------------------------------------------


def _linearize(c: float) -> float:
    """Convert an sRGB channel value [0, 1] to linear light."""
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(r: int, g: int, b: int) -> float:
    """Return the WCAG relative luminance of an RGB colour (0–255 each)."""
    rl = _linearize(r / 255)
    gl = _linearize(g / 255)
    bl = _linearize(b / 255)
    return 0.2126 * rl + 0.7152 * gl + 0.0722 * bl


def contrast_ratio(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    """Return the WCAG contrast ratio between two RGB colours.

    A ratio ≥ 4.5 satisfies AA for normal text; ≥ 3.0 for large text.
    """
    l1 = relative_luminance(*fg)
    l2 = relative_luminance(*bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def passes_aa(fg: tuple[int, int, int], bg: tuple[int, int, int], large_text: bool = False) -> bool:
    """Return True when the colour pair passes WCAG 2.1 AA contrast."""
    ratio = contrast_ratio(fg, bg)
    threshold = 3.0 if large_text else 4.5
    return ratio >= threshold


def passes_aaa(fg: tuple[int, int, int], bg: tuple[int, int, int], large_text: bool = False) -> bool:
    """Return True when the colour pair passes WCAG 2.1 AAA contrast."""
    ratio = contrast_ratio(fg, bg)
    threshold = 4.5 if large_text else 7.0
    return ratio >= threshold


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert a CSS hex colour string to an (R, G, B) tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b


# ---------------------------------------------------------------------------
# ARIA label helpers
# ---------------------------------------------------------------------------


def result_aria_label(result: dict[str, Any]) -> str:
    """Build a descriptive ARIA label for a search result article."""
    parts: list[str] = []

    title = result.get('title', '') or ''
    if title:
        # Strip HTML tags
        clean_title = re.sub(r'<[^>]+>', '', title)
        parts.append(clean_title)

    domain = ''
    parsed = result.get('parsed_url')
    if parsed:
        domain = getattr(parsed, 'netloc', '')
    if domain:
        parts.append(f'from {domain}')

    content_type = result.get('atomic_content_type', '')
    if content_type and content_type != 'Article':
        parts.append(content_type)

    freshness = result.get('atomic_freshness_label', '')
    if freshness:
        parts.append(freshness)

    reading_time = result.get('atomic_reading_time')
    if reading_time:
        parts.append(f'{reading_time} minute read')

    return ', '.join(parts)


def pagination_aria_label(page: int, is_current: bool = False) -> str:
    """Return an ARIA label for a pagination button."""
    if is_current:
        return f'Current page, page {page}'
    return f'Go to page {page}'


def search_input_aria_description(has_operators: bool, quick_action: str | None) -> str:
    """Return a dynamic ARIA description for the search input."""
    parts = ['Search query']
    if has_operators:
        parts.append('with advanced operators')
    if quick_action:
        action_labels = {
            'calculator': 'calculator expression detected',
            'unit_converter': 'unit conversion detected',
            'weather': 'weather query detected',
            'stocks': 'stock query detected',
            'definition': 'definition query detected',
            'time': 'time zone query detected',
            'currency': 'currency conversion detected',
        }
        label = action_labels.get(quick_action, f'{quick_action} detected')
        parts.append(label)
    return ', '.join(parts)


# ---------------------------------------------------------------------------
# Keyboard navigation metadata
# ---------------------------------------------------------------------------

# Hotkey definitions for screen-reader announcements
KEYBOARD_SHORTCUTS: dict[str, str] = {
    '/': 'Focus search box',
    'j': 'Next result',
    'k': 'Previous result',
    'o': 'Open selected result',
    'n': 'Next page',
    'p': 'Previous page',
    'Escape': 'Clear focus / close panel',
    '?': 'Show keyboard shortcuts',
}


def get_skip_links() -> list[dict[str, str]]:
    """Return skip-navigation link definitions for the page."""
    return [
        {'href': '#main_results', 'label': 'Skip to results'},
        {'href': '#search', 'label': 'Skip to search'},
        {'href': '#sidebar', 'label': 'Skip to sidebar'},
    ]


# ---------------------------------------------------------------------------
# Dyslexia-friendly text helpers
# ---------------------------------------------------------------------------

# OpenDyslexic and system fallbacks
DYSLEXIA_FONT_STACK = (
    '"OpenDyslexic", "Comic Sans MS", "Arial", sans-serif'
)


def dyslexia_css_vars() -> dict[str, str]:
    """Return CSS custom property overrides for dyslexia-friendly mode."""
    return {
        '--font-family': DYSLEXIA_FONT_STACK,
        '--line-height': '1.8',
        '--letter-spacing': '0.05em',
        '--word-spacing': '0.15em',
        '--paragraph-spacing': '1.5em',
    }


# ---------------------------------------------------------------------------
# Focus indicator helpers
# ---------------------------------------------------------------------------


def focus_ring_css(color: str = '#3050ff', width: int = 3, offset: int = 2) -> str:
    """Return a CSS ``outline`` shorthand for a visible focus ring."""
    return f'{width}px solid {color}'


def focus_ring_offset(offset: int = 2) -> str:
    """Return a CSS ``outline-offset`` value."""
    return f'{offset}px'


# ---------------------------------------------------------------------------
# Screen-reader text utilities
# ---------------------------------------------------------------------------


def sr_only_text(text: str) -> str:
    """Wrap *text* in a span that is visually hidden but readable by screen readers.

    The caller is responsible for ensuring the ``.sr-only`` CSS class is
    defined (it is included in the Atomic theme stylesheets).
    """
    return f'<span class="sr-only">{text}</span>'


def announce_result_count(count: int, query: str) -> str:
    """Return a screen-reader announcement string for result count."""
    if count == 0:
        return f'No results found for {query}'
    if count == 1:
        return f'1 result found for {query}'
    return f'{count} results found for {query}'
