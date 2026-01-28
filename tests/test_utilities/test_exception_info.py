"""
TestExceptionInfo module tests the ExceptionInfo class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import ExceptionInfo
from . import UtilitiesTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class _TestBaseException(BaseException):
  """
  This subclass of 'BaseException' is used only for testing purposes.
  Generally speaking, 'BaseException' should not be subclassed directly
  and it should most definitely *never* be caught in application code.
  """
  pass


class TestExceptionInfo(UtilitiesTest):
  """Tests the ExceptionInfo class."""

  exceptions = None

  @classmethod
  def setUpClass(cls) -> None:
    super().setUpClass()
    cls.exceptions = (
      ValueError,
      KeyError,
      IndexError,
      RuntimeError,
      OSError,
      PermissionError,
      TypeError,
      FileExistsError,
      FileNotFoundError
    )

  def test_no_context(self, ) -> None:
    """
    Testing 'ExceptionInfo' outside any context manager.
    """
    for excType in self.exceptions:
      info = ExceptionInfo(excType)
      self.assertIsNone(info.actualException)
      self.assertIs(info.expectedException, excType)
      infoStr = str(info)
      expectedSpec = """<%s expected='%s'>"""
      clsName, escType = type(info).__name__, excType.__name__
      expectedStr = expectedSpec % (clsName, escType)
      self.assertEqual(infoStr, expectedStr)

  def test_no_exception(self, ) -> None:
    """
    Testing 'ExceptionInfo' when no exception is raised.
    """
    for excType in self.exceptions:
      with ExceptionInfo(excType) as info:
        pass
      self.assertIsNone(info.actualException)
      self.assertIs(info.expectedException, excType)
      infoStr = str(info)
      expectedSpec = """<%s expected='%s'>"""
      clsName, escType = type(info).__name__, excType.__name__
      expectedStr = expectedSpec % (clsName, escType)
      self.assertEqual(infoStr, expectedStr)
      infoRepr = repr(info)
      expectedRepr = """%s(%s)""" % (clsName, escType)
      self.assertEqual(infoRepr, expectedRepr)

  def test_expected_exception(self, ) -> None:
    """
    Testing 'ExceptionInfo' when the expected exception is raised.
    """
    for excType in self.exceptions:
      try:
        with ExceptionInfo(excType) as info:
          raise excType("Test exception")
      finally:
        self.assertIsInstance(info.actualException, excType)
        self.assertIs(info.expectedException, excType)
        infoStr = str(info)
        expectedSpec = """<%s expected='%s' actual='%s'>"""
        clsName = type(info).__name__
        escType = excType.__name__
        expectedStr = expectedSpec % (clsName, escType, escType)
        self.assertEqual(infoStr, expectedStr)
        infoRepr = repr(info)
        expectedRepr = """%s(%s)""" % (clsName, escType)
        self.assertEqual(infoRepr, expectedRepr)

  def test_unexpected_exception(self, ) -> None:
    """
    Testing 'ExceptionInfo' when an unexpected exception is raised.
    """
    for expected in self.exceptions:
      for actual in self.exceptions:
        if actual is expected:
          continue
        try:
          with ExceptionInfo(expected) as info:
            raise actual("Test exception")
        finally:
          self.assertIsInstance(info.actualException, actual)
          infoStr = str(info)
          expectedSpec = """<%s expected='%s' actual='%s'>"""
          clsName = type(info).__name__
          escExpected = expected.__name__
          escActual = actual.__name__
          expectedStr = expectedSpec % (clsName, escExpected, escActual)
          self.assertEqual(infoStr, expectedStr)
          infoRepr = repr(info)
          expectedRepr = """%s(%s)""" % (clsName, escExpected)
          self.assertEqual(infoRepr, expectedRepr)

  def test_base_exception(self, ) -> None:
    """
    Testing 'ExceptionInfo' when a 'BaseException' is raised.
    """
    for excType in self.exceptions:
      with self.assertRaises(_TestBaseException):
        try:
          with ExceptionInfo(excType) as info:
            raise _TestBaseException
        finally:
          self.assertIsInstance(info.actualException, _TestBaseException)
          self.assertIs(info.expectedException, excType)
          infoStr = str(info)
          expectedSpec = """<%s expected='%s' actual='%s'>"""
          clsName = type(info).__name__
          escType = excType.__name__
          actualType = _TestBaseException.__name__
          expectedStr = expectedSpec % (clsName, escType, actualType)
          self.assertEqual(infoStr, expectedStr)
          infoRepr = repr(info)
          expectedRepr = """%s(%s)""" % (clsName, escType)
          self.assertEqual(infoRepr, expectedRepr)
