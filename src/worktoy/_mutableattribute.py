"""WorkToy - Mutable Attribute
This module supports variable attributes for types that are not callables.
"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Never

from worktoy import AbstractAttribute


class MutableAttribute(AbstractAttribute):
  """WorkToy - Variable Attributes
  This module supports variable attributes for types that are not callables.
  """

  @abstractmethod
  def _typeCheck(self, value: object) -> bool:
    """Passed on from AbstractAttribute"""

  @abstractmethod
  def _typeGuard(self, value: object) -> object:
    """Passed on from AbstractAttribute"""

  def __init__(self, *args, **kwargs) -> None:
    AbstractAttribute.__init__(self, *args, **kwargs)

  def __set__(self, *_) -> Never:
    """Illegal setter"""
    raise self.AttributeException
