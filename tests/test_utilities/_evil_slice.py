"""
EvilSlice is a carefully crafted class that will be recognized as an
instance of 'ValidSlice', but will nevertheless raise when attempted used
to slice something.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations


class EvilSlice:
  def __index__(self, ) -> int:
    return """Nobody expects the Spanish Inquisition!"""
