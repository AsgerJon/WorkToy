"""__ExceptionCorePropertiesProperties provides the properties on the
_ExceptionCoreProperties"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any, NoReturn, Never

from worktoy.core import maybe, maybeType, searchKeys


class _ExceptionCoreProperties:
  """Properties for custom exceptions."""

  @classmethod
  @abstractmethod
  def yoDawg(cls, *args, **kwargs) -> Any:
    """Heard you like ReadOnlyError, so we put a ReadOnlyError
      in your ReadOnlyError!"""

  def __init__(self, *args, **kwargs) -> None:
    cmtKwarg = searchKeys('cmt', 'comment') @ str >> kwargs
    cmtArg = maybeType(str, *args)
    cmtDefault = None
    self._comment = maybe(cmtKwarg, cmtArg, cmtDefault)
    self._msg = None
    self._callerClass = None
    self._callerFunction = None
    self._callerMethod = None

  def _getClass(self, ) -> Any:
    """Getter-function for class"""
    return maybe('%s' % (self.__class__.__name__), '**INSCLASS**')

  def _setClass(self, *_) -> Any:
    """Setter deleter function"""
    _ExceptionCoreProperties.yoDawg('callerClass')

  def _delClass(self) -> Any:
    """Illegal deleter function"""
    _ExceptionCoreProperties.yoDawg('callerClass')

  def _getCallerFunction(self, ) -> Any:
    """Getter-function for caller function"""
    return maybe(self._callerFunction, '**FUNC**')

  def _setCallerFunction(self, *_) -> Any:
    """Setter setter function"""
    _ExceptionCoreProperties.yoDawg('func')

  def _delCallerFunction(self) -> Any:
    """Illegal deleter function"""
    _ExceptionCoreProperties.yoDawg('func')

  def _getCallerMethod(self, ) -> Any:
    """Getter-function for caller function"""
    return maybe(self._callerMethod, '**CALL**')

  def _setCallerMethod(self, *_) -> Any:
    """Setter setter function"""
    _ExceptionCoreProperties.yoDawg('meth')

  def _delCallerMethod(self) -> Any:
    """Illegal deleter function"""
    _ExceptionCoreProperties.yoDawg('meth')

  @abstractmethod
  def createMessage(self) -> NoReturn:
    """Creator-function for the message"""

  def _getMsg(self, ) -> str:
    """Getter-function for msg"""
    if self._msg is None:
      if self.createMessage():
        return maybe(self._msg, 'MSG UNDEFINED')
      return 'MSG UNDEFINED'
    return maybe(self._msg, 'MSG UNDEFINED')

  def _setMsg(self, message: str) -> NoReturn:
    """Setter-function function"""
    self._msg = message

  def _delMsg(self) -> Never:
    """Illegal deleter function"""
    _ExceptionCoreProperties.yoDawg('meth')

  insClass = property(_getClass, _setClass, _delClass)
  meth = property(_getCallerMethod, _setCallerMethod, _delCallerMethod)
  func = property(_getCallerFunction, _setCallerFunction, _delCallerFunction)
  msg = property(_getMsg, _setMsg, _delMsg)
