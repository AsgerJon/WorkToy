"""
Tag is the diamond listing the plain branch first.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import Labelled, Fixed


class Tag(Fixed, Labelled):
  """
  A class listing the plain branch first takes the plain method, as
  Python's lookup would: 'Tag' receives no dispatcher at 'scale', since
  'Fixed' hides every declaration behind it on the route of 'Tag'.
  """
