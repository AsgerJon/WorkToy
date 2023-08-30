"""WorkToy - Symbolics - MetaSym
The Symbolic classes rely on metaclasses for functionality. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.core import Bases
from worktoy.metaclass import AbstractMetaClass
from worktoy.symbolics import SYM

ic.configureOutput(includeContext=True)


class Test:
  """fuck"""

  def test(self) -> SYM:
    return SYM()


class MetaSym(AbstractMetaClass):
  """WorkToy - Symbolics - MetaSym
  The Symbolic classes rely on metaclasses for functionality. """

  @classmethod
  def __prepare__(mcls, name, bases, **kwargs) -> dict:
    """Implementing the nameSpace generation"""
    return {'Test': getattr(Test, 'test')}

  def __new__(mcls, name: str, bases: Bases, nameSpace: dict, **kw) -> type:
    return super().__new__(mcls, name, bases, nameSpace, **kw)

  def __init__(cls, name: str, bases: Bases, nameSpace: dict, **kw) -> None:
    AbstractMetaClass.__init__(cls, name, bases, nameSpace, **kw)

  def __call__(cls, value: int = None) -> SYM:
    """This method returns an existing instance of SYM, instead of
    instantiating the Symbolic class."""
