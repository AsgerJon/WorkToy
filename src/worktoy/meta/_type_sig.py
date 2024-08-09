"""TypeSig encapsulates type signatures and the functionality for
recognizing positional arguments. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Optional

from worktoy.text import monoSpace


class _SingleType:
  """This class specifies special type handling"""

  __inner_type__ = None

  def __init__(self, arg: object) -> None:
    """Initialize the _SingleType object."""
    if isinstance(arg, type):
      self.__inner_type__ = arg
    else:
      e = """The _SingleType must be initialized with a type, but received: 
      '%s'!"""
      raise TypeError(monoSpace(e % arg))

  def __str__(self) -> str:
    """String representation"""
    clsName = self.__inner_type__.__name__
    return '_SingleType(%s,)' % clsName

  def __repr__(self, ) -> str:
    """Code representation"""
    return self.__str__()

  def cast(self, arg: object) -> object:
    """Cast the argument to the inner type."""
    if arg is None:
      raise ValueError('None cannot be casted!')
    if isinstance(arg, self.__inner_type__):
      return arg
    if self.__inner_type__ is float:
      if isinstance(arg, int):
        return float(arg)
      if isinstance(arg, complex):
        if arg.imag:
          return None
        return float(arg.real)
    if self.__inner_type__ is int:
      if isinstance(arg, complex):
        if arg.imag:
          return None
        if arg.real.is_integer():
          return int(arg.real)
      if isinstance(arg, float):
        if arg.is_integer():
          return int(arg)
        return None
    return None


class TypeSig:
  """TypeSig encapsulates type signatures and the functionality for
  recognizing positional arguments. """

  __type_signature__ = None
  __single_types__ = None

  def __init__(self, *args) -> None:
    """Initialize the TypeSig object."""
    self.__type_signature__ = []
    self.__single_types__ = []
    for arg in args:
      if isinstance(arg, type):
        self.__type_signature__.append(arg)
        self.__single_types__.append(_SingleType(arg))
        continue
      e = """The TypeSig must be initialized with types, but received: 
      '%s'!"""
      raise TypeError(monoSpace(e % arg))

  def __contains__(self, other: tuple) -> bool:
    """Check if the TypeSig is contained in the other tuple."""
    if not other:
      return False
    if isinstance(other, (list, tuple)):
      out = self.cast(*other, )
      return False if out is None else True

  def __bool__(self, ) -> bool:
    """The empty signature makes the instance False."""
    return True if self.__type_signature__ else False

  def __len__(self) -> int:
    """Return the length of the type signature."""
    return len(self.__type_signature__)

  def cast(self, *args) -> Any:
    """Casts the arguments to the """
    if not args and not self:
      return []
    out = []
    for (type_, arg) in zip(self.__single_types__, args):
      val = _SingleType.cast(type_, arg)
      if val is None:
        return None
      out.append(val)
    return out

  def __str__(self) -> str:
    """String representation"""
    out = [cls.__name__ for cls in self.__type_signature__]
    return '(%s,)' % ', '.join(out)

  def __repr__(self) -> str:
    """String representation"""
    return self.__str__()
