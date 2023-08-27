"""WorkToy - Core - List
Inline descriptor specifically for list variables. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from worktoy.core import Function
from worktoy.fields import AbstractDescriptor


class ListDescriptor(AbstractDescriptor, ):
  """WorkToy - Core - List
  Inline descriptor specifically for list variables. """

  __key__ = 'LIST'

  def __init__(self, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self.setSourceClass(list)
    self.setDefaultValue([None, ])

  def __get__(self, obj: object, cls: type) -> list:
    """Getter"""
    value = AbstractDescriptor.__get__(self, obj, cls)
    if isinstance(value, list):
      return value
    raise TypeError

  def __set__(self, *_) -> Never:
    """Illegal setter"""
    raise TypeError

  def __delete__(self, *_) -> Never:
    """Illegal deleter"""
    raise TypeError

  def sourceInstanceFactory(self) -> Function:
    """Factory for source instance creators."""
    source = self.getSourceClass()

    def sourceInstanceCreator(cls: type, obj: object) -> object:
      """Source instance creator"""
      return [None, ]

    return sourceInstanceCreator


LIST = ListDescriptor
