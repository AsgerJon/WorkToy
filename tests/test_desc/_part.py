"""
Part is an 'Object' meant to be built by a box, so it carries the tags.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object


class Part(Object):
  """
  A value an 'AttriBox' builds is tagged with the box, the owner and
  the name when it is an 'Object', so it can ask the box for the
  instance of the access in progress and survive a pickle round trip
  naming its box. 'Part' is such a value, with nothing of its own.
  """
  pass
