"""WorkToy - Immutable Attribute
This subclass of the abstract attribute provides setters"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import AbstractAttribute
from abc import abstractmethod


class ImmutableAttribute(AbstractAttribute):
  """WorkToy - Immutable Attribute
  This subclass of the abstract attribute provides setters"""

  def __init__(self, *args, **kwargs) -> None:
    AbstractAttribute.__init__(self, *args, **kwargs)

  @abstractmethod
  def _typeCheck(self, value: object) -> bool:
    """Passed on from AbstractAttribute"""

  @abstractmethod
  def _typeGuard(self, value: object) -> object:
    """Passed on from AbstractAttribute"""
