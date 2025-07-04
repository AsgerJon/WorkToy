"""
The 'worktoy.utilities.mathematics' module provides mathematical utilities
used across the 'worktoy' library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ._constants import e, pi, log, exp
from ._trig import sin, cos, tan
from ._fft import fft
from ._ifft import ifft
from ._product import product
from ._factorial import factorial

__all__ = [
    'product',
    'e',
    'pi',
    'log',
    'exp',
    'sin',
    'cos',
    'tan',
    'fft',
    'ifft',
    'factorial',
]
