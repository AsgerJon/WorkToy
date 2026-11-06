"""
TestBaseTest tests 'BaseTest' from 'worktoy.work_test'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import os
import unittest
from unittest import TestCase

from worktoy.desc import AttriBox, Field
from worktoy.mcls import BaseMeta
from worktoy.waitaminute import TypeException
from worktoy.work_test import BaseTest, SubTest
from worktoy.work_test.samplers import IntSampler, FloatSampler
from worktoy.work_test.samplers import GaussianSampler, SymbolicSampler
from worktoy.work_test.samplers import WordSampler, LoremSampler
from . import WorkTestTest

SAMPLERS = (
  ('randomInteger', IntSampler), ('randomFloat', FloatSampler),
  ('randomGaussian', GaussianSampler),
  ('randomSymbolicName', SymbolicSampler), ('randomWord', WordSampler),
  ('randomLorem', LoremSampler),
)


class TestBaseTest(WorkTestTest):
  """
  'BaseTest' is the base every test of the suite is based on: six
  samplers of its own per test, 'subTest' recording every block and
  'tearDown' failing the test once with every record, the common
  exceptions, a report of arguments, and the subclass assertions on
  every Python supported. The tests pin the samplers as per-instance
  boxes, the seeding of all six and its refusal before any is seeded,
  the exceptions, the report with its cut and its two keywords, the
  assertions in both directions, and the verdicts of 'tearDown' as a
  plain 'unittest.TestResult' records them for a case built for it.
  """

  def test_shape(self) -> None:
    self.assertIsSubclass(BaseTest, TestCase)
    self.assertIs(type(BaseTest), BaseMeta)
    self.assertNotIn('tearDownClass', vars(BaseTest))
    self.assertIn('tearDown', vars(BaseTest))
    for name, _ in SAMPLERS:
      with self.subTest(name=name):
        self.assertIsInstance(BaseTest.__dict__[name], AttriBox)
    self.assertIsInstance(BaseTest.__dict__['subTest'], SubTest)
    self.assertIsInstance(BaseTest.__dict__['exceptions'], Field)

  def test_samplers_are_per_instance(self) -> None:
    class Case(BaseTest):
      def test_nothing(self) -> None:
        """Never runs: the case is built for its samplers alone."""

    first, second = Case('test_nothing'), Case('test_nothing')
    for name, cls in SAMPLERS:
      with self.subTest(name=name):
        self.assertIsInstance(getattr(first, name), cls)
        self.assertIs(getattr(first, name), getattr(first, name))
        self.assertIsNot(getattr(first, name), getattr(second, name))
        self.assertIsNone(getattr(second, name).seed)
    first.randomInteger = IntSampler(1, 6)
    self.assertEqual(first.randomInteger.maxVal, 6)
    self.assertEqual(second.randomInteger.maxVal, 255)

  def test_seed_samplers(self) -> None:
    class Case(BaseTest):
      def test_nothing(self) -> None:
        """Never runs: the case is built for its samplers alone."""

    case = Case('test_nothing')
    case.seedSamplers(7)
    for name, cls in SAMPLERS:
      with self.subTest(name=name):
        sampler = getattr(case, name)
        self.assertEqual(sampler.seed, 7)
        fresh = cls(seed=7)
        self.assertEqual([str(sampler()) for _ in range(4)],
                         [str(fresh()) for _ in range(4)])
    case.seedSamplers(7)
    first = [case.randomInteger() for _ in range(5)]
    case.seedSamplers(7)
    self.assertEqual([case.randomInteger() for _ in range(5)], first)
    self.assertNotEqual([case.randomInteger() for _ in range(5)], first)
    other = Case('test_nothing')
    with self.assertRaises(TypeException) as context:
      other.seedSamplers('seven')
    self.assertTypeRefused(context.exception, 'seed', 'seven', int)
    for name, _ in SAMPLERS:
      with self.subTest(name=name):
        self.assertIsNone(getattr(other, name).seed)
    self.assertEqual(self.randomInteger.seed, self.__sampler_seed__)

  def test_exceptions(self) -> None:
    expected = [ValueError, KeyError, IndexError, RuntimeError, OSError,
                PermissionError, TypeError, FileExistsError,
                FileNotFoundError]
    self.assertEqual([*self.exceptions], expected)
    self.assertEqual([*BaseTest('tearDown').exceptions], expected)

  def test_arg_report(self) -> None:
    report = BaseTest.argReport('never', 7, (1, 2))
    lines = report.split(os.linesep)
    self.assertEqual(lines[0], '<str: never>')
    self.assertEqual(lines[1].strip(), '<int: 7>')
    self.assertEqual(lines[2].strip(), '<tuple: (1, 2)>')
    self.assertEqual(self.argReport(), '')
    kept = BaseTest.argReport('x' * 40)
    self.assertEqual(kept, '<str: %s>' % ('x' * 40))
    self.assertEqual(len(kept), 47)
    cut = BaseTest.argReport('x' * 41)
    self.assertEqual(len(cut), 48)
    self.assertEqual(cut, '<str: %s...' % ('x' * 39))
    short = BaseTest.argReport('x' * 41, chars=24)
    self.assertEqual(short, '<str: %s...' % ('x' * 15))
    joined = BaseTest.argReport(1, 2, newLine='|')
    self.assertEqual(joined, '<int: 1>|  <int: 2>')

  def test_assertion_aliases(self) -> None:
    self.assertIsSubclass(bool, int)
    self.assertIsNotSubclass(int, bool)
    self.assertIsNotInstance(42, str)
    self.assertIs(BaseTest.assertIsNotSubclass,
                  BaseTest.assertNotIsSubclass)
    self.assertIs(BaseTest.assertIsNotInstance,
                  BaseTest.assertNotIsInstance)
    with self.assertRaises(AssertionError) as context:
      self.assertIsSubclass(int, str, msg='custom message')
    self.assertIn('custom message', str(context.exception))
    with self.assertRaises(AssertionError) as context:
      self.assertIsNotSubclass(bool, int, msg='custom message')
    self.assertIn('custom message', str(context.exception))
    with self.assertRaises(AssertionError) as context:
      self.assertIsNotInstance(42, int, msg='custom message')
    self.assertIn('custom message', str(context.exception))
    with self.assertRaises(AssertionError):
      self.assertIsSubclass(int, str)
    with self.assertRaises(AssertionError):
      self.assertIsNotSubclass(bool, int)

  def test_tear_down_verdicts(self) -> None:
    class Case(BaseTest):
      def test_pass(self) -> None:
        with self.subTest(x=1):
          self.assertEqual(1, 1)

      def test_untouched(self) -> None:
        self.assertEqual(1, 1)

      def test_fail(self) -> None:
        with self.subTest(x=1):
          self.fail('one')
        with self.subTest(x=2):
          raise KeyError('two')
        with self.subTest(x=3):
          self.assertEqual(3, 3)

      def test_skip(self) -> None:
        with self.subTest(x=1):
          self.skipTest('later')

    result = unittest.TestResult()
    unittest.TestLoader().loadTestsFromTestCase(Case).run(result)
    self.assertEqual(result.testsRun, 4)
    self.assertEqual(len(result.failures), 1)
    self.assertEqual(result.errors, [])
    self.assertEqual([reason for _, reason in result.skipped], ['later'])
    test, text = result.failures[0]
    self.assertEqual(test._testMethodName, 'test_fail')
    self.assertIn('FAIL [x=1]: one', text)
    self.assertIn("ERROR [x=2]: KeyError('two')", text)
    self.assertIn("self.fail('one')", text)
    self.assertIn("raise KeyError('two')", text)
    self.assertNotIn('x=3', text)
    self.assertEqual(text.count('Traceback (most recent call last)'), 3)

  def test_tear_down_builds_no_accumulator(self) -> None:
    class Case(BaseTest):
      def test_nothing(self) -> None:
        """Never runs: the case is built for its tearDown alone."""

    case = Case('test_nothing')
    case.tearDown()
    self.assertNotIn('__sub_test__', case.__dict__)
    _ = case.subTest
    case.tearDown()
    self.assertIn('__sub_test__', case.__dict__)

  def test_format_raised(self) -> None:
    self.assertEqual(BaseTest._formatRaised(ValueError('boom')),
                     'ValueError: boom')
    self.assertEqual(BaseTest._formatRaised(KeyError('k')), "KeyError: 'k'")
