"""Test lol"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.attributes import ConstantAttribute, VariableAttribute
import time


class Base:
  """LOL"""

  name = ConstantAttribute('LMAO')

  price = ConstantAttribute(77)

  clock = VariableAttribute(time.ctime())

  def __init__(self, *args, **kwargs) -> None:
    pass

  def __str__(self, *args, **kwargs) -> str:
    """String Representation"""
    return '%s has a price of: %s' % (self.name, self.price)

  def __repr__(self, ) -> str:
    """Code Representation"""
    return self.__str__()
