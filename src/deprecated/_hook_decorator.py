"""
PreGetHook decorates a method on an 'AbstractDescriptor' subclass to
specify it as a pre-get hook.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from types import FunctionType as Func

from worktoy.attr.accessor_hooks import HookPhase
from worktoy.parse import maybe
from worktoy.static import AbstractObject
from worktoy.text import stringList
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute import VariableNotNone

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self, Union, Iterator, TypeAlias, Type
  from . import AbstractDescriptorHook as Hook

  AHook: TypeAlias = Type[Hook]


class _Name(AbstractObject):
  """
  Simple descriptor returning the name of the wrapped function.
  """

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    Returns the name of the PreGetHook.
    """
    if instance is None:
      return self
    wrappedFunc = getattr(instance, '__wrapped__', None)
    if wrappedFunc is None:
      raise MissingVariable('__wrapped__', )
    wrappedName = getattr(wrappedFunc, '__name__', None)
    if wrappedName is None:
      raise MissingVariable('__name__', )
    if isinstance(wrappedName, str):
      return wrappedName
    raise TypeException('wrappedName', wrappedName, str, )


class _Priority(AbstractObject):
  """
  _Priority exposes the priority of the accessor hook through the descriptor
  protocol.
  """

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    Returns the priority value of the hook.
    """
    if instance is None:
      return self
    getPriority = getattr(instance, '_getPriority', None)
    if getPriority is None:
      raise MissingVariable('_getPriority', )
    if not callable(getPriority):
      raise TypeException('_getPriority', getPriority, Func, )
    return getPriority()


class HookDecorator(AbstractObject):
  """
  HookDecorator decorates a method on an 'AbstractDescriptor' subclass to
  specify it as a hook. Each particular hook should subclass this class.
  """
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables
  __fallback_priority__ = 255

  #  Private Variables
  __priority_value__ = None
  __wrapped__ = None
  __hook_phases__ = None

  #  Public Variables

  #  Virtual Variables
  __name__ = _Name()
  priority = _Priority()
  p = priority

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getWrapped(self) -> Func:
    """
    Returns the wrapped function.
    """
    print(self.instance, self.owner, self.__wrapped__, )
    if self.__wrapped__ is None:
      raise MissingVariable('__wrapped__', )
    if not hasattr(self.__wrapped__, '__name__'):
      raise MissingVariable('__name__', )
    wrappedName = getattr(self.__wrapped__, '__name__', )
    wrappedFunc = getattr(self.owner, wrappedName, None)
    if wrappedFunc is None:
      raise MissingVariable(wrappedName, )
    if not callable(wrappedFunc):
      raise TypeException(wrappedName, wrappedFunc, Func, )
    if hasattr(wrappedFunc, '__func__'):
      wrappedFunc = getattr(wrappedFunc, '__func__', )
    if self.instance is None:
      return wrappedFunc
    raise SystemExit

    def boundMethod(*args, **kwargs) -> Any:
      """
      Returns a method bound to the instance.
      """
      return wrappedFunc(self.instance, *args, **kwargs)

    return boundMethod  # NOQA

  def _getPriority(self) -> int:
    """
    Returns the priority value of the hook.
    """
    return maybe(self.__priority_value__, self.__fallback_priority__)

  @abstractmethod
  def _getPrimaryHookPhase(self, ) -> HookPhase:
    """
    Subclasses must implement this method to specify what hook phase to
    which they apply.
    """

  def _getHookPhases(self, **kwargs) -> Iterator[HookPhase]:
    """
    Getter-function for the hook phases where the decorated function
    object should run.
    """
    if self.__hook_phases__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__hook_phases__ = (self._getPrimaryHookPhase(),)
    yield from self.__hook_phases__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _wrapOther(self, other: Union[Self, Func]) -> Self:
    """
    When stacking these decorators, the outermost decorator returns the
    final object that will appear in the class namespace.
    """
    if isinstance(other, Func):
      self._setWrapped(other)
      return self
    otherWrapped = other._getWrapped()
    otherHookPhases = other._getHookPhases()
    self._setWrapped(otherWrapped)
    existingHookPhases = self._getHookPhases()
    self.__hook_phases__ = (*existingHookPhases, *otherHookPhases,)
    return self

  def _setWrapped(self, wrapped: Any, **kwargs) -> None:
    """
    Setter-function for the wrapped function.
    """
    if self.__wrapped__ is not None:
      raise VariableNotNone('__wrapped__', )
    if isinstance(wrapped, Func):
      self.__wrapped__ = wrapped

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __call__(self, *args, **kwargs) -> Any:
    """
    If the '__wrapped__' has not been set, this call assumes it receives
    the method to be wrapped.
    """
    if self.__wrapped__ is None:
      return self._wrapOther(args[0])
    print('calling wrapped function: %s' % self.__wrapped__.__name__)
    print('owned by: %s' % self.owner.__name__)
    print('with instance: %s' % self.instance)
    wrappedFunc = self._getWrapped()
    return wrappedFunc(*args, **kwargs)

  def __int__(self) -> int:
    """
    Returns the priority value of the hook.
    """
    return self._getPriority()

  def __set_name__(self, owner: AHook, name: str, **kwargs) -> None:
    """
    Sets the name of the HookDecorator.
    """
    super().__set_name__(owner, name, **kwargs)
    wrapped = self._getWrapped()
    for hookPhase in self._getHookPhases():
      owner.addPhase(hookPhase, wrapped)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    pKeys = stringList("""priority, rank, tier, order""")
    kwargPriority, kwargs = self.parseKwargs(int, *pKeys, **kwargs)
    if kwargPriority is None:
      argPriority = None
      for arg in args:
        if isinstance(arg, int):
          argPriority = arg
          break
      else:
        self.__priority_value__ = self.__fallback_priority__
    else:
      self.__priority_value__ = kwargPriority
    if len(args) == 1:
      try:
        self._setWrapped(args[0])
      except TypeException as typeException:
        if typeException.actualObject is not args[0]:
          raise typeException

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
