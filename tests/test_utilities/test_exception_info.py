"""
TestExceptionInfo module tests the ExceptionInfo class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import ExceptionInfo
from worktoy.utilities._exception_info import _Exc, _ExcObject, _ExcName
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

  def test_no_context(self, ) -> None:
    """
    Testing 'ExceptionInfo' outside any context manager.
    """
    for excType in self.exceptions:
      info = ExceptionInfo(excType)
      self.assertIsNone(info.actualException)
      self.assertIs(info.expectedExcType, excType)
      infoStr = str(info)
      infoRepr = repr(info)
      self.assertIn(excType.__name__, infoStr)
      self.assertIn(excType.__name__, infoRepr)

  def test_no_exception(self, ) -> None:
    """
    Testing 'ExceptionInfo' when no exception is raised.
    """
    for excType in self.exceptions:
      with ExceptionInfo(excType) as info:
        pass
      self.assertIsNone(info.actualException)
      self.assertIs(info.expectedExcType, excType)
      infoStr = """<%s expected='%s' actual='%s'>"""
      clsName = type(info).__name__
      expectedStr = infoStr % (clsName, info.expectedName, info.actualName)
      self.assertEqual(expectedStr, str(info))
      expectedRepr = """%s(%s)""" % (clsName, info.expectedName)
      self.assertEqual(expectedRepr, repr(info))

  def test_subclass_exception(self, ) -> None:
    """
    Testing 'ExceptionInfo' when a subclass of the expected exception is
    raised.
    """
    subNames = str.split("""Never gonna give you up""")
    info = None
    for excType in self.exceptions:
      for name in subNames:
        Sub = type(str.capitalize(name), (excType,), dict())
        try:
          with ExceptionInfo(excType) as info:
            raise Sub
        finally:
          self.assertIsInstance(info.actualException, Sub)
          self.assertIsInstance(info.actualException, excType)
          self.assertIs(info.expectedExcType, excType)
          strSpec = """<%s expected='%s' actual='%s'>"""
          clsName = type(info).__name__
          expStr = strSpec % (clsName, info.expectedName, info.actualName)
          reprSpec = """%s(%s)"""
          expectedRepr = reprSpec % (clsName, info.expectedName)
          self.assertEqual(str(info), expStr)
          self.assertEqual(repr(info), expectedRepr)

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
        self.assertIs(info.expectedExcType, excType)
        strSpec = """<%s expected='%s' actual='%s'>"""
        reprSpec = """%s(%s)"""
        clsName = type(info).__name__
        expStr = strSpec % (clsName, info.expectedName, info.actualName)
        expRepr = reprSpec % (clsName, info.expectedName)
        self.assertEqual(str(info), expStr)
        self.assertEqual(repr(info), expRepr)

  def test_wrong_exception_type(self, ) -> None:
    """
    Testing 'ExceptionInfo' when an unexpected exception is raised.
    """
    for expected in self.exceptions:
      for actual in self.exceptions:
        if issubclass(actual, expected) or issubclass(expected, actual):
          continue
        try:
          with ExceptionInfo(expected) as info:
            raise actual("Test exception")
        finally:
          self.assertIsInstance(info.actualException, actual)
          strSpec = """<%s expected='%s' actual='%s'>"""
          reprSpec = """%s(%s)"""
          clsName = type(info).__name__
          expStr = strSpec % (clsName, info.expectedName, info.actualName)
          expRepr = reprSpec % (clsName, info.expectedName)
          self.assertIs(info.expectedExcType, expected)
          self.assertEqual(str(info), expStr)
          self.assertEqual(repr(info), expRepr)
          self.assertNotIsInstance(info.actualException, expected)

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
          self.assertIsInstance(info.actualException, BaseException)
          self.assertIs(info.expectedExcType, excType)
          strSpec = """<%s expected='%s' actual='%s'>"""
          reprSpec = """%s(%s)"""
          clsName = type(info).__name__
          expStr = strSpec % (clsName, info.expectedName, info.actualName)
          expRepr = reprSpec % (clsName, info.expectedName)
          self.assertEqual(str(info), expStr)
          self.assertEqual(repr(info), expRepr)

  def test_descriptor_objects(self, ) -> None:
    """
    Testing the descriptor objects on the ExceptionInfo class.
    """
    self.assertIsInstance(ExceptionInfo.expectedExcType, _Exc)
    self.assertIsInstance(ExceptionInfo.actualExcType, _Exc)
    self.assertIsInstance(ExceptionInfo.actualException, _ExcObject)
    self.assertIsInstance(ExceptionInfo.expectedName, _ExcName)
    self.assertIsInstance(ExceptionInfo.actualName, _ExcName)

  def test_no_expections(self, ) -> None:
    """
    Testing ExceptionInfo on no exceptions.
    """
    with ExceptionInfo() as info:
      pass
    self.assertIsNone(info.actualException)
    self.assertEqual('ExceptionInfo()', repr(info))

  def test_from_exception_instance(self) -> None:
    """
    Testing ExceptionInfo from an exception instance rather than exception
    type.
    """
    for excType in self.exceptions:
      try:
        raise excType()
      except Exception as exception:
        with ExceptionInfo(exception) as info:  # noqa
          pass
        self.assertIsInstance(exception, excType)
        self.assertIs(info.expectedExcType, excType)

  def test_exception_type_gymnastics(self, ) -> None:
    """
    Testing the descriptor gymnastics of ExceptionInfo.
    """

    info = ExceptionInfo()
    susExc = """I'm an error, trust me bro!"""
    setattr(info, '__expected_exception__', susExc)
    self.assertEqual(info.expectedExcType, 'No Exception')
    setattr(info, '__actual_exception__', susExc)
    self.assertEqual(info.actualExcType, 'No Exception')
    self.assertIsNone(info.actualException)

  def test_unexpected_exception(self, ) -> None:
    """
    Testing exceptions raised when no exception is expected.
    """
    for excType in self.exceptions:
      try:
        with ExceptionInfo() as info:
          raise excType()
      except Exception as exception:
        self.assertIsInstance(exception, excType)
        self.assertIsNone(info.__expected_exception__)
        self.assertIs(info.actualExcType, excType)
        self.assertIs(info.actualException, exception)

  def test_well(self) -> None:
    """
    Testing the case where no exception is expected or raised.
    """
    with ExceptionInfo() as info:
      pass
    self.assertIsNone(info.actualException)
    self.assertIsNone(info.__expected_exception__)
    self.assertIn('Exited without exception as expected', info.report)
