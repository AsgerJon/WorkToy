"""WorkToy - Guards - TypeGuard
Guards against wrong arguments on the basis of types."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from inspect import stack
from typing import Any, Never

from icecream import ic

from worktoy.core import Function
from worktoy.guards import AbstractGuard

ic.configureOutput(includeContext=True)


class TypeGuard(AbstractGuard):
  """WorkToy - Guards - TypeGuard
  Guards against wrong arguments on the basis of types."""

  def __init__(self, *args, **kwargs) -> None:
    _types = []
    for arg in args:
      if isinstance(arg, type):
        _types.append(arg)
    AbstractGuard.__init__(self, *args, **kwargs)
    self._allowableTypes = _types or (object,)

  def __guard_validator_factory__(self, obj: object,
                                  cls: type, ) -> Function:

    def __guard_validator__(varValue: Any, varName: str) -> Any:
      if varValue is None:
        from worktoy.waitaminute import UnexpectedStateError
        raise UnexpectedStateError(varName)
      for type_ in self.getAllowableTypes():
        if isinstance(varValue, type_):
          return varValue
      from worktoy.waitaminute import TypeGuardError
      raise TypeGuardError(varValue, self)

    return __guard_validator__

  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Subclasses must implement this method."""
    if getattr(cls, '__debug_error__', False):
      return self.__debug_error__
    return self.__guard_validator_factory__(obj, cls)

  def getAllowableTypes(self) -> tuple[type, ...]:
    """Getter-function for the allowable types."""
    return self._allowableTypes

  def __debug_error__(self, ) -> Never:
    from worktoy.waitaminute import TypeGuardError
    e = TypeGuardError(7777, 'cunt', self)
    print(e.funcInfo())
