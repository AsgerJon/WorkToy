"""TypeSig encapsulates casting to specific type signatures. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace, typeMsg
from worktoy.castOLD import maybe, typeCast, THIS
from worktoy.waitaminute import CastMismatch

try:
  from typing import Any
except ImportError:
  Any = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

try:
  from typing import Self
except ImportError:
  Self = object

if TYPE_CHECKING:
  from typing import Optional

  Types = Optional[tuple[type, ...]]
else:
  Types = object


class TypeSig:
  """TypeSig encapsulates casting to specific type signatures. """

  __raw_types__ = None

  @staticmethod
  def _argsHash(*args) -> int:
    """Returns the hash value of the arguments. """
    return hash((*[type(arg) for arg in args],))

  def __init__(self, *args) -> None:
    """Initialize the TypeSig object."""
    for arg in args:
      if arg is THIS:
        e = """'THIS' placeholder is not allowed in TypeSig! TypeSig 
        should not be instantiated before the final object is ready. """
        raise ValueError(monoSpace(e))
      self.addType(arg)

  def getTypes(self, **kwargs) -> Types:
    """Getter-function for the inner types"""
    types_ = maybe(self.__raw_types__, ())
    if isinstance(types_, tuple):
      for type_ in types_:
        if not isinstance(type_, type):
          e = typeMsg('type', type_, type)
          raise TypeError(e)
      return types_
    if isinstance(types_, list):
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__raw_types__ = (*types_,)
      return self.getTypes(_recursion=True)
    if isinstance(types_, type):
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__raw_types__ = (types_,)
      return self.getTypes(_recursion=True)
    e = typeMsg('__raw_types__', types_, type)
    raise TypeError(e)

  def addType(self, type_: type) -> None:
    """Add a type to the inner types. """
    self.__raw_types__ = (*self.getTypes(), type_,)

  def __len__(self) -> int:
    """Returns the number of inner types. """
    return len(self.getTypes())

  def __hash__(self, ) -> int:
    """Returns the hash value of the inner types. """
    return hash((*self.getTypes(),))

  def __eq__(self, other: Self) -> bool:
    """Returns 'True' if the inner types are equal. """
    if not isinstance(other, type(self)):
      return False
    for (selfType, otherType) in zip(self.getTypes(), other.getTypes()):
      if selfType != otherType:
        return False
    return True

  def fastCast(self, *args) -> Types:
    """Attempt at casting based on hash values. Returns the arguments in a
    tuple if successful, otherwise returns 'None'. """
    if self._argsHash(*args) - hash(self):
      raise CastMismatch(self, *args)
    return args

  def flexCast(self, *args) -> Types:
    """Attempt at casting involving casting of individual arguments. """
    if len(self) - len(args):
      raise CastMismatch(self, *args)
    out = []
    types = self.getTypes()
    for (arg, type_) in zip(args, types):
      castArg = typeCast(arg, type_, strict=False)
      if castArg is None:
        raise CastMismatch(self, *args)
      out.append(castArg)
    return (*out,)

  def getTypeNames(self) -> str:
    """Returns a string representation of the type names. """
    return ', '.join([type_.__name__ for type_ in self.getTypes()])

  def __str__(self, ) -> str:
    """Returns a string representation of the TypeSig object. """
    return '(%s)' % self.getTypeNames()

  def __repr__(self, ) -> str:
    """Returns code that would create this instance. """
    clsName = type(self).__name__
    return '%s(%s)' % (clsName, self.getTypeNames())
