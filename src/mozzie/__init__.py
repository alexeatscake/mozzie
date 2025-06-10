"""
mozzie: This is a surrogate modelling package for GDSiMS.
"""

from __future__ import annotations

from importlib.metadata import version

__all__ = ("__version__", "generate")
__version__ = version(__name__)

from . import (
    generate,
)
