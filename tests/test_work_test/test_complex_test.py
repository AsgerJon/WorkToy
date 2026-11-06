"""
TestComplexTest tests 'ComplexTest' from 'worktoy.work_test', the bank,
by the verdicts of the cases that list it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import unittest
from unittest import TestCase

from worktoy.work_test import BaseTest, ComplexTest
from worktoy.work_test import _complex_test
from . import WorkTestTest, SimpleComplex, WrongComplex, BotchedComplex


class TestComplexTest(WorkTestTest):
  """
  'ComplexTest' is a bank of twenty-five tests of the arithmetic of a
  'ComplexMixin', run against every target of the class that lists it
  before a test case. The tests pin the bank by its verdicts: no loader
  collects the bank itself, a class with a target passes all
  twenty-five, a class without targets skips all twenty-five and says
  so, targets set in 'setUpClass' are found, a wrong target fails the
  tests of its wrong operation and no other with the target named in
  the label, and a class listing the bank without a test case is refused
  at the class statement with the shape to write.
  """

  @staticmethod
  def _run(cls: type) -> unittest.TestResult:
    """Every test of the class run into a fresh result."""
    result = unittest.TestResult()
    unittest.TestLoader().loadTestsFromTestCase(cls).run(result)
    return result

  def test_bank_is_no_test_case(self) -> None:
    self.assertIsNotSubclass(ComplexTest, TestCase)
    suite = unittest.TestLoader().loadTestsFromModule(_complex_test)
    self.assertEqual(suite.countTestCases(), 0)
    names = [name for name in dir(ComplexTest) if name.startswith('test_')]
    self.assertEqual(len(names), 25)
    self.assertEqual(ComplexTest.targets, ())

  def test_targeted_runs(self) -> None:
    class Bank(ComplexTest, BaseTest):
      targets = (SimpleComplex,)

    result = self._run(Bank)
    self.assertEqual(result.testsRun, 25)
    self.assertEqual(result.skipped, [])
    self.assertEqual(result.failures, [])
    self.assertEqual(result.errors, [])
    self.assertTrue(result.wasSuccessful())

  def test_untargeted_skips(self) -> None:
    class Empty(ComplexTest, BaseTest):
      """A class that forgot its targets."""

    result = self._run(Empty)
    self.assertEqual(result.testsRun, 25)
    self.assertEqual(len(result.skipped), 25)
    self.assertEqual({reason for _, reason in result.skipped},
                     {'Empty has no targets'})
    self.assertTrue(result.wasSuccessful())

  def test_targets_set_in_set_up_class(self) -> None:
    class Late(ComplexTest, BaseTest):
      @classmethod
      def setUpClass(cls) -> None:
        cls.targets = (SimpleComplex,)

    result = self._run(Late)
    self.assertEqual(result.testsRun, 25)
    self.assertEqual(result.skipped, [])
    self.assertTrue(result.wasSuccessful())

  def test_wrong_target_fails_its_own_tests(self) -> None:
    class Bank(ComplexTest, BaseTest):
      targets = (SimpleComplex, WrongComplex)

    result = self._run(Bank)
    self.assertEqual(result.testsRun, 25)
    self.assertEqual(result.errors, [])
    self.assertEqual(result.skipped, [])
    failed = sorted(test._testMethodName for test, _ in result.failures)
    self.assertEqual(failed, ['test_add_builtin_complex',
                              'test_add_instances', 'test_add_scalar',
                              'test_radd_scalar'])
    for _, text in result.failures:
      self.assertIn('FAIL [target=WrongComplex]:', text)
      self.assertNotIn('target=SimpleComplex', text)

  def test_botched_target_fails_every_test(self) -> None:
    class Bank(ComplexTest, BaseTest):
      targets = (SimpleComplex, BotchedComplex)

    result = self._run(Bank)
    self.assertEqual(result.testsRun, 25)
    self.assertEqual(result.errors, [])
    self.assertEqual(result.skipped, [])
    failed = sorted(test._testMethodName for test, _ in result.failures)
    expected = sorted(name for name in dir(ComplexTest)
                      if name.startswith('test_'))
    self.assertEqual(failed, expected)
    for _, text in result.failures:
      self.assertIn('[target=BotchedComplex]', text)
      self.assertNotIn('target=SimpleComplex', text)

  def test_bank_tells_the_operation_from_a_lookalike(self) -> None:
    #  With other operands a reflected division that subtracts and a
    #  square that doubles give the right numbers by accident; a power
    #  with a scalar base reaches the same '__pow__', so the doubling
    #  target fails the reflected power as well.
    class Subtracting(SimpleComplex):
      def __rtruediv__(self, other: object) -> SimpleComplex:
        return self._resolveOther(other) - self

    class Doubling(SimpleComplex):
      def __pow__(self, other: object) -> SimpleComplex:
        return self * other

    class Bank(ComplexTest, BaseTest):
      targets = (Subtracting, Doubling)

    result = self._run(Bank)
    self.assertEqual(result.testsRun, 25)
    self.assertEqual(result.errors, [])
    failed = {test._testMethodName: text for test, text in result.failures}
    self.assertEqual(sorted(failed), ['test_pow_scalar', 'test_rpow_scalar',
                                      'test_rtruediv_scalar'])
    self.assertIn('[target=Doubling]', failed['test_pow_scalar'])
    self.assertIn('[target=Doubling]', failed['test_rpow_scalar'])
    self.assertIn('[target=Subtracting]', failed['test_rtruediv_scalar'])
    self.assertNotIn('Subtracting', failed['test_pow_scalar'])
    self.assertNotIn('Doubling', failed['test_rtruediv_scalar'])

  def test_bank_refuses_a_stranger_in_each_operation(self) -> None:
    #  A target that takes a stranger in one operation alone must fail
    #  the refusal test of that operation and no other, so each of the
    #  five refusal tests is shown to exercise its own operation.
    expected = {
      '__add__': 'test_add_unsupported', '__sub__': 'test_sub_unsupported',
      '__mul__': 'test_mul_unsupported',
      '__truediv__': 'test_truediv_unsupported',
      '__pow__': 'test_pow_unsupported',
    }
    for dunder, name in expected.items():
      with self.subTest(dunder=dunder):
        Lenient = self._lenientIn(dunder)

        class Bank(ComplexTest, BaseTest):
          targets = (Lenient,)

        result = self._run(Bank)
        self.assertEqual(result.testsRun, 25)
        self.assertEqual(result.errors, [])
        failed = [test._testMethodName for test, _ in result.failures]
        self.assertEqual(failed, [name])
        self.assertIn('[target=Lenient]', result.failures[0][1])

  @staticmethod
  def _lenientIn(dunder: str) -> type:
    """A 'SimpleComplex' taking a string in the one operation named."""
    proper = getattr(SimpleComplex, dunder)

    def lenient(self: SimpleComplex, other: object) -> object:
      """The operation, with a string taken as the instance itself."""
      if isinstance(other, str):
        return self
      return proper(self, other)

    return type('Lenient', (SimpleComplex,), {dunder: lenient})

  def test_shape_refused(self) -> None:
    with self.assertRaises(TypeError) as context:
      class Wrong(ComplexTest):
        targets = (SimpleComplex,)
    self.assertEqual(str(context.exception), "'Wrong' lists 'ComplexTest' "
                                             "as a base but no test case, "
                                             "so no loader would run its "
                                             "tests. The bank runs as part "
                                             "of a test case: write 'class "
                                             "Wrong(ComplexTest, "
                                             "BaseTest):' with the "
                                             "targets.")
