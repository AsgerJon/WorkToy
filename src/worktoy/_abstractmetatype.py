"""MetaType provides a meta-metaclass for use across modules in the
WorkToy package"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, MutableMapping, Any, Union

from PySide6.QtWidgets import QWidget
from icecream import ic

from worktoy import DefaultClass, Function

if TYPE_CHECKING:
  Bases = tuple[type]
  Map = MutableMapping[str, Any]

ic.configureOutput(includeContext=True)  # Removed before production
ShibokenObject = type(QWidget.__class__)


class MetaMetaType(type):
  """The meta type is a meta-metaclass required to implement __str__ and
  __repr__ on the class level."""

  def __repr__(cls) -> str:
    """Code Representation"""
    if cls is MetaMetaType:
      return '_MetaMeta'
    return cls.__qualname__

  def __str__(cls) -> str:
    """String Representation"""
    if cls is MetaMetaType:
      return '_MetaMeta'
    return cls.__qualname__


class AbstractMetaType(MetaMetaType, metaclass=MetaMetaType):
  """The abstract metaclass intended for use in the rest of the package"""

  @classmethod
  def cloneNameSpace(mcls, source: Union[type, Map], **kwargs) -> dict:
    """Clones the dictionary given or the namespace of the given type.
    Use keyword argument 'includeDunder' to specify whether to include
    dunder methods, default is False."""
    if isinstance(source, type) and kwargs.get('_recursion', False):
      raise RecursionError
    if isinstance(source, type):
      return mcls.cloneNameSpace(dict(**source.__dict__), )
    if kwargs.get('includeDunder', False):
      return dict(**source)
    return {k: v for (k, v) in source.items() if not k.startswith('__')}

  @classmethod
  def _clone(mcls, cls: type) -> type:
    """
    Clones the specified derived class.

    :param cls: Derived class to be cloned.
    :return: Clone of the derived class.
    """
    return mcls(cls.__name__, cls.__bases__, mcls.cloneNameSpace(cls))

  def clone(cls, ) -> type:
    """Invokes the _clone method on the metaclass"""
    return cls.__class__._clone(cls)

  def appendFunction(cls, key: str, func: Function) -> type:
    """Concatenates the function at 'key' with the given 'func'.
    This method does not preserve the return value of either the original
    function nor the new function. It invokes the original.
    Then it invokes the appended function. For more advanced use,
    see chainFunction. """
    originalFunction = getattr(cls, key, None)
    if not isinstance(originalFunction, Function):
      raise TypeError

    def wrapper(*args, **kwargs) -> None:
      """Enhanced __init__ function"""
      originalFunction(*args, **kwargs)
      func(*args, **kwargs)

    setattr(cls, key, wrapper)
    return cls

  def chainFunction(cls, key: str, func: Function) -> type:
    """Replaces the existing function at 'key' of with 'func(existing)'.
    Thus, the provided function must map from function to function. The
    return value is then placed at 'key' and the class is returned."""
    originalFunction = getattr(cls, key, None)
    if not isinstance(originalFunction, Function):
      raise TypeError
    wrapper = func(originalFunction)
    if not isinstance(wrapper, Function):
      raise TypeError
    setattr(cls, key, wrapper)
    return cls

  @classmethod
  def __prepare__(mcls, name, bases) -> object:
    """Implements the prepare method. Subclasses should primarily use a
    custom namespace class to customize the classes."""
    return mcls.cloneNameSpace(DefaultClass)

  def __new__(mcls,
              name: str,
              bases: Bases,
              nameSpace: dict,
              **kwargs) -> type:
    cls = super().__new__(mcls, name, bases, nameSpace, **kwargs)
    return cls

  def __init__(cls,
               name: str,
               bases: Bases,
               nameSpace: dict,
               **kwargs) -> None:
    super().__init__(name, bases, nameSpace, **kwargs)


class AbstractType(DefaultClass, metaclass=AbstractMetaType):
  """Classes not implementing a custom metaclass should inherit this class"""
  pass
