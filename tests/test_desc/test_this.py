"""TestTHIS tests if the special Zeroton classes THIS and TYPE are working
correctly. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any
from unittest import TestCase

from icecream import ic

from worktoy.desc import AttriBox, TYPE, THIS, Field
from worktoy.ezdata import EZData
from worktoy.meta import BaseObject
from worktoy.parse import maybe
from worktoy.text import typeMsg

ic.configureOutput(includeContext=True)


class Value(BaseObject):
  """Value encapsulates a class that expects the instance and owner of the
  class to be pass to the descriptor. """

  __owning_instance__ = None
  __owning_class__ = None
  __inner_value__ = None

  owner = Field()
  instance = Field()

  def __init__(self, cls: type, this: object, *args) -> None:
    if not isinstance(this, cls):
      e = typeMsg('this', this, cls)
      raise TypeError(e)
    self.__owning_instance__ = this
    self.__owning_class__ = cls
    if args:
      self.__inner_value__ = args[0]

  def __call__(self, *args, **kwargs) -> Any:
    return self.__inner_value__

  @owner.GET
  def _getOwner(self) -> object:
    return self.__owning_class__

  @instance.GET
  def _getInstance(self) -> object:
    return self.__owning_instance__


class Owner(BaseObject):
  """Space point"""

  x = AttriBox[Value](TYPE, THIS, 69)
  y = AttriBox[Value](TYPE, THIS, 420)
