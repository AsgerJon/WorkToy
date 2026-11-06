"""
Badge is the diamond listing the overloading branch first.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import Labelled, Fixed


class Badge(Labelled, Fixed):
  """
  A class listing the overloading branch first keeps what that branch
  inherits from the shared ancestor, although the plain branch stands
  between them in its own order: 'Badge().scale(2)' reaches 'Figure'
  through 'Labelled'. The plain method of 'Fixed' takes no call the
  overloads refuse.
  """
