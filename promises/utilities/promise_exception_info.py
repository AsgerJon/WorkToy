"""
PromiseExceptionInfo promises 'ExceptionInfo' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import ExceptionInfo


class PromiseExceptionInfo(TestCase):
  """
  'ExceptionInfo(expected)' wraps a block expected to raise and records
  what happened. With an expected type, the block's exception is
  recorded and suppressed, whether it is of that type, a subclass, or
  another type entirely, and a block raising nothing exits normally.
  Without one, a block raising nothing exits normally and an exception
  propagates with 'report' left empty. A 'BaseException' that is no
  'Exception', such as 'KeyboardInterrupt', always propagates. The
  record is 'expectedExcType', 'actualException', 'actualExcType',
  'expectedName', 'actualName', both 'No Exception' when there is none,
  and 'report', a summary for a person to read. Source: the
  'ExceptionInfo' docstring.
  """

  def test_clean_exit(self) -> None:
    with ExceptionInfo() as info:
      pass
    self.assertIsNone(info.expectedExcType)
    self.assertIsNone(info.actualException)
    self.assertIsNone(info.actualExcType)
    self.assertEqual(info.expectedName, 'No Exception')
    self.assertEqual(info.actualName, 'No Exception')
    self.assertTrue(info.report)

  def test_expected_raised(self) -> None:
    error = ValueError('bad value')
    with ExceptionInfo(ValueError) as info:
      raise error
    self.assertIs(info.expectedExcType, ValueError)
    self.assertIs(info.actualException, error)
    self.assertIs(info.actualExcType, ValueError)
    self.assertEqual(info.expectedName, 'ValueError')
    self.assertEqual(info.actualName, 'ValueError')
    self.assertTrue(info.report)

  def test_subclass_raised(self) -> None:
    with ExceptionInfo(LookupError) as info:
      raise KeyError('missing')
    self.assertIs(info.expectedExcType, LookupError)
    self.assertIs(info.actualExcType, KeyError)
    self.assertTrue(info.report)

  def test_other_type_raised(self) -> None:
    with ExceptionInfo(ValueError) as info:
      raise KeyError('missing')
    self.assertIs(info.expectedExcType, ValueError)
    self.assertIs(info.actualExcType, KeyError)
    self.assertTrue(info.report)

  def test_expected_missing(self) -> None:
    with ExceptionInfo(ValueError) as info:
      pass
    self.assertIs(info.expectedExcType, ValueError)
    self.assertIsNone(info.actualException)
    self.assertEqual(info.actualName, 'No Exception')
    self.assertTrue(info.report)

  def test_unexpected_propagates(self) -> None:
    info = ExceptionInfo()
    with self.assertRaises(KeyError):
      with info:
        raise KeyError('missing')
    self.assertEqual(info.report, '')

  def test_base_exception_propagates(self) -> None:
    info = ExceptionInfo(Exception)
    with self.assertRaises(KeyboardInterrupt):
      with info:
        raise KeyboardInterrupt
    self.assertTrue(info.report)

  def test_expected_instance(self) -> None:
    with ExceptionInfo(ValueError('template')) as info:
      raise ValueError('bad value')
    self.assertIs(info.expectedExcType, ValueError)
    self.assertIs(info.actualExcType, ValueError)
