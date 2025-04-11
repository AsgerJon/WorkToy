"""TypeSig instances represent particular type signatures. The 'fast' method
provides a performant validation of a tuple of objects. The 'flex' method
attempts to cast each object in a tuple to the expected type. The latter is
substantially slower than the former."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.static.casting import AbstractCast, Cast
from worktoy.waitaminute import SigMismatch, CastMismatch, ResolveException

try:
  from typing import Self, TypeAlias, Any, TYPE_CHECKING
except ImportError:
  Self = object
  TypeAlias = object
  Any = object
  TYPE_CHECKING = False

from worktoy.text import typeMsg

if TYPE_CHECKING:
  Types: TypeAlias = list[type]
  Casts: TypeAlias = list[AbstractCast]


class _Types:
  """Private class representing tuple of types."""

  def __get__(self, typeSig: TypeSig, owner: type) -> Any:
    """Get the types."""
    if typeSig is None:
      return self
    types = getattr(typeSig, '__raw_types__', None)
    if types is None:
      info = """'__raw_types__' attribute is not set!"""
      raise RuntimeError(info)
    if not isinstance(types, (tuple, list)):
      e = typeMsg('__raw_types__', types, tuple)
      raise TypeError(e)
    for type_ in types:
      if not isinstance(type_, type):
        info = """Found object '%s' in '__raw_types__' that is not a 
        type!""" % str(type_)
        raise TypeError(info)
    return (*types,)


class TypeSig:
  """TypeSig instances represent particular type signatures. The 'fast'
  method provides a performant validation of a tuple of objects. The
  'flex' method attempts to cast each object in a tuple to the expected
  type. The latter is substantially slower than the former."""

  __iter_contents__ = None
  __raw_types__ = None
  __type_casts__ = None

  types = _Types()

  def __init__(self, *targetTypes, **kwargs) -> None:
    typeArgs = []
    for type_ in targetTypes:
      if isinstance(type_, str):
        type_ = globals().get(type_, None)
      if isinstance(type_, type):
        typeArgs.append(type_)
        continue
      e = typeMsg('type_', type_, type)
      raise TypeError(e)
    self.__raw_types__ = (*typeArgs,)

  def _createCasts(self, ) -> None:
    """Creator-function for the Cast objects."""
    if self.__type_casts__ is not None:
      e = """__type_casts__ has already been set!"""
      raise RuntimeError(e)
    if TYPE_CHECKING:
      assert isinstance(self.types, tuple)
    self.__type_casts__ = [Cast(type_) for type_ in self.types]

  def getCasts(self, **kwargs) -> Casts:
    """Get the casts for the types in the signature."""
    if TYPE_CHECKING:
      assert isinstance(self.types, list)
    if self.__type_casts__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createCasts()
      return self.getCasts(_recursion=True)
    if isinstance(self.__type_casts__, list):
      for cast in self.__type_casts__:
        if not isinstance(cast, AbstractCast):
          e = typeMsg('__type_casts__', cast, AbstractCast)
          raise TypeError(e)
      return self.__type_casts__
    e = typeMsg('__type_casts__', self.__type_casts__, list)
    raise TypeError(e)

  @staticmethod
  def _argHash(*args) -> int:
    """Hashes the types of the arguments received."""
    if not args:
      return 0
    return hash((*[type(arg) for arg in args],))

  def fast(self, *args, **kwargs) -> tuple:
    """If the hash of argument types matches the hash of 'self' the
    arguments are returned, otherwise a SigMismatch exception is raised."""
    if self._argHash(*args) == self.__hash__():
      return args
    raise SigMismatch(self, *args)

  def cast(self, *args) -> tuple:
    """If the hash of argument types matches the hash of 'self' the
    arguments are returned, otherwise a SigMismatch exception is raised."""
    if len(args) == len(self):
      out = []
      casts = self.getCasts()
      for (arg, cast) in zip(args, casts):
        try:
          out.append(cast(arg))
        except CastMismatch:
          break
      else:
        return self.fast(*out)
    raise SigMismatch(self, *args)

  def flex(self, *args) -> tuple:
    """This method attempts to find an argument from the given ones for
    each of the types in the signature. Unused arguments are accepted. """
    if TYPE_CHECKING:
      assert isinstance(self.types, list)
    out = []
    unusedArgs = [*args, ]
    posArgs = []
    casts = self.getCasts()
    for (type_, cast) in zip(self.types, casts):
      while unusedArgs:
        arg = unusedArgs.pop(0)
        try:
          out.append(cast(arg))
          posArgs = [*posArgs, *unusedArgs]
          break
        except CastMismatch:
          posArgs.append(arg)
      else:
        raise SigMismatch(self, *args)
      unusedArgs = [*posArgs, ]
      posArgs = []
    return self.fast(*out)

  def __iter__(self) -> Self:
    """Iterate over the types in the signature."""
    self.__iter_contents__ = [*self.types, ]
    return self

  def __next__(self, ) -> type:
    """Get the next type in the signature."""
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  def __len__(self, ) -> int:
    """Get the number of types in the signature."""
    if TYPE_CHECKING:
      assert isinstance(self.types, list)
    if self.types is None:
      return 0
    return len(self.types)

  def __contains__(self, type_: type, **kwargs) -> bool:
    """Check if the type is in the signature."""
    if isinstance(type_, type):
      for item in self:
        if item is type_:
          return True
    if kwargs.get('_recursion', False):
      raise RecursionError
    if isinstance(type_, str):
      val = globals().get(type_, None)
      if isinstance(val, type):
        return self.__contains__(val, _recursion=True)
    return self.__contains__(type(type_), _recursion=True)

  def __hash__(self, ) -> int:
    """Hash the TypeSig instance."""
    if self.types:
      return hash(self.types)
    return 0

  def _resolveOther(self, other: object) -> Self:
    """Resolve the other object to a TypeSig instance."""
    cls = type(self)
    if isinstance(other, cls):
      return other
    if isinstance(other, (tuple, list)):
      return cls(*other)
    if isinstance(other, type):
      return cls(other)
    raise ResolveException(self, other)

  def __eq__(self, other: object) -> bool:
    """Check if the TypeSig instance is equal to another."""
    try:
      other = self._resolveOther(other)
      return True if hash(self) == hash(other) else False
    except ResolveException:
      return False

  def __str__(self, ) -> str:
    """Get the string representation of the TypeSig instance."""
    if TYPE_CHECKING:
      assert isinstance(self.types, list)
    typeNames = [type_.__name__ for type_ in self.types]
    clsName = type(self).__name__
    return '%s object: [%s]' % (clsName, ', '.join(typeNames),)

  def __repr__(self, ) -> str:
    """Get the string representation of the TypeSig instance."""
    if TYPE_CHECKING:
      assert isinstance(self.types, list)
    typeNames = [type_.__name__ for type_ in self.types]
    clsName = type(self).__name__
    return '%s(%s)' % (clsName, ', '.join(typeNames),)
