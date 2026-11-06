"""
DESC sentinel provides a placeholder for the descriptor object in the
descriptor flow along with THIS and OWNER.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import Sentinel


class DESC(Sentinel):
  """
  An argument of an 'AttriBox', written in the class body, may need to be
  the box itself, which has no name the class body could use for it.

  Implementation
  --------------

  At the first read, an argument that is 'DESC' itself is replaced by the
  box building the value.
  """
