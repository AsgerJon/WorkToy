"""WorkSide - Fields - DataSpace
Implementation of namespace class used by MetaData class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Bases
from worktoy.metaclass import AbstractNameSpace


class DataSpace(AbstractNameSpace):
  """WorkSide - Fields - DataSpace
  Implementation of namespace class used by MetaData class."""

  def __init__(self, mcls: type, name: str = None, bases: Bases = None,
               *args, **kwargs) -> None:
    AbstractNameSpace.__init__(self, name, bases, **kwargs)
    self._metaClass = mcls
