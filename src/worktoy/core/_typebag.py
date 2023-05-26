"""TypeBag is a subclass of the typing union classes that support
isinstance."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import typing

from icecream import ic

from worktoy.core import CopyClass, unStupid, unPack

union = getattr(typing, '_UnionGenericAlias', None)
if union is None:
  raise ImportError('Failed to find _UnionGenericAlias!')

ic.configureOutput(includeContext=True)


def _parseType(stupid: union) -> list[type]:
  """Extracts the types from the stupid"""
  return unStupid(stupid)


class CopyMeta(CopyClass):
  """Metaclass inheriting the copy functionality"""

  def __call__(cls, *args, **kwargs) -> typing.Any:
    name = '%s%s' % (cls.__name__, 'copy')
    newCls = type(name, cls.__bases__, cls.__dict__.copy())
    newTypes = unPack(*args)
    setattr(newCls, '__types__', newTypes)
    setattr(newCls, '__args__', newTypes)
    newInstance = newCls.__new__(newCls)
    newInstance._name = '%s_instance' % (name)
    return newInstance


class TypeBagParent(metaclass=CopyMeta):
  """Mixin class bringing the metaclass"""
  pass


class _TypeBag(TypeBagParent, union, _root='F... da police!'):
  """TypeBag is a subclass of the typing union classes that support
  isinstance.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init_subclass__(cls, /, *args, **kwargs) -> typing.NoReturn:
    """ClassFail"""

  def __init__(self, *args, **kwargs) -> None:
    union.__init__(self, *args, **kwargs)

  @classmethod
  def __instancecheck__(cls, instance) -> bool:
    """Implementing instance check"""


class TypeBag(_TypeBag):
  @classmethod
  def __instancecheck__(cls, instance: typing.Any) -> bool:
    """Reimplementation"""
    for type_ in cls.__types__:
      if isinstance(instance, type_):
        return True
    return False

  def __init__(self, *args, **kwargs) -> None:
    _TypeBag.__init__(self, *args, **kwargs)
    self._curInd = 0

  def __contains__(self, type_: type) -> bool:
    """Indicates whether given type is in this bag."""
    return True if type_ in self.types else False

  def __len__(self) -> int:
    """Number of types in bag"""
    cls = self.__class__
    return len(cls.__types__)

  def __iter__(self) -> TypeBag:
    """Implementation of iteration through the types"""
    self._curInd = 0
    return self

  def __next__(self) -> type:
    """Implementation of iteration through the types"""
    self._curInd += 1
    if self._curInd > len(self):
      raise StopIteration
    return self.types[self._curInd - 1]

  def _getTypes(self) -> list[type]:
    """Getter-function for the types"""
    out = self.__class__.__types__
    if any([t in out for t in [float, int, complex]]):
      out = [*out, float, int, complex]
      return list(set(out))

  def _setTypes(self, *_) -> typing.Never:
    """Illegal setter function"""
    from worktoy.waitaminute import ReadOnlyError
    raise ReadOnlyError('types')

  def _delTypes(self, ) -> typing.Never:
    """Illegal deleter function"""
    from worktoy.waitaminute import ReadOnlyError
    raise ReadOnlyError('types')

  types = property(_getTypes, _setTypes, _delTypes)


Container = TypeBag(list, tuple)
Numerical = TypeBag(int, float, complex)
