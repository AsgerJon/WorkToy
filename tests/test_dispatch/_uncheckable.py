"""
Uncheckable is a class 'isinstance' refuses.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from . import UncheckableMeta


class Uncheckable(metaclass=UncheckableMeta):
  """
  The entry of a signature that 'validateTypes' must refuse as
  uncheckable: a proper class, so it passes the class check, whose
  metaclass raises 'TypeError' from every instance check.
  """
  pass
