"""The Dispatch class dispatches a function call to the appropriate
function based on the type of the first argument. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import FunctionType
from worktoy.static.casting import Cast

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

from worktoy.text import typeMsg
from worktoy.waitaminute import MissingVariable, VariableNotNone
from worktoy.waitaminute import SigMismatch, CastMismatch
from worktoy.waitaminute import DispatchException

if TYPE_CHECKING:
  from typing import Any, Callable, TypeAlias

  Types: TypeAlias = tuple[type, ...]
  Hashes: TypeAlias = list[int]
  HashMap: TypeAlias = dict[int, Callable]
  TypesMap: TypeAlias = dict[Types, Callable]
  CastMap: TypeAlias = dict[Types, Callable]


class Dispatch:
  """The Dispatch class dispatches a function call to the appropriate
  function based on the type of the first argument. """

  __field_name__ = None  # name of the function
  __field_owner__ = None  # owner of the function
  __bound_instance__ = None  # bound instance

  __all_functions__ = None  # list of all functions
  __hashed_functions__ = None  # hash -> function
  __typed_functions__ = None  # types -> function

  def _getBoundInstance(self) -> object:
    """Get the bound instance."""
    return self.__bound_instance__

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the function."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the bound instance."""
    self.__bound_instance__ = instance
    return self

  def _getHashedMap(self, ) -> HashMap:
    """Get the hashed map of functions."""
    if self.__hashed_functions__ is None:
      self.__hashed_functions__ = {}
    return self.__hashed_functions__

  def _getTypedMap(self, ) -> TypesMap:
    """Get the typed map of functions."""
    if self.__typed_functions__ is None:
      self.__typed_functions__ = {}
    return self.__typed_functions__

  def _getTypes(self) -> list[Types]:
    """Get the types of the functions."""
    out = []
    typedMap = self._getTypedMap()
    return [(*types,) for types, _ in typedMap.items()]

  def _getHashes(self, ) -> Hashes:
    """Get the hashes of the functions."""
    out = []
    typeTuples = self._getTypes()
    for types in typeTuples:
      out.append(hash((*types,)))
    return out

  def _getTypeCasters(self, ) -> CastMap:
    """Get the type casters."""
    typeTuples = self._getTypes()
    out = {}
    for typeTuple in typeTuples:
      if TYPE_CHECKING:
        assert isinstance(typeTuple, tuple)
      types: Types = typeTuple
      casts = [Cast(type_) for type_ in typeTuple]

      def castFunc(*args) -> tuple:
        """Cast the arguments to the types."""
        if len(args) == len(casts):
          try:
            return (*[cast(arg) for cast, arg in zip(casts, args)],)
          except Exception as e:
            raise SigMismatch(types, args) from e
        raise SigMismatch(types, args)

      out[types] = castFunc
    return out

  def fast(self, *args, **kwargs) -> Any:
    """Fast dispatch method. This method uses the hash of the first
    argument to determine which function to call. """
    hashVal = hash((*[type(arg) for arg in args],))
    try:
      func = self.__typed_functions__[hashVal]
      return func(*args, **kwargs)
    except KeyError:
      raise SigMismatch

  def cast(self, *args, **kwargs) -> Any:
    """Cast dispatch method. This method uses the type of the first
    argument to determine which function to call. """
    castMap = self._getTypeCasters()
    castArgs = None
    for types, cast in castMap.items():
      if len(args) == len(types):
        try:
          return self.fast(*cast(*args, **kwargs))
        except SigMismatch:
          continue

  def __call__(self, *args, **kwargs):
    """Call method. This method uses the type of the first argument to
    determine which function to call. """
    instance = self._getBoundInstance()
    if instance is None:
      posArgs = (*args,)
    else:
      posArgs = (instance, *args,)
    try:
      return self.fast(*posArgs, **kwargs)
    except SigMismatch:
      try:
        return self.cast(*posArgs, **kwargs)
      except SigMismatch:
        raise DispatchException(self._getTypes(), *posArgs) from None
