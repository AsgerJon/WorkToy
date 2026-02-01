"""
ExceptionInfo provides a context manager for capturing and inspecting
exceptions. The motivating use case is when debugging scenarios where in
the testing framework, and expected exception fails to raise or does
raise, but is of unexpected 'Exception' subclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Type, Self, Optional, Any


class _Exc:
  """
  Private descriptor exposing exception class name for exception
  attributes. Falls back to 'No Exception' when absent.
  """

  __slot_name__ = None
  __field_name__ = None
  __field_owner__ = None

  def __init__(self, name: str) -> None:
    self.__slot_name__ = name

  def __set_name__(self, owner: type, name: str) -> None:
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self
    excAttr = getattr(instance, self.__slot_name__, )
    if isinstance(excAttr, type):
      return excAttr
    if isinstance(excAttr, Exception):
      return type(excAttr)
    return 'No Exception'


class _ExcName(_Exc):
  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self
    excAttr = getattr(instance, self.__slot_name__, )
    if isinstance(excAttr, type):
      return excAttr.__name__
    if isinstance(excAttr, Exception):
      return type(excAttr).__name__
    return 'No Exception'


class _ExcObject(_Exc):
  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self
    excAttr = getattr(instance, self.__slot_name__, )
    if isinstance(excAttr, BaseException):
      return excAttr
    return None


class ExceptionInfo:
  """
  ExceptionInfo provides a context manager for capturing and inspecting
  exceptions. The motivating use case is when debugging scenarios where in
  the testing framework, and expected exception fails to raise or does
  raise, but is of unexpected 'Exception' subclass.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Annotations
  __expected_exception__: Optional[Type[Exception]]
  __actual_exception__: Optional[Exception]
  report: str

  #  Public Variables
  expectedExcType = _Exc('__expected_exception__')
  actualExcType = _Exc('__actual_exception__')
  actualException = _ExcObject('__actual_exception__')
  expectedName = _ExcName('__expected_exception__')
  actualName = _ExcName('__actual_exception__')

  __slots__ = ('__expected_exception__', '__actual_exception__', 'report',)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, expExc: Type[Exception] = None, ) -> None:
    if isinstance(expExc, (type, BaseException)):
      self.__expected_exception__ = expExc
    else:
      self.__expected_exception__ = None
    self.__actual_exception__ = None
    self.report = ''

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __enter__(self, ) -> Self:
    return self

  def __exit__(self, _, excValue: Exception, __) -> bool:
    self.__actual_exception__ = excValue
    if not isinstance(excValue, Exception):
      if isinstance(excValue, BaseException):
        self.report = self._handleBaseException(excValue)
        return False  # BaseException must *always* propagate
    if excValue is None:
      self.report = self._handleNoException()
      return True
    if self.__expected_exception__ is None:
      return False  # Did not expect an exception, let it propagate
    if type(excValue) is self.expectedExcType:
      self.report = self._handleExpectedException()
      return True
    if isinstance(excValue, self.expectedExcType):
      self.report = self._handleSubclassException()
      return True
    self.report = self._handleUnexpectedException()
    return True

  def __str__(self) -> str:
    clsName = type(self).__name__
    infoSpec = """<%s expected='%s' actual='%s'>"""
    info = infoSpec % (clsName, self.expectedName, self.actualName)
    return textFmt(info)

  def __repr__(self, ) -> str:
    if self.__expected_exception__ is None:
      return textFmt("""%s()""" % (type(self).__name__,))
    infoSpec = """%s(%s)"""
    clsName = type(self).__name__
    info = infoSpec % (clsName, self.expectedName)
    return textFmt(info)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _handleBaseException(baseExp: BaseException) -> str:
    infoSpec = """Received BaseException of type '%s', which is not a 
    subclass of 'Exception'. These exceptions must always propagate!"""
    excType = type(baseExp).__name__
    info = infoSpec % (excType,)
    return textFmt(info)

  def _handleNoException(self) -> str:
    infoSpec = """Expected '%s', but no exception was raised!"""
    excType = self.expectedName
    info = infoSpec % (excType,)
    return textFmt(info)

  def _handleSubclassException(self, ) -> str:
    infoSpec = """Expected '%s' and received exception of type: 
    '%s', a subclass of '%s': '%s'"""
    expName = self.expectedName
    excStr = str(self.actualException)
    info = infoSpec % (expName, self.actualName, expName, excStr)
    return textFmt(info)

  def _handleUnexpectedException(self, ) -> str:
    infoSpec = """Expected '%s', but received exception of type '%s' 
    instead: %s"""
    excStr = str(self.actualException)
    info = infoSpec % (self.expectedName, self.actualName, excStr,)
    return textFmt(info)

  def _handleExpectedException(self, ) -> str:
    infoSpec = """Caught '%s' as expected: %s"""
    info = infoSpec % (self.expectedName, str(self.actualException))
    return textFmt(info)
