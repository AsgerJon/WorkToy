"""
Inherits is a subclass of 'Count' without a hook of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import Count


class Inherits(Count):
  """
  A '__cast_as__' hook is looked up along the resolution order and bound
  to the class being cast to, so a subclass declaring none still builds
  itself. 'Inherits' declares nothing and relies on the hook of 'Count'.
  """
  pass
