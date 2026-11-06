"""
Item is an 'Object' meant to be built by a box.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object


class Item(Object):
  """
  A value an 'AttriBox' builds is tagged with the box, and can learn the
  instance it belongs to while the box is reading, through
  'getContextInstance'. 'Item' is such a value, with nothing of its own.
  """
  pass
