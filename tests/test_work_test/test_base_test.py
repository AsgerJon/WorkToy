"""
TestBaseTest tests the 'BaseTest' class of the 'worktoy.work_test' package.
"Who tests the testers?" - "This class does."
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestBaseTest(BaseTest):
  """
  TestBaseTest tests the 'BaseTest' class of the 'worktoy.work_test' package.
  "Who tests the testers?" - "This class does."
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  argReport  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_arg_report(self, ) -> None:
    args = 'never', 'gonna', ('give', 'you', 'up'), 69, 420
    for chars in 24, 48, 77:
      report = self.argReport(*args, chars=chars, newLine=os.linesep)
      self.assertIsInstance(report, str)
      for line in str.split(report, os.linesep):
        self.assertLessEqual(len(str.strip(line)), chars)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  setUpClass artefacts   # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_stoch_word_attached(self) -> None:
    """setUpClass attaches a 'stochWord' generator to the class."""
    self.assertTrue(hasattr(type(self), 'stochWord'))

  def test_lorem_sentence_attached(self) -> None:
    """setUpClass attaches a 'loremSentence' generator to the class."""
    self.assertTrue(hasattr(type(self), 'loremSentence'))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Field getters  # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_typical_exceptions_includes_common_types(self) -> None:
    """'exceptions' yields the common runtime exception types."""
    excs = list(self.exceptions)
    self.assertIn(ValueError, excs)
    self.assertIn(TypeError, excs)
    self.assertIn(KeyError, excs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  assertion aliases  # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_assert_is_subclass(self) -> None:
    """'assertIsSubclass' passes for true subclass relations."""
    self.assertIsSubclass(bool, int)

  def test_assert_is_not_subclass_alias(self) -> None:
    """'assertIsNotSubclass' passes when the relation does not hold."""
    self.assertIsNotSubclass(int, bool)

  def test_assert_is_not_instance_alias(self) -> None:
    """'assertIsNotInstance' passes when the instance check fails."""
    self.assertIsNotInstance(42, str)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  tearDown branches  # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_tearDown_without_sub_test_is_noop(self) -> None:
    """tearDown returns cleanly when no sub test was used."""
    inst = TestBaseTest('test_arg_report')
    inst.tearDown()  # must not raise

  def test_tearDown_with_empty_sub_is_noop(self) -> None:
    """tearDown returns cleanly when sub test exists but has no fails."""
    inst = TestBaseTest('test_arg_report')
    _ = inst.subTest  # force the per-instance copy to exist
    inst.tearDown()  # must not raise

  def test_tearDown_surfaces_fails(self) -> None:
    """tearDown raises self.failureException when fails are recorded."""
    inst = TestBaseTest('test_arg_report')
    sub = inst.subTest
    sub._addFail(AssertionError('boom'))
    with self.assertRaises(AssertionError):
      inst.tearDown()

  def test_tearDown_surfaces_errors(self) -> None:
    """tearDown also surfaces non-AssertionError exceptions."""
    inst = TestBaseTest('test_arg_report')
    sub = inst.subTest
    sub._addError(ValueError('boom'))
    with self.assertRaises(AssertionError):
      inst.tearDown()

  def test_tearDown_surfaces_fails_and_errors(self) -> None:
    """tearDown reports both buckets in the failure message."""
    inst = TestBaseTest('test_arg_report')
    sub = inst.subTest
    sub._addFail(AssertionError('bad assert'))
    sub._addError(ValueError('bad value'))
    with self.assertRaises(AssertionError):
      inst.tearDown()
