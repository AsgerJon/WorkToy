"""
METACALL sentinel specifies that a class defers to the metaclass for the
class dunder hooks.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import Sentinel


class METACALL(Sentinel):
  pass
