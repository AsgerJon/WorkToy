"""
TypeSignature encapsulates type signatures in hashable objects.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..core import Object
from ..core.sentinels import Sentinel, WILDCARD, FALLBACK
from ..desc import Field
from ..utilities import textFmt, typeCast
from ..waitaminute.dispatch import HashMismatch, CastMismatch
from ..waitaminute.dispatch import TypeCastException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator, TypeAlias, Union, Self

  HASH: TypeAlias = Union[type, Sentinel]


class TypeSignature(Object):
  """TypeSignature encapsulates type signatures in hashable objects. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __raw_types__ = None
  __is_wild__ = None
  __fall_back__ = None

  #  Public Variables
  isWild = Field()
  isFallback = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @isWild.GET
  def _getIsWild(self, **kwargs) -> bool:
    """Returns True if the type signature contains WILDCARD."""
    if self.__is_wild__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__is_wild__ = True
      for type_ in self.__raw_types__:
        if type_ is WILDCARD:
          break
      else:  # means no break, thus no WILDCARD
        self.__is_wild__ = False
      return self._getIsWild(_recursion=True)
    return True if self.__is_wild__ else False

  @isFallback.GET
  def _getFallback(self) -> bool:
    """Returns True if 'self' is a fallback signature. """
    return True if FALLBACK in self else False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *types: HASH) -> None:
    if (types or [None, ])[0] is FALLBACK and len(types) != 1:
      raise NotImplementedError("""TODO: FALLBACK with other args!""")
    self.__raw_types__ = types

  @classmethod
  def fromArgs(cls, *args: Any) -> Self:
    return cls(*(type(arg) for arg in args))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __hash__(self) -> int:
    """Returns the hash of the type signature."""
    return hash((*self.__raw_types__,))

  @staticmethod
  def argHash(*args: Any) -> int:
    return hash((*(type(arg) for arg in args),))

  def __eq__(self, other: Any) -> bool:
    """Checks if the type signature is equal to another."""
    cls = type(self)
    if not isinstance(other, cls):
      return NotImplemented
    if len(self) != len(other):
      return False
    for this, that in zip(self.__raw_types__, other.__raw_types__):
      if this is not that:
        return False
    return True

  def __len__(self) -> int:
    """Returns the number of types in the type signature."""
    return len(self.__raw_types__)

  def __iter__(self) -> Iterator[HASH]:
    """Returns an iterator over the types in the type signature."""
    yield from self.__raw_types__

  def __contains__(self, item: Any) -> bool:
    """Checks if the type signature contains a given type."""
    for type_ in self:
      if type_ is item:
        return True
    return False

  def __bool__(self) -> bool:
    return True if self.__raw_types__ else False

  def __str__(self) -> str:
    """Returns a string representation of the type signature."""
    infoSpec = """%s object with %d types: %s"""
    typeStr = '[%s]' % ', '.join(str(t) for t in self)
    n = len(self)
    clsName = type(self).__name__
    return textFmt(infoSpec % (clsName, n, typeStr))

  def __repr__(self) -> str:
    """Returns code that would recreate the type signature."""
    infoSpec = """%s(%s)"""
    typeStr = ', '.join(repr(t) for t in self)
    return textFmt(infoSpec % (type(self).__name__, typeStr))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def swapType(self, *types: type) -> Self:
    """Swaps the types in the type signature with the given types."""
    self.__is_wild__ = None
    if not types:
      raise ValueError("No types provided to swap.")
    if len(types) > 2:
      raise ValueError("Too many types provided to swap, expected 1 or 2.")
    oldType, newType = None, None
    if len(types) == 1:
      out = None
      for base in types[0].__bases__:
        out = self.swapType(base, types[0])
      else:
        return out
    oldType, newType = types
    rawTypes = [*self.__raw_types__]
    updatedTypes = []
    for type_ in rawTypes:
      if type_ is oldType:
        updatedTypes.append(newType)
        continue
      updatedTypes.append(type_)
    return type(self)(*updatedTypes, )

  def mroLen(self, ) -> int:
    """Returns the number of types in the type signature, including MRO."""
    out = 0
    for type_ in self:
      for base in type_.__mro__:
        out += 1
    return out

  def calmLen(self, ) -> int:
    """Returns number of types that are not WILD"""
    return len([t for t in self if t is not WILDCARD])

  def fast(self, *args: Any) -> Any:
    """Returns arguments if their types match the type signature."""
    if not args and not self:
      return ()
    if not (self.isFallback or self.isWild):
      if len(args) == len(self):
        if hash(self) == self.argHash(*args):
          return args
    raise HashMismatch(self, *args)

  def cast(self, *args: Any) -> Any:
    """Casts arguments to the types in the type signature."""
    if len(args) > len(self) or len(args) < self.calmLen():
      raise CastMismatch(self, *args)
    out = []
    for arg, type_ in zip(args, self):
      if type_ is WILDCARD:
        out.append(arg)
        continue
      if isinstance(arg, type_):
        out.append(arg)
        continue
      try:
        casted = typeCast(type_, arg)
      except TypeCastException as typeCastException:
        raise CastMismatch(self, *args) from typeCastException
      else:
        out.append(casted)
    return (*out,)
