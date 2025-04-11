"""OverloadEntry provides a decorator for functions that are overloaded. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.castOLD import maybe
from worktoy.text import typeMsg

try:
  from typing import Any, TYPE_CHECKING
except ImportError:
  Any = object
  TYPE_CHECKING = False

try:
  from typing import Self
except ImportError:
  Self = object

if TYPE_CHECKING:
  from worktoy.mcls import CallMeMaybe

  DefTypes = list[type]
else:
  DefTypes = object


class OverloadEntry:
  """OverloadEntry provides a decorator for functions that are
  overloaded. """

  __call_me_maybe__ = None
  __is_fallback__ = None
  __deferred_types__ = None

  def __init__(self, *types, **kwargs) -> None:
    """Initialize the OverloadEntry object. """
    self.__deferred_types__ = [*types, ]
    self.__is_fallback__ = True if kwargs.get('_fallback', False) else False

  def isFallback(self) -> bool:
    """Return True if the entry is a fallback. """
    return True if self.__is_fallback__ else False

  def __call__(self, callMeMaybe: CallMeMaybe) -> Self:
    """Set the function as the callable for the type signature. """
    if self.__call_me_maybe__ is not None:
      e = """The function has already been set! This indicates that the 
      '%s' object is being called directly. This is not possible! 
      Instances of this class are intended only for use during class 
      creation. """
      raise AttributeError(e % self.__class__.__name__)
    if not callable(callMeMaybe):
      e = typeMsg('func', callMeMaybe, CallMeMaybe)
      raise TypeError(e)
    self.__call_me_maybe__ = callMeMaybe
    return self

  def __bool__(self) -> bool:
    """Return True if the function has been set. """
    return False if self.__call_me_maybe__ is None else True

  def getDeferredTypes(self) -> DefTypes:
    """Return the deferred types. """
    defTypes = maybe(self.__deferred_types__, [])
    if isinstance(defTypes, list):
      for t in defTypes:
        if not isinstance(t, type):
          e = typeMsg('type', t, type)
          raise TypeError(e)
      return defTypes
    e = typeMsg('deferred_types', defTypes, list)
    raise TypeError(e)

  def getFunc(self) -> CallMeMaybe:
    """Getter-function for the contained function. """
    if self.__call_me_maybe__ is None:
      e = """The function has not been set!"""
      raise AttributeError(e)
    if callable(self.__call_me_maybe__):
      if TYPE_CHECKING:
        assert isinstance(self.__call_me_maybe__, CallMeMaybe)
      return self.__call_me_maybe__
    e = typeMsg('call_me_maybe', self.__call_me_maybe__, CallMeMaybe)
    raise TypeError(e)

  def __str__(self) -> str:
    """Return a string representation of the object. """
    out = """OverloadEntry: %s -> %s"""
    typeStr = ', '.join([t.__name__ for t in self.getDeferredTypes()])
    if self:
      return out % (typeStr, self.getFunc().__name__)
    return out % (typeStr, 'Function not set!')


class _FallbackDescriptor:
  """Descriptor class for the fallback function. """

  def __get__(self, instance: object, owner: type) -> Any:
    """Return the fallback function. """
    if instance is None:
      return self

    def fallbackFactory(callMeMaybe: CallMeMaybe) -> OverloadEntry:
      """Return a fallback OverloadEntry object. """
      entry = OverloadEntry(_fallback=True)
      return entry(callMeMaybe)

    return fallbackFactory


class OverloadDecorator:
  """Decorator class wrapping the overloading"""

  fallback = _FallbackDescriptor()

  def __call__(self, *types) -> OverloadEntry:
    """Return an OverloadEntry object. """
    return OverloadEntry(*types)


overload = OverloadDecorator()
