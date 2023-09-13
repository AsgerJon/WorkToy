"""WorkSide - Widgets - FontFamily
Enum class representation of common classes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtGui import QFont
from icecream import ic
from worktoy.core import Bases
from worktoy.metaclass import AbstractMetaClass, AbstractNameSpace
from worktoy.worktoyclass import WorkToyClass

ic.configureOutput(includeContext=True)


class FontMeta(AbstractMetaClass, WorkToyClass):
  """Symbolic class representation of font families"""

  _families = [
    'Arial',
    'Calibri',
    'Cambria',
    'Consolas',
    'Courier',
    'Impact',
    'Modern',
    'Tahoma',
    'Times New Roman',
    'Verdana',
  ]

  @classmethod
  def getFontFamilyNames(cls) -> list[str]:
    """Getter-function for font family names"""
    return cls._families

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases,
                  **kwargs) -> AbstractNameSpace:
    nameSpace = AbstractNameSpace()
    nameSpace |= {'getFontFamilyNames': mcls.getFontFamilyNames}
    nameSpace |= {'instanceDict' : {},
                  'instanceList' : [],
                  'fontName'     : None,
                  '__font_name__': None,
                  '__str__'      : lambda self: getattr(self, 'fontName'),
                  '__repr__'     : lambda self: getattr(self, 'fontName'), }
    return nameSpace

  def __new__(mcls, name: str, bases: Bases, nameSpace: AbstractNameSpace,
              **kwargs) -> type:
    return AbstractMetaClass.__new__(mcls, name, bases, nameSpace, **kwargs)

  def __init__(cls, name: str, bases: Bases, nameSpace: AbstractNameSpace,
               **kwargs) -> None:
    AbstractMetaClass.__init__(cls, name, bases, nameSpace, **kwargs)
    for fontName in cls.getFontFamilyNames():
      instance = cls(fontName, _allowCreate=True)
      cls.instanceDict |= {fontName: instance}
      cls.instanceList.append(instance)

  def __call__(cls, *args, **kwargs) -> Any:
    if kwargs.get('_allowCreate', False):
      return AbstractMetaClass.__call__(cls, *args, **kwargs)
    fontName = cls.maybeType(str, *args, )
    if fontName in cls.getFontFamilyNames():
      instanceDict = getattr(cls, 'instanceDict')
      return instanceDict.get(fontName, )
    raise KeyError

  def __iter__(cls) -> type:
    """Implementation"""
    setattr(cls, '__current_index__', 0)
    return cls

  def __next__(cls) -> Any:
    """Implementation"""
    __current_index__ = getattr(cls, '__current_index__', )
    setattr(cls, '__current_index__', __current_index__ + 1)
    instanceList = getattr(cls, 'instanceList', )
    if __current_index__ < len(instanceList):
      return instanceList[__current_index__]
    raise StopIteration

  def __str__(cls) -> str:
    """String representation"""
    return cls.__name__.upper()

  def __repr__(cls) -> str:
    """Code representation"""
    return '%s(%s)' % (cls.__name__, getattr(cls, 'fontName'))

  def __getattribute__(cls, key: str) -> Any:
    getFamilies = object.__getattribute__(cls, 'getFontFamilyNames')
    families = getFamilies()
    instanceDict = object.__getattribute__(cls, 'instanceDict')
    if key in families:
      return instanceDict[key]
    return object.__getattribute__(cls, key)

  def __getitem__(cls, fontName: str) -> Any:
    """Returns the instance matching the given name"""
    instanceList = getattr(cls, 'instanceList', None)
    if instanceList is None:
      raise TypeError
    for item in instanceList:
      if item == fontName:
        return item


class _FontFamily(str, WorkToyClass, metaclass=FontMeta):
  """WorkSide - Widgets - FontFamily
  Enum class representation of common classes."""

  def __new__(cls, *args, **kwargs) -> FontFamily:
    if args[0] in cls.getFontFamilyNames():
      out = str.__new__(str, args[0])
      return out


class FontFamily(_FontFamily):
  """WorkSide - Widgets - FontFamily
  Enum class representation of common classes."""

  def __init__(self, *args, **kwargs) -> None:
    WorkToyClass.__init__(self, *args, **kwargs)

  def __matmul__(self, other: QFont) -> QFont:
    """Changes the font family of other to self"""
    if isinstance(other, QFont):
      other.setFamily(self)
      return other
    return NotImplemented

  def __rmatmul__(self, other: QFont) -> QFont:
    """Same as above"""
    return self @ other
