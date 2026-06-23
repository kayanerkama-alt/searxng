# SPDX-License-Identifier: AGPL-3.0-or-later
"""Implementations needed for a branding of Atomic Search."""
# pylint: disable=too-few-public-methods

# Struct fields aren't discovered in Python 3.14
# - https://github.com/searxng/searxng/issues/5284
from __future__ import annotations

__all__ = ["SettingsBrand"]

import msgspec


class BrandCustom(msgspec.Struct, kw_only=True, forbid_unknown_fields=True):
    """Custom settings in the brand section."""

    links: dict[str, str] = {}
    """Custom entries in the footer of the WEB page: ``[title]: [link]``"""


class ThemeColors(msgspec.Struct, kw_only=True, forbid_unknown_fields=True):
    """Custom settings for theme colors in the brand section."""

    theme_color_light: str = "#0066ff"
    background_color_light: str = "#ffffff"
    theme_color_dark: str = "#00d4ff"
    background_color_dark: str = "#0a0e27"
    theme_color_black: str = "#0066ff"
    background_color_black: str = "#000000"


class SettingsBrand(msgspec.Struct, kw_only=True, forbid_unknown_fields=True):
    """Options for configuring brand properties for Atomic Search.

    .. code:: yaml

       brand:
         issue_url: https://github.com/kayanerkama-alt/searxng/issues
         docs_url: https://atomic-search.dev/docs
         public_instances: https://atomic-search.dev/instances
         wiki_url: https://github.com/kayanerkama-alt/searxng/wiki

         custom:
           links:
             Privacy: https://atomic-search.dev/privacy
             About: https://atomic-search.dev/about
    """

    issue_url: str = "https://github.com/kayanerkama-alt/searxng/issues"
    """If you host your own issue tracker change this URL."""

    docs_url: str = "https://atomic-search.dev/docs"
    """If you host your own documentation change this URL."""

    public_instances: str = "https://atomic-search.dev/instances"
    """If you host your own instances page change this URL."""

    wiki_url: str = "https://github.com/kayanerkama-alt/searxng/wiki"
    """Link to your wiki (or ``false``)"""

    custom: BrandCustom = msgspec.field(default_factory=BrandCustom)
    """Optional customizing.

    .. autoclass:: searx.brand.BrandCustom
       :members:
    """

    pwa_colors: ThemeColors = msgspec.field(default_factory=ThemeColors)
    """Custom settings for PWA colors."""

    new_issue_url: str = "https://github.com/kayanerkama-alt/searxng/issues/new"
    """If you host your own issue tracker not on GitHub, then unset this URL.

    Note: This URL will create a pre-filled GitHub bug report form for an
    engine.  Since this feature is implemented only for GH (and limited to
    engines), it will probably be replaced by another solution in the near
    future.
    """

