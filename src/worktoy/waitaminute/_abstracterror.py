"""AbstractError serves as the baseclass of the custom exceptions"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from worktoy.core import BedrockMeta

if TYPE_CHECKING:
  from worktoy.worktype import CallMeMaybe


class AbstractError(Exception, metaclass=BedrockMeta):
  """AbstractError serves as the baseclass of the custom exceptions"""

  _monoSpace = None

  @classmethod
  def _createMonoSpace(cls, ) -> None:
    """Creator-function for the monoSpace."""
    from worktoy.core import monoSpace
    cls._monoSpace = monoSpace

  @classmethod
  def _getMonoSpace(cls, **kwargs) -> CallMeMaybe:
    """Getter-function for the monoSpace"""
    if cls._monoSpace is None and kwargs.get('recursion', False):
      raise RecursionError('lol')
    if cls._monoSpace is None:
      cls._createMonoSpace()
      return cls._getMonoSpace(recursion=True)
    return cls._monoSpace

  @classmethod
  def monoSpace(cls, msg: str, newLine: str = None) -> str:
    """Locally imported version."""
    return AbstractError._getMonoSpace()(msg, newLine)

  def __str__(self) -> str:
    """String Representation"""
    header = """%s raised by %s!""" % (
      self._getErrorName(), self._getObject())
    body = """Explanation: %s""" % (self._getMessage())
    msg = '%s<br>%s' % (header, body)
    return self.monoSpace(msg)

  def __init__(self, obj: object = None, *__, **kwargs) -> None:
    self._object = obj
    Exception.__init__(self, self._getMessage())

  def __repr__(self) -> str:
    """Code Representation"""
    return self.__class__.__qualname__

  def _getObject(self) -> object:
    """Getter-function for the object within which the error is raised."""
    return self._object

  def _getClass(self) -> type:
    """Getter-function for the class of the object"""
    return self._getObject().__class__

  def _getErrorName(self) -> str:
    """Getter-function for the name of the custom exception"""
    return self.__class__.__qualname__

  @abstractmethod
  def _getMessage(self) -> str:
    """Getter-function for the customized message. Subclasses must
    implement this method. Do not call monoSpace on the message. This
    happens in the __str__ method."""
