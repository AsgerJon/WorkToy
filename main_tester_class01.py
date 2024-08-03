"""LMAO"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field, AttriBox
from worktoy.parse import maybe


class OwningClass:
  """This class uses 'property' to implement the 'name' attribute. """

  __fallback_number__ = 0
  __fallback_name__ = 'Unnamed'
  __inner_number__ = None
  __inner_name__ = None

  def __init__(self, *args, **kwargs) -> None:
    self.__inner_number__ = kwargs.get('number', None)
    self.__inner_name__ = kwargs.get('name', None)
    for arg in args:
      if isinstance(arg, int) and self.__inner_number__ is None:
        self.__inner_number__ = arg
      elif isinstance(arg, str) and self.__inner_name__ is None:
        self.__inner_name__ = arg

  @property
  def name(self) -> str:
    """Name property"""
    if self.__inner_name__ is None:
      return self.__fallback_name__
    return self.__inner_name__

  @name.setter
  def name(self, value: str) -> None:
    """Name setter"""
    self.__inner_name__ = value

  @name.deleter
  def name(self) -> None:
    """Name deleter"""
    del self.__inner_name__

  def _getNumber(self) -> int:
    """Number getter"""
    if self.__inner_number__ is None:
      return self.__fallback_number__
    return self.__inner_number__

  def _setNumber(self, value: int) -> None:
    """Number setter"""
    self.__inner_number__ = value

  def _delNumber(self) -> None:
    """Number deleter"""
    del self.__inner_number__

  number = property(_getNumber, _setNumber, _delNumber, doc='Number')


class Point:
  """This class uses the 'Field' descriptor to implement the coordinate
  attributes. """
  __x_value__ = None
  __y_value__ = None

  x = Field()
  y = Field()

  @x.GET
  def _getX(self) -> float:
    return self.__x_value__

  @x.SET
  def _setX(self, value: float) -> None:
    self.__x_value__ = value

  @y.GET
  def _getY(self) -> float:
    return self.__y_value__

  @y.SET
  def _setY(self, value: float) -> None:
    self.__y_value__ = value

  def __init__(self, *args, **kwargs) -> None:
    self.__x_value__ = kwargs.get('x', None)
    self.__y_value__ = kwargs.get('y', None)
    for arg in args:
      if isinstance(arg, int):
        arg = float(arg)
      if isinstance(arg, float):
        if self.__x_value__ is None:
          self.__x_value__ = arg
        elif self.__y_value__ is None:
          self.__y_value__ = arg
          break
    else:
      if self.__x_value__ is None:
        self.__x_value__, self.__y_value__ = 69., 420.
      elif self.__y_value__ is None:

        self.__y_value__ = 420.
