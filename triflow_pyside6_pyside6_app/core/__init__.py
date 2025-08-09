"""
Core package for the PySide6 version of TriFlow.

This package exposes common helpers for encryption, configuration,
models, and other shared functionality.  Currently it only
initialises the encryption utilities module.
"""

from . import utils  # noqa: F401  # re-export for convenience

__all__ = ["utils"]