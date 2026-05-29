"""
ExceptionInfo is a context manager for capturing and inspecting an
expected exception.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import textFmt, QuickDesc

if TYPE_CHECKING:  # pragma: no cover
  from typing import Type, Self, Optional, TypeAlias

  ExcType: TypeAlias = Type[Exception]

_NO_EXC = 'No Exception'


class ExceptionInfo:
  """Context manager for capturing and inspecting exceptions.

  Wrap a block of code that is expected to raise. The expected
  exception class is passed to the constructor. On exit, the
  raised exception (if any) is recorded and 'report' is set, with
  these outcomes:

  - no expected type set, no exception: clean-exit report; the
    block exits normally.
  - expected type set, no exception: missing-exception report.
  - expected type set, exact type raised: match report; the
    exception is suppressed.
  - expected type set, subclass raised: subclass-match report; the
    exception is suppressed.
  - expected type set, different type raised: wrong-type report;
    the exception is also suppressed.
  - no expected type set, an exception raised: the exception
    propagates and 'report' is left empty.

  'BaseException' subclasses that are not 'Exception' subclasses
  (e.g. 'KeyboardInterrupt') always propagate; 'report' notes this.

  Attributes
  ----------
  expectedExcType : type or None
      The expected exception class, or 'None' if none was
      requested.
  actualException : BaseException or None
      The raised exception instance, if any.
  actualExcType : type or None
      The class of the raised exception.
  expectedName : str
      Name of the expected exception class, or 'No Exception'.
  actualName : str
      Name of the raised exception class, or 'No Exception'.
  report : str
      Human-readable summary of what happened in the block.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Annotations
  __expected_exception__: Optional[Type[BaseException]]
  __actual_exception__: Optional[BaseException]
  __expected_name__: str
  __actual_exc_type__: Optional[type]
  __actual_name__: str
  __report__: str

  #  Public Variables
  expectedExcType: QuickDesc[Exception] = QuickDesc('__expected_exception__')
  actualException: QuickDesc[Exception] = QuickDesc('__actual_exception__')
  actualExcType: QuickDesc[ExcType] = QuickDesc('__actual_exc_type__')
  expectedName: QuickDesc[str] = QuickDesc('__expected_name__')
  actualName: QuickDesc[str] = QuickDesc('__actual_name__')
  report: QuickDesc[str] = QuickDesc('__report__')

  __slots__ = (
    '__expected_exception__',
    '__actual_exception__',
    '__expected_name__',
    '__actual_exc_type__',
    '__actual_name__',
    '__report__',
  )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _setActual(self, exc: Optional[BaseException]) -> None:
    """Update the actual-exception slot trio in lock-step."""
    self.__actual_exception__ = exc
    excType = type(exc) if exc is not None else None
    self.__actual_exc_type__ = excType
    self.__actual_name__ = (
      excType.__name__ if excType is not None else _NO_EXC
    )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, expExc: Type[BaseException] = None) -> None:
    if expExc is None:
      expectedCls = None
    elif isinstance(expExc, type) and issubclass(expExc, BaseException):
      expectedCls = expExc
    elif isinstance(expExc, BaseException):
      expectedCls = type(expExc)
    else:
      info = """'expExc' must be a 'BaseException' subclass or
      instance; got '%s'""" % type(expExc).__name__
      raise TypeError(textFmt(info))
    self.__expected_exception__ = expectedCls
    self.__expected_name__ = (
      expectedCls.__name__ if expectedCls is not None else _NO_EXC
    )
    self._setActual(None)
    self.__report__ = ''

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __enter__(self) -> Self:
    return self

  def __exit__(self, _, excValue, __) -> bool:
    self._setActual(excValue)
    expected = self.__expected_exception__
    if not isinstance(excValue, Exception):
      if isinstance(excValue, BaseException):
        self.__report__ = self._handleBaseException(excValue)
        return False  # BaseException must always propagate
    if excValue is None:
      if expected is None:
        self.__report__ = self._handleWell()
      else:
        self.__report__ = self._handleNoException()
      return True
    if expected is None:
      return False  # Did not expect an exception; let it propagate
    if type(excValue) is expected:
      self.__report__ = self._handleExpectedException()
      return True
    if isinstance(excValue, expected):
      self.__report__ = self._handleSubclassException()
      return True
    self.__report__ = self._handleUnexpectedException()
    return True

  def __str__(self) -> str:
    info = """<%s expected='%s' actual='%s'>""" % (
      type(self).__name__, self.expectedName, self.actualName,
    )
    return textFmt(info)

  def __repr__(self) -> str:
    if self.__expected_exception__ is None:
      return '%s()' % type(self).__name__
    return '%s(%s)' % (type(self).__name__, self.expectedName)

  def __bool__(self) -> bool:
    return self.__actual_exception__ is not None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _handleBaseException(baseExp: BaseException) -> str:
    info = """Received BaseException of type '%s', which is not a
    subclass of 'Exception'. These exceptions must always
    propagate!""" % type(baseExp).__name__
    return textFmt(info)

  @staticmethod
  def _handleWell() -> str:
    return 'Exited without exception as expected!'

  def _handleNoException(self) -> str:
    info = """Expected '%s', but no exception was raised!""" \
           % (self.expectedName,)
    return textFmt(info)

  def _handleSubclassException(self) -> str:
    info = """Expected '%s' and received exception of type: '%s',
    a subclass of '%s': '%s'""" % (
      self.expectedName, self.actualName, self.expectedName,
      str(self.actualException),
    )
    return textFmt(info)

  def _handleUnexpectedException(self) -> str:
    info = """Expected '%s', but received exception of type '%s'
    instead: %s""" % (
      self.expectedName, self.actualName,
      str(self.actualException),
    )
    return textFmt(info)

  def _handleExpectedException(self) -> str:
    info = """Caught '%s' as expected: %s""" % (
      self.expectedName, str(self.actualException),
    )
    return textFmt(info)
