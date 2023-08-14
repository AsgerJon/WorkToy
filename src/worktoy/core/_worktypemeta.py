"""MetaField provides metaclass shared by the Field classes"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Self, Type, MutableMapping, TYPE_CHECKING, cast

from worktoy.core import NameSpace
from worktoy.functionals import validateNamespace

if TYPE_CHECKING:
  pass

# from worktoy.waitaminute import InvalidNameSpaceError

Bases = tuple[type]
Map = MutableMapping[str, Any]


class WorkTypeMeta(type):
  """MetaField provides metaclass shared by the Field classes"""

  __meta__ = None

  @staticmethod
  def createNameSpace(name: str, bases: Bases, **kwargs) -> Map:
    """Creator-function for the nameSpace used by the __prepare__ method.
    By default, an instance of 'dict' is returned containing:
      nameSpace = dict(
        __prepare_data__=dict(name=name, bases=bases, **kwargs))
    To use an instance of a custom class instead of the builtin dict,
    it is sufficient to reimplement this method as the __prepare__ method
    is already implemented to call this method."""
    return dict(__prepare_data__=dict(name=name, bases=bases, **kwargs))

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> Map:
    """The default implementation receives an appropriate object from the
    createNameSpace method and returns it. Subclasses can adjust this
    behaviour as needed. Please note that the base implementation includes
    a call to the validateNameSpace method, which ensures that the object
    intended for use as namespace does in fact support the necessary
    operations."""
    testNameSpace = mcls.createNameSpace(name, bases, **kwargs)
    if validateNamespace(cast(Map, testNameSpace)):
      return cast(Map, mcls.createNameSpace(name, bases, **kwargs))

  @staticmethod
  def __pre_init__(self: Any, *args, **kwargs) -> None:
    """During instance creation, this method is invoked after the __new__
    on the class, but before the __init__ on the class. By default,
    this method does nothing, but it is invoked by the default instance
    creation allowing subclasses to simply implement this method."""

  @staticmethod
  def __post_init__(self: Any, *args, **kwargs) -> None:
    """Similar to above except called after the __init__ on the class"""

  def __new_str__(cls, ) -> type:
    """Enhances the __str__ on the class """

  def __new__(mcls,
              name: str,
              bases: Bases,
              nameSpace: NameSpace,
              **kwargs) -> type:
    """Implementation of class creation logic"""
    cls = super().__new__(mcls, name, bases, nameSpace, **kwargs)
    setattr(cls, '__pre_init__', mcls.__pre_init__)
    setattr(cls, '__post_init__', mcls.__post_init__)
    setattr(cls, '__meta__', mcls)
    return cls

  def __init__(cls,
               name: str,
               bases: Bases,
               nameSpace: NameSpace,
               **kwargs) -> None:
    """Implementation of class initialization"""
    type.__init__(cls, name, bases, nameSpace, **kwargs)

  def __call__(cls: Type[Self], *args, **kwargs) -> Any:
    """Instance creation and initialization"""
    self = object.__new__(cls)
    cls.__pre_init__(self, *args, **kwargs)
    cls.__init__(self, *args, **kwargs)
    cls.__post_init__(self, *args, **kwargs)
    return self

  def __repr__(cls, ) -> str:
    """Code Representation of class"""
    return cls.__qualname__ or type.__repr__(cls)

  def __str__(cls) -> str:
    """String Representation of class"""
    if type(cls) is type:
      return cls.__qualname__
    return '%s of metaclass: %s' % (cls.__qualname__, cls.__meta__)


class WorkType(metaclass=WorkTypeMeta):
  """Base class implementing the metaclass. """
  pass
