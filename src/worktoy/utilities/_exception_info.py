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
  from typing import Type, Self, Optional


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

  #  Public Variables
  expectedException: Type[Exception]
  actualException: Optional[Exception]
  report: str
  __slots__ = ('expectedException', 'actualException', 'report',)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, expExc: Type[Exception], ) -> None:
    self.expectedException = expExc
    self.actualException = None
    self.report = ''

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __enter__(self, ) -> Self:
    return self

  def __exit__(self, _, excValue: Exception, __) -> bool:
    self.actualException = excValue
    if not isinstance(excValue, Exception):
      if isinstance(excValue, BaseException):
        self.report = self._handleBaseException(excValue)
        return False  # BaseException must *always* propagate
    if excValue is None:
      self.report = self._handleNoException()
      return True
    if isinstance(excValue, self.expectedException):
      self.report = self._handleExpectedException(excValue)
      return True
    self.report = self._handleUnexpectedException(excValue)
    return True

  def __str__(self) -> str:
    clsName = type(self).__name__
    expected = self.expectedException.__name__
    if self.actualException is None:
      infoSpec = """<%s expected='%s'>"""
    else:
      infoSpec = """<%s expected='%s' actual='%s'>"""
    if self.actualException is None:
      info = infoSpec % (clsName, expected)
    else:
      actual = type(self.actualException).__name__
      info = infoSpec % (clsName, expected, actual)
    return textFmt(info)

  def __repr__(self, ) -> str:
    infoSpec = """%s(%s)"""
    clsName = type(self).__name__
    expected = self.expectedException.__name__
    info = infoSpec % (clsName, expected)
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
    infoSpec = """Expected exception of type '%s', but no exception was 
    raised!"""
    excType = self.expectedException.__name__
    info = infoSpec % (excType,)
    return textFmt(info)

  def _handleUnexpectedException(self, excValue: Exception) -> str:
    infoSpec = """Expected exception of type '%s', but received exception 
    of type '%s' instead: %s"""
    expected = self.expectedException.__name__
    actual = type(excValue).__name__
    excMsg = str(excValue)
    info = infoSpec % (expected, actual, excMsg)
    return textFmt(info)

  @staticmethod
  def _handleExpectedException(excValue: Exception) -> str:
    infoSpec = """Caught '%s' as expected: %s"""
    excType = type(excValue).__name__
    excMsg = str(excValue)
    info = infoSpec % (excType, excMsg)
    return textFmt(info)
