"""WorkSide - Geometry - GeoMeta
Metaclass for the geometries"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.core import Bases, Map
from worktoy.base import DefaultClass
from worktoy.metaclass import AbstractMetaClass

ic.configureOutput(includeContext=True)


class GeoMeta(AbstractMetaClass, ):
  """WorkSide - Geometry - GeoMeta
  Metaclass for the geometries"""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> Map:
    return {}

  def __str__(cls) -> str:
    """String Representation"""
    return 'Geometry Class: %s' % cls.__qualname__

  def __repr__(cls, ) -> str:
    """Code Representation"""
    return '%s()' % cls.__qualname__

  def __new__(mcls, *args, **kwargs) -> type:
    out = AbstractMetaClass.__new__(mcls, *args, **kwargs)
    setattr(out, '__str__', getattr(mcls, '__instance_str__'))
    setattr(out, '__repr__', getattr(mcls, '__instance_repr__'))

    return out

  def __init__(cls, *args, **kwargs) -> None:
    AbstractMetaClass.__init__(cls, *args, **kwargs)

  @staticmethod
  def __instance_str__(self, ) -> str:
    name = self.__class__.__qualname__
    width = getattr(self, 'width', None)
    height = getattr(self, 'height', None)
    left = getattr(self, 'left', None)
    top = getattr(self, 'top', None)
    right = getattr(self, 'right', None)
    bottom = getattr(self, 'bottom', None)
    if name == 'Rect':
      header = 'Rectangle spanning:'
      msg = '(Left: %d, top: %d, right: %d, bottom: %d)'
      subHeader = msg % (left, top, right, bottom)
      return self.monoSpace('%s<br>%s' % (header, subHeader))
    return '%s Instance' % self.__class__.__qualname__

  @staticmethod
  def __instance_repr__(self, ) -> str:
    return '%s()' % self.__class__.__qualname__
