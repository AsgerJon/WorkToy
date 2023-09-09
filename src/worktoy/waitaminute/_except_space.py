"""WorkToy - Wait A Minute! - ErrorNameSpace
Special namespace class for use with the metaclass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Keys, Items, Values, Bases
from worktoy.metaclass import AbstractNameSpace


class ExceptSpace(AbstractNameSpace):
  """WorkToy - Wait A Minute! - ErrorNameSpace
  Special namespace class for use with the metaclass."""

  def __init__(self, name: str, bases: tuple[type], **kwargs) -> None:
    AbstractNameSpace.__init__(self, name, bases, **kwargs)

  def getModuleName(self) -> str:
    """Getter-function for the module name"""
    return 'WorkToy - Wait A Minute!'
