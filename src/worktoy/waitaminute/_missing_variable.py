"""
MissingVariable subclasses 'AttributeError' and provides a custom
exception raised to indicate that a variable was expected to have been
assigned a value other than 'None'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class MissingVariable(AttributeError):
  """
  MissingVariable subclasses 'AttributeError' and provides a custom
  exception raised to indicate that a variable was expected to have been
  assigned a value other than 'None'.

  Attributes
  ----------
  instance: Any
    The instance that the variable was expected to be assigned to.
  varName: str
    The name of the variable that was expected to be assigned a value
    other than 'None'.
  expectedTypes: tuple of type
    The accepted types for the variable. May be empty if no type was
    given; shown as a single name for one type, or 'Union[...]' for
    several.

  Examples
  --------
  >>>  from typing import TypeAlias, Optional, Callable, Any, Type, Union
  >>>  from types import FunctionType as Func
  >>>  from worktoy.waitaminute import TypeException
  ...
  >>>  MaybeFunc: TypeAlias = Optional[Func]
  ...
  >>>  class Decorate:
  ...    __wrapped__: MaybeFunc = None
  ...
  ...    def __init__(self, func: MaybeFunc = None) -> None:
  ...      if func is not None:
  ...        if not callable(func):
  ...          raise TypeException('func', func, Callable)
  ...        self.__wrapped__ = func
  ...
  ...    def __call__(self, *args, **kw) -> Any:
  ...      if self.__wrapped__ is None:
  ...        raise MissingVariable(self, '__wrapped__', Callable)
  ...      return self.__wrapped__(*args, **kw)
  ...
  >>>  try:
  ...    decorated = Decorate()
  ...    decorated()
  ...  except MissingVariable as missingVariable:
  ...    print(missingVariable)
  """

  __slots__ = ('instance', 'varName', 'expectedTypes')

  def __init__(self, instance: Any, varName: str, *type_: type) -> None:
    self.varName = varName
    self.instance = instance
    self.expectedTypes = type_
    AttributeError.__init__(self, )

  def __str__(self) -> str:
    owner = type(self.instance).__name__
    infoSpec = """Missing '%s.%s: %s'!"""
    if not self.expectedTypes:
      typeStr = ''
      infoSpec = """Missing '%s.%s%s'!"""
    elif len(self.expectedTypes) == 1:
      typeStr = self.expectedTypes[0].__name__
    else:
      typeSpec = """Union[%s]"""
      typeNames = ', '.join(cls.__name__ for cls in self.expectedTypes)
      typeStr = typeSpec % typeNames
    info = infoSpec % (owner, self.varName, typeStr)
    return textFmt(info)

  __repr__ = __str__
