""""""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlag
from . import PrimeValued


class MouseButton(PrimeValued):
  """Bitmask flags for mouse buttons, but with values as prime
  numbers. """
  LEFT = KeeFlag()
  RIGHT = KeeFlag()
  MIDDLE = KeeFlag()
