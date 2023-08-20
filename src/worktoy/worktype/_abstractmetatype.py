"""MetaType provides a meta-metaclass for use across modules in the
WorkToy package"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic


def maybe(*args) -> object:
  """Returns first arg not None"""
  for arg in args:
    if arg is not None:
      return arg


class _MetaType(type):
  """The meta type is a meta-metaclass required to implement __str__ and
  __repr__ on the class level."""

  def __repr__(cls) -> str:
    """Code Representation"""
    qualName = getattr(cls, '__qualname__', None)
    name = getattr(cls, '__name__', None)
    fallBack = '%s' % type(cls)
    return str(maybe(qualName, name, fallBack))

  def __str__(cls) -> str:
    """String Representation"""
    qualName = getattr(cls, '__qualname__', None)
    name = getattr(cls, '__name__', None)
    fallBack = '%s' % type(cls)
    return str(maybe(qualName, name, fallBack))

  @classmethod
  def __core_methods__(mcls) -> list[str]:
    """Returns a list of methods that are set by the metaclass."""
    if mcls is not _MetaType:
      return []
    return ['__repr__', '__str__', ]

  @classmethod
  def __default_methods__(mcls) -> list[str]:
    """Returns a list of names of methods where the MetaType provides a
    default implementation"""
    return []

  @classmethod
  def __abstract_methods__(mcls) -> list[str]:
    """Returns a list of names of methods that are required by classes,
    but where the metaclass provides no implementation."""
    return []

  @classmethod
  def __prepare__(mcls, *args, **kwargs) -> object:
    """The __prepare__ method is responsible for creating the dictionary
    used to collect the namespace. By default, this method returns an
    empty dictionary. Subclasses can reimplement this method to return a
    custom namespace class, in which case the MetaType validates the
    instances returned by the subclass implementation."""
    return super().__prepare__(*args, **kwargs)

  def __validator_namespace__(cls, *args, **kwargs) -> object:
    """This method validates namespace returned by the __prepare__ method"""

  def __new__(mcls, *args, **kwargs) -> type:
    cls = super().__new__(mcls, *args, **kwargs)
    return cls

  def __init__(cls,
               name: str,
               bases: tuple,
               nameSpace: object,
               **kwargs) -> None:
    ic(cls)
    ic(name)
    ic(bases)
    ic(nameSpace)

    super().__init__(cls, name, bases, nameSpace, )
    # for name in cls.__core_methods__():
    #   metaVersion = getattr(cls, name, None)
    #   if metaVersion is None:
    #     raise TypeError
    #   setattr(cls, name, metaVersion)
    # for name in cls.__default_methods__():
    #   metaVersion = getattr(cls, name, None)
    #   if metaVersion is None:
    #     raise TypeError
    #   classVersion = getattr(cls, name, None)
    #   if classVersion is None:
    #     setattr(cls, name, metaVersion)
    # for name in cls.__abstract_methods__():
    #   classVersion = getattr(cls, name, None)
    #   if classVersion is None:
    #     raise TypeError

  # def __call__(cls, *args, **kwargs) -> object:
  #   return type.__call__(cls, *args, **kwargs)


class AbstractMetaType(_MetaType, metaclass=_MetaType):
  """MetaType provides the metaclass that both inherits from and uses as
  metaclass the _MetaType defined above. This is the class exposed by the
  module."""
  print('AbstractMetaType')
