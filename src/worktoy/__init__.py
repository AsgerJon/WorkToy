"""The 'worktoy' package provides a collection of utilities leveraging
advanced python features including custom metaclasses and the descriptor
protocol. The readme file included provides detailed documentation on the
included features. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from . import desc, ezdata, keenum, meta, parse, text

__all__ = ['desc', 'ezdata', 'keenum', 'meta', 'parse', 'text']
