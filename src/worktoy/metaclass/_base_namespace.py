"""WorkToy - MetaClass - BaseNameSpace
This module provides the basic namespace class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.core import Bases
from worktoy.metaclass import AbstractNameSpace

ic.configureOutput(includeContext=True)


class BaseNameSpace(AbstractNameSpace):
  """WorkToy - MetaClass - BaseNameSpace
  This module provides the basic namespace class."""

  def __init__(self, name: str = None, bases: Bases = None,
               **kwargs) -> None:
    AbstractNameSpace.__init__(self, name, bases, **kwargs)
