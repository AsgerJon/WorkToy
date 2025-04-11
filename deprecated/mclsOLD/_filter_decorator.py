"""ItemFilter provides namespace filtering logic for use by the custom
namespace system in the 'worktoy.mcls' module. The namespace class should
own an instance of ItemFilter, which should then decorate the callables in
the class that are to be used as filters. These filter functions will
receive arguments:
  - self: The namespace object
  - key: The key being set
  - value: The value being set
They should return True if they handle the key and value, or False if the
default __setitem__ should be called. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import FilterFunction
from worktoy.parse import maybe
from worktoy.waitaminute import MissingVariable

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Callable, Self


class FilterDecorator:
  """FilterDecorator provides namespace filtering logic for use by the custom
  namespace system in the 'worktoy.mcls' module. The namespace class should
  own an instance of ItemFilter, which should then decorate the callables in
  the class that are to be used as filters. These filter functions will
  receive arguments:
    - self: The namespace object
    - key: The key being set
    - value: The value being set
  They should return True if they handle the key and value, or False if the
  default __setitem__ should be called. """

  __field_name__ = None
  __field_owner__ = None
  __function_names__ = None

  __bound_instance__ = None

  __iter_contents__ = None
  __filter_contents__ = None

  def _getFunctionNames(self) -> list[str]:
    """Get the function names."""
    return maybe(self.__function_names__, [])

  def _addFunctionName(self, name: str) -> None:
    """Adds the given name to the list of function names. """
    existing = self._getFunctionNames()
    self.__function_names__ = [*existing, name]

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner  # Will point to baseclass

  def __get__(self, instance: object, owner: type) -> FilterDecorator:
    """Get the wrapped function. The owner is the class through which the
    descriptor is accessed. This is either __field_class__ or a subclass
    hereof. """
    if instance is None:
      return self
    if TYPE_CHECKING:
      assert isinstance(instance, self.__field_owner__)
    self.__bound_instance__ = instance
    return self

  def _getPrivateName(self) -> str:
    """Get the private name of the field."""
    if self.__field_name__ is None:
      raise MissingVariable('__field_name__', type(self))
    return '_%s_functions' % self.__field_name__

  def _getFieldOwner(self) -> type:
    """Get the owner of the field."""
    if self.__field_owner__ is None:
      raise MissingVariable('__field_owner__', type(self))
    return self.__field_owner__

  def __call__(self, callMeMaybe: Callable) -> FilterFunction:
    """Decorator for item filters. """
    self._addFunctionName(callMeMaybe.__name__)
    return FilterFunction(callMeMaybe)

  def __iter__(self, ) -> Self:
    """Iterate over the filter functions."""
    self.__iter_contents__ = []
    for name in self._getFunctionNames():
      func = getattr(self.__bound_instance__, name, None)
      if func is not None:
        self.__iter_contents__.append(func)
        continue
      raise MissingVariable(name, Callable)
    return self

  def __next__(self, ) -> Callable:
    """Get the next filter function."""
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    self.__iter_contents__ = None
    raise StopIteration
