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

  @staticmethod
  def _getKeyName() -> str:
    """Getter-function for keyName indicating decorated target."""
    return 'applyFlag'

  def __init__(self, value: Any) -> None:
    self._value = value

  def validate(self, target: CallMeMaybe) -> NoReturn:
    """Ensures that only functions taking and returning types are
    decorated."""
    notes = target.__annotations__
    if not notes:
      raise n00bError('Missing annotations')
    returnFlag, argFlag = False, False
    for (key, val) in notes.items():
      if key == 'return':
        if val == 'type':
          returnFlag = True
      elif val == 'type':
        argFlag = True
    if not (returnFlag and argFlag):
      cause = ''
      head = """Failed to validate target method suitable for use in class 
      decoration. When inspecting the target %s, """ % target
      if not (returnFlag or argFlag):
        cause = """type: 'type' was not found on the return value nor on 
        the argument typehints. """
      elif returnFlag:
        cause = """type: 'type' was found only on the return value, 
        not on any argument value."""
      elif argFlag:
        cause = """type: 'type' was found only on the an argument value, 
        not on the return value."""
      msg = '\n'.join([head, cause])
      raise ValidationError(msg)
    return True

  def decorate(self, target: Target) -> Target:
    """Decorates target Function"""
    setattr(target, self._getKeyName(), self._value)
