"""WorkToy - Core - MetaClassParams
Instances of AbstractParams collecting arguments for use in the metaclass
implementation. Please note that the Params instance has to be set on the
meta-metaclass, not on the actual metaclass. For convenience, the
meta-metaclass is implemented here."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.fields import Parameter, AbstractDescriptor

ARGS = tuple[type, str, tuple[type, ...], dict]


class _Name(Parameter):
  """Name parameter"""

  def __get__(self, obj: object, cls: type) -> str:
    name = Parameter.__get__(self, obj, cls)
    if isinstance(name, str):
      return name


class _Bases(Parameter):
  """Bases Parameter"""

  def __get__(self, obj: object, cls: type) -> tuple:
    bases = Parameter.__get__(self, obj, cls)
    if isinstance(bases, tuple):
      return bases


class _NameSpace(Parameter):
  """NameSpace Parameter"""

  def __get__(self, obj: object, cls: type) -> dict:
    nameSpace = Parameter.__get__(self, obj, cls)
    if isinstance(nameSpace, dict):
      return nameSpace


class MetaClassParams(AbstractDescriptor):
  """WorkToy - Core - MetaClassParams
  Instances of AbstractParams collecting arguments for use in the metaclass
  implementation."""

  name = _Name(str, 'name')
  bases = _Bases(tuple, 'bases')
  nameSpace = _NameSpace(dict, 'nameSpace')


class MetaMetaClass(type):
  """The meta-metaclass implements __repr__ and __str__ for even the
  metaclasses themselves."""

  params = MetaClassParams()

  def __str__(cls) -> str:
    """String Representation"""
    return cls.__qualname__

  def __repr__(cls) -> str:
    """Code Representation"""
    return '%s()' % cls.__qualname__
