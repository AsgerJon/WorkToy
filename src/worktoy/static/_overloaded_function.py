"""OverloadedFunction class represent an overloaded function. Each
instance may have multiple signatures, but must point to a single function
object. If instantiated with class method 'fallback', the function object
will be used as a fallback if no other signatures match. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parse import maybe
from worktoy.static import TypeSig
from worktoy.text import typeMsg
from worktoy.waitaminute import MissingVariable, ReadOnlyError

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any, Callable


class _Name:
  """Private descriptor allowing attribute access to the name of the
  wrapped function. """

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the name of the function."""
    if instance is None:
      return self
    if TYPE_CHECKING:
      assert isinstance(instance, OverloadedFunction)
    return instance.getFunc().__name__


class _FallbackFlag:
  """_FallbackFlag is a flag that indicates that the function object is a
  fallback. """

  __fallback_state__ = False
  __default_state__ = None

  __attr_name__ = '__is_fallback__'

  def _getAttrName(self, ) -> str:
    """Get the name of the attribute."""
    return self.__attr_name__

  def __init__(self, state: bool = None) -> None:
    """Initialize the _FallbackFlag object."""
    if state is not None:
      self.__default_state__ = state

  def __get__(self, instance: object, owner: object) -> Any:
    """Get the state of the flag."""
    if instance is None:
      return self
    attrName = self._getAttrName()
    val = getattr(instance, attrName, None)
    out = maybe(val, self.__default_state__, self.__fallback_state__)
    return True if out else False

  def __set__(self, instance: object, value: bool) -> None:
    """Set the state of the flag."""
    attrName = self._getAttrName()
    setattr(instance, attrName, True if value else False)


class _FlexFlag(_FallbackFlag):
  """_FlexFlag indicates that the function object allows a flexible
  call. """

  def _getAttrName(self, ) -> str:
    """Get the name of the attribute."""
    return '__allow_flex__'

  def __set__(self, instance: object, value: bool) -> None:
    """Set the state of the flag."""
    raise ReadOnlyError(object, self, value)


class OverloadedFunction:
  """OverloadedFunction class represent an overloaded function. Each
  instance may have multiple signatures, but must point to a single function
  object. If instantiated with class method 'fallback', the function object
  will be used as a fallback if no other signatures match. """

  __iter_contents__ = None

  __overloaded_function__ = None
  __type_sigs__ = None
  __is_fallback__ = None
  __allow_flex__ = None

  __name__ = _Name()
  isFallback = _FallbackFlag()
  allowFlex = _FlexFlag()

  def getFunc(self, ) -> Callable:
    """Get the function object of the overloaded function. """
    if self.__overloaded_function__ is None:
      from worktoy.mcls import CallMeMaybe
      raise MissingVariable('__overloaded_function__', CallMeMaybe)
    if not callable(self.__overloaded_function__):
      from worktoy.mcls import CallMeMaybe
      name = '__overloaded_function__'
      func = self.__overloaded_function__
      e = typeMsg(name, func, CallMeMaybe)
      raise TypeError(e)
    return self.__overloaded_function__

  def _setFunc(self, func: Callable) -> None:
    """Set the function object of the overloaded function. """
    if self.__overloaded_function__ is not None:
      raise MissingVariable('__overloaded_function__', Callable)
    if not callable(func):
      from worktoy.mcls import CallMeMaybe
      e = typeMsg('func', func, CallMeMaybe)
      raise TypeError(e)
    self.__overloaded_function__ = func

  def getTypeSigs(self, **kwargs) -> list[TypeSig]:
    """Get the type signatures of the overloaded function. """
    if self.__type_sigs__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__type_sigs__ = []
      return self.getTypeSigs(_recursion=True)
    if not isinstance(self.__type_sigs__, list):
      e = typeMsg('__type_sigs__', self.__type_sigs__, list)
      raise TypeError(e)
    return self.__type_sigs__

  def _addTypeSig(self, sig: TypeSig) -> None:
    """Add a type signature to the overloaded function. """
    if not isinstance(sig, TypeSig):
      e = typeMsg('sig', sig, TypeSig)
      raise TypeError(e)
    existing = self.getTypeSigs()
    if sig in existing:
      return
    self.__type_sigs__ = [*existing, sig]

  def __iter__(self, ) -> Self:
    """Implements the iterator protocol to  iterate through the type
    signatures. """
    self.__iter_contents__ = [*self.getTypeSigs(), ]
    return self

  def __next__(self, ) -> TypeSig:
    """Get the next type signature in the iterator. """
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    self.__iter_contents__ = None
    raise StopIteration

  def __call__(self, other: Self) -> Self:
    """Call the overloaded function with the other instance. """
    cls = type(self)
    if isinstance(other, cls):
      if not self.isFallback and other.isFallback:
        self.__is_fallback__ = True
      if not self.allowFlex and other.allowFlex:
        self.__allow_flex__ = True
      for sig in other:
        self._addTypeSig(sig)
      self._setFunc(other.getFunc())
      return self
    if callable(other):
      self._setFunc(other)
      return self
    e = typeMsg('other', other, cls)
    raise TypeError(e)

  def __init__(self, *types: type, **kwargs) -> None:
    """Initialize the overloaded function. """
    self._addTypeSig(TypeSig(*types))
    self.__is_fallback__ = kwargs.get('_fallback', False)
    self.__allow_flex__ = kwargs.get('_flex', False)

  @classmethod
  def fallback(cls, *args) -> Self:
    """Creates an instance with the 'isFallback' flag set to True. """
    if not args:
      return cls(_fallback=True, )
    if all(isinstance(arg, type) for arg in args):
      return cls(*args, _fallback=True, )
    if isinstance(args[0], cls):
      other = args[0]
      other.__is_fallback__ = True
      return other
    if callable(args[0]):
      self = cls(_fallback=True, )
      self(args[0])
      return self
    from worktoy.mcls import CallMeMaybe
    e = typeMsg('other', args[0], CallMeMaybe)
    raise TypeError(e)

  @classmethod
  def flex(cls, *args) -> Self:
    """Creates an instance with the 'allowFlex' flag set to True. """
    if all(isinstance(arg, type) for arg in args):
      return cls(*args, _flex=True, _root=True)
    if isinstance(args[0], cls):
      other = args[0]
      other.__allow_flex__ = True
      return other
    if callable(args[0]):
      self = cls(_flex=True, _root=True)
      self._setFunc(args[0])
      return self
    from worktoy.mcls import CallMeMaybe
    e = typeMsg('other', args[0], CallMeMaybe)
    raise TypeError(e)
