"""NameSpaceError is a custom exception raised when the __prepare__ method
on a metaclass cannot be validated. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, MutableMapping

from worktoy.waitaminute import AbstractError

Bases = tuple[type]
Map = MutableMapping[str, Any]


class NameSpaceError(AbstractError):
  """NameSpaceError is a custom exception raised when the __prepare__ method
  on a metaclass cannot be validated. """

  def __init__(self,
               nameSpaceClass: type,
               originClass: type,
               exception: Exception) -> None:
    self._nameSpaceClass = nameSpaceClass
    self._object = originClass
    self._exception = exception
    AbstractError.__init__(self, self._object)

  def _getMessage(self) -> str:
    """Getter-function for message"""
    header = ('Failed to validate class %s as a class suitable for use as '
              'namespace in a metaclass.' %
              self._nameSpaceClass.__qualname__)
    body = 'During validation, the following exception were returned: %s' % (
      self._exception.__class__.__qualname__)
    return '%s<br>%s' % (header, body)

  def __repr__(self) -> str:
    """Code Representation"""
    cls = self.__class__.__qualname__
    nameSpace = self._nameSpaceClass.__qualname__
    exception = self._exception.__qualname__
    return '%s(%s, %s)' % (cls, nameSpace, exception)
