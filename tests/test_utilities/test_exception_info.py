"""
TestExceptionInfo tests 'ExceptionInfo' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import ExceptionInfo
from . import UtilitiesTest, Interrupt


class TestExceptionInfo(UtilitiesTest):
  """
  'ExceptionInfo' wraps a block expected to raise, records what the
  block raised against what was expected, and writes a report of the
  outcome. The tests pin each of the six outcomes the docstring lists,
  the propagation of a 'BaseException' that is no 'Exception', the two
  refusals of the constructor, and the string forms.
  """

  def test_no_expectation_no_exception(self) -> None:
    with ExceptionInfo() as info:
      pass
    self.assertFalse(info)
    self.assertIsNone(info.expectedExcType)
    self.assertIsNone(info.actualException)
    self.assertIsNone(info.actualExcType)
    self.assertEqual(info.expectedName, 'No Exception')
    self.assertEqual(info.actualName, 'No Exception')
    self.assertEqual(info.report, 'Exited without exception as expected!')

  def test_expected_but_nothing_raised(self) -> None:
    with ExceptionInfo(ValueError) as info:
      pass
    self.assertFalse(info)
    self.assertIs(info.expectedExcType, ValueError)
    self.assertEqual(info.expectedName, 'ValueError')
    self.assertEqual(info.actualName, 'No Exception')
    self.assertIn("Expected 'ValueError', but no exception", info.report)

  def test_exact_match_suppressed(self) -> None:
    with ExceptionInfo(ValueError) as info:
      raise ValueError('bad value')
    self.assertTrue(info)
    self.assertIsInstance(info.actualException, ValueError)
    self.assertIs(info.actualExcType, ValueError)
    self.assertEqual(info.actualName, 'ValueError')
    self.assertEqual(info.report,
                     "Caught 'ValueError' as expected: bad value")

  def test_subclass_match_suppressed(self) -> None:
    with ExceptionInfo(LookupError) as info:
      raise KeyError('missing')
    self.assertTrue(info)
    self.assertIs(info.actualExcType, KeyError)
    self.assertIn("'KeyError'", info.report)
    self.assertIn("a subclass of 'LookupError'", info.report)
    self.assertIn("'missing'", info.report)

  def test_wrong_type_suppressed(self) -> None:
    with ExceptionInfo(ValueError) as info:
      raise TypeError('wrong kind')
    self.assertTrue(info)
    self.assertIs(info.actualExcType, TypeError)
    self.assertIn("Expected 'ValueError'", info.report)
    self.assertIn("'TypeError' instead: wrong kind", info.report)

  def test_no_expectation_propagates(self) -> None:
    info = ExceptionInfo()
    with self.assertRaises(ValueError) as context:
      with info:
        raise ValueError('unexpected')
    self.assertEqual(str(context.exception), 'unexpected')
    self.assertTrue(info)
    self.assertIsInstance(info.actualException, ValueError)
    self.assertEqual(info.report, '')

  def test_base_exception_propagates(self) -> None:
    info = ExceptionInfo(ValueError)
    with self.assertRaises(Interrupt) as context:
      with info:
        raise Interrupt()
    self.assertEqual(context.exception.args, ())
    self.assertTrue(info)
    self.assertIs(info.actualExcType, Interrupt)
    self.assertIn("Received BaseException of type 'Interrupt'", info.report)
    self.assertIn('must always propagate', info.report)

  def test_instance_taken_as_its_type(self) -> None:
    info = ExceptionInfo(ValueError('from instance'))
    self.assertIs(info.expectedExcType, ValueError)
    self.assertEqual(info.expectedName, 'ValueError')

  def test_not_an_exception_refused(self) -> None:
    with self.assertRaises(TypeError) as context:
      ExceptionInfo(42)
    self.assertIn("got 'int'", str(context.exception))

  def test_class_not_an_exception_refused(self) -> None:
    with self.assertRaises(TypeError) as context:
      ExceptionInfo(str)
    self.assertIn("got 'type'", str(context.exception))

  def test_base_exception_not_expectable(self) -> None:
    with self.assertRaises(TypeError) as context:
      ExceptionInfo(Interrupt)
    self.assertIn("cannot expect 'Interrupt'", str(context.exception))

  def test_typical_exceptions_all_caught(self) -> None:
    for excType in self.exceptions:
      with self.subTest(excType=excType):
        with ExceptionInfo(excType) as info:
          raise excType('typical')
        self.assertIs(info.actualExcType, excType)
        self.assertIn('as expected', info.report)

  def test_str(self) -> None:
    with ExceptionInfo(ValueError) as info:
      raise KeyError('k')
    expected = "<ExceptionInfo expected='ValueError' actual='KeyError'>"
    self.assertEqual(str(info), expected)
    self.assertEqual(str(ExceptionInfo()), (
      "<ExceptionInfo expected='No Exception' actual='No Exception'>"
    ))

  def test_repr(self) -> None:
    self.assertEqual(repr(ExceptionInfo()), 'ExceptionInfo()')
    self.assertEqual(repr(ExceptionInfo(OSError)), 'ExceptionInfo(OSError)')

  def test_enter_returns_self(self) -> None:
    info = ExceptionInfo()
    self.assertIs(info.__enter__(), info)
    self.assertTrue(info.__exit__(None, None, None))
