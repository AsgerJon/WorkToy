"""Argument instances define the parsing required by a function or a class.
"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn, Any, TypeAlias, Never

from worktoy import searchKeys, maybeType, maybe, CallMeMaybe

Args: TypeAlias = tuple[Any, ...]
Kwargs: TypeAlias = dict[str, Any]


class Argument:
  """Argument instances define the parsing required by a function or a class.
  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    typeKwarg = searchKeys('type_', 'class') @ str >> kwargs
    typeArg = maybeType(type, *args)
    self._type = maybe(typeKwarg, typeArg, None)
    nameKwarg = searchKeys('name') @ str >> kwargs
    nameArg = maybeType(str, *args)
    self._name = maybe(nameKwarg, nameArg, None)
    parserKwarg = searchKeys('parser', 'interpret') @ CallMeMaybe >> kwargs
    parserArg = maybeType(CallMeMaybe, *args)
    parserDefault = lambda *__, **_: None
    self._parser = maybe(parserKwarg, parserArg, parserDefault)
    if self._name is None or self._type is None:
      raise TypeError('Missing arguments!')
    self._value = None

  def _getType(self) -> type:
    """Getter-function for the type"""
    return self._type

  def _setType(self, type_: type) -> NoReturn:
    """Setter-function for the type"""

  def _delType(self, ) -> Never:
    """Illegal deleter function"""
    TypeError('ReadOnlyError')

  def parseType(self, *args) -> tuple[Any, Args]:
    """Parses the positional arguments on the content at _type"""

  def _setterFunction(self, *args, **kwargs) -> tuple[Args, Kwargs]:
    """Invoking this function on *args, **kwargs attempts to parse the
    given arguments to the value. Upon completion, the function returns
    the arguments having removed any argument used to compute the value."""
    return (args, kwargs)

  def _getValue(self) -> Any:
    """Getter-function for value"""
    return self._value

  def __invert__(self) -> Any:
    """Returns the underlying value"""

  def __matmul__(self, other: CallMeMaybe) -> Argument:
    """Overwrites the current parser with other"""
    self._parser = other
    return self

  def __call__(self, *args, **kwargs) -> NoReturn:
    """Call the instance on arguments"""

  type_ = property(_getType, _setType, _delType)
