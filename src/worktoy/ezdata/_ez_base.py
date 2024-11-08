"""EZBase provides the base class for the EZData dataclasses. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZMeta


class EZBase(metaclass=EZMeta):
  """EZBase is the base class for EZData. """

  def __bool__(self, ) -> bool:
    return True
