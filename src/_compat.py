"""Python version compatibility shims.

Centralizes import fallbacks so individual modules don't each carry the
same try/except boilerplate. Currently provides ``tomllib`` (stdlib on
Python 3.11+, ``tomli`` backport on 3.10).
"""

from __future__ import annotations

try:
    import tomllib
except ImportError:  # Python 3.10
    import tomli as tomllib  # type: ignore[no-redef]

__all__ = ["tomllib"]
