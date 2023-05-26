"""FieldApply instances are used to decorate methods in the Field class as
well as in subclasses."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import NoReturn, Any

from worktoy.core import CallMeMaybe, TypeBag
from worktoy.field import Decorator
from worktoy.waitaminute import n00bError, ValidationError

Target = TypeBag(CallMeMaybe, type)


class FieldApply(Decorator):
  """Markers assign a single attribute to the target. """

  _count = 0

  @classmethod
  def _getCount(cls) -> int:
    """Getter-function for count of functions decorated"""
    return cls._count

  @classmethod
  def _incrementCount(cls) -> NoReturn:
    """Incrementor function for count"""
    cls._count += 1

  @classmethod
  def applicator(cls, priority: int = None) -> FieldApply:
    """Alias for instantiation call with value True"""
    return cls(priority)

  @staticmethod
  def _getKeyName() -> str:
    """Getter-function for keyName indicating decorated target."""
    return 'applyFlag'

  def __init__(self, value: Any, **kwargs) -> None:
    priority = kwargs.get('priority', None)
    self._value = value

  def decorate(self, target: Target) -> Target:
    """Decorates target Function"""
    setattr(target, self._getKeyName(), self._value)
