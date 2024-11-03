"""TypeSig encapsulates type signatures and the functionality for
recognizing positional arguments. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybe

try:
  from typing import Any
except ImportError:
  Any = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

from worktoy.text import monoSpace, typeMsg

if TYPE_CHECKING:
  from typing import Union, Optional

  Number = Union[int, float, complex]
  MaybeInt = Optional[int]
  MaybeFloat = Optional[float]
  MaybeComplex = Optional[complex]
else:
  Number = object
  MaybeInt = object
  MaybeFloat = object
  MaybeComplex = object


class TypeSig:
  """TypeSig encapsulates type signatures and the functionality for
  recognizing positional arguments. """

  __type_signature__ = None
  __hash_value__ = None

  @classmethod
  def castInt(cls, num: Number) -> MaybeInt:
    """Casts the number to an integer."""
    if isinstance(num, int):
      return num
    if isinstance(num, float):
      if num.is_integer():
        return int(num)
      return None
    if isinstance(num, complex):
      if num.imag:
        return None
      return cls.castInt(num.real)
    return None

  @classmethod
  def castFloat(cls, num: Number) -> MaybeFloat:
    """Casts the number to a float."""
    if isinstance(num, int):
      return float(num)
    if isinstance(num, float):
      return num
    if isinstance(num, complex):
      if num.imag:
        return None
      return cls.castFloat(num.real)
    return None

  @classmethod
  def castComplex(cls, num: Number) -> MaybeComplex:
    """Casts the number to a complex number."""
    if isinstance(num, int):
      return cls.castFloat(num) + 0j
    if isinstance(num, float):
      return num + 0j
    if isinstance(num, complex):
      return num
    return None

  @classmethod
  def castArg(cls, arg: object, type_: type) -> object:
    """Casts the argument to the type. """
    if type_ is int:
      return cls.castInt(arg)
    if type_ is float:
      return cls.castFloat(arg)
    if type_ is complex:
      return cls.castComplex(arg)
    if isinstance(arg, type_):
      return arg
    return None

  def __init__(self, *args) -> None:
    """Initialize the TypeSig object."""
    self.__type_signature__ = []
    for arg in args:
      if isinstance(arg, type):
        self.__type_signature__.append(arg)
        continue
      e = """The TypeSig must be initialized with types, but received: 
      '%s'!"""
      raise TypeError(monoSpace(e % arg))
    self.setHash(hash((*args,)))

  def __hash__(self, ) -> int:
    """Return the hash of the type signature."""
    if self.__hash_value__ is None:
      e = """The hash value has not been set!"""
      raise ValueError(monoSpace(e))
    return self.__hash_value__

  def setHash(self, hashValue: int) -> None:
    """Set the hash value of the type signature."""
    self.__hash_value__ = hashValue

  def getTypes(self, ) -> list[type]:
    """Return the types of the type signature."""
    return maybe(self.__type_signature__, [])

  def fastCast(self, *args) -> object:
    """Fast cast the arguments to the type signature."""
    if hash((*[type(arg) for arg in args],)) - hash(self):
      return None
    return (*[self.castArg(a, t) for (a, t) in zip(args, self.getTypes())],)

  def cast(self, *args) -> Any:
    """Casts the arguments to the """
    if len(args) != len(self):
      return None
    if not args and not self:
      return []
    out = []
    for (type_, arg) in zip(self.getTypes(), args):
      val = self.castArg(arg, type_)
      if val is None:
        return None
      out.append(val)
    return out

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

  def __str__(self) -> str:
    """String representation"""
    out = [cls.__name__ for cls in self.getTypes()]
    return '(%s,)' % ', '.join(out)

  def __repr__(self) -> str:
    """String representation"""
    return self.__str__()
