"""
PromiseBaseTest promises 'BaseTest' and its 'subTest' from
'worktoy.work_test'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import unittest
from unittest import TestCase

from worktoy.work_test import BaseTest
from worktoy.work_test.samplers import IntSampler, FloatSampler


class PromiseBaseTest(TestCase):
  """
  'BaseTest' is a 'unittest.TestCase' a project's tests may be based on.
  Its 'subTest' runs every block of a loop even when one fails or
  raises, and the test then fails once, its report naming the label of
  each failed block, nested labels joined by ' -> ', and what it raised.
  A 'setUp' of a test needs no call of the base's. Each test has
  samplers of its own, 'randomInteger',
  'randomFloat' and the others, and 'seedSamplers(seed)' seeds them all
  so a test repeats its data. 'assertIsNotInstance' and
  'assertIsNotSubclass' are the negative assertions on every Python
  worktoy supports. Source: the docstrings of 'BaseTest' and 'SubTest'.
  """

  def runTests(self, testClass: type) -> unittest.TestResult:
    result = unittest.TestResult()
    unittest.TestLoader().loadTestsFromTestCase(testClass).run(result)
    return result

  def test_sub_test_runs_every_block(self) -> None:
    seen = []

    class TestValues(BaseTest):
      def test_values(self) -> None:
        for value in (1, 2, 3, 4):
          with self.subTest(value=value):
            seen.append(value)
            self.assertNotIn(value, (2, 3))

    result = self.runTests(TestValues)
    self.assertEqual(seen, [1, 2, 3, 4])
    self.assertEqual(result.testsRun, 1)
    self.assertEqual(len(result.failures), 1)
    report = result.failures[0][1]
    self.assertIn('value=2', report)
    self.assertIn('value=3', report)

  def test_errors_and_nesting(self) -> None:
    seen = []

    class TestLookups(BaseTest):
      def test_lookups(self) -> None:
        for key in ('a', 'b'):
          with self.subTest(key=key):
            seen.append(key)
            _ = {}[key]
        with self.subTest(outer=1):
          with self.subTest(inner=2):
            raise AssertionError('nested')

    result = self.runTests(TestLookups)
    self.assertEqual(seen, ['a', 'b'])
    self.assertFalse(result.wasSuccessful())
    report = (result.failures + result.errors)[0][1]
    self.assertIn('KeyError', report)
    self.assertIn('outer=1 -> inner=2', report)

  def test_own_set_up(self) -> None:
    drawn = []

    class TestOwnSetUp(BaseTest):
      def setUp(self) -> None:
        self.extra = 1

      def test_draw(self) -> None:
        drawn.append(self.randomInteger.item)

    self.assertTrue(self.runTests(TestOwnSetUp).wasSuccessful())
    self.assertEqual(len(drawn), 1)

  def test_passing(self) -> None:
    class TestFine(BaseTest):
      def test_fine(self) -> None:
        for value in (1, 2):
          with self.subTest(value=value):
            self.assertTrue(value)

    result = self.runTests(TestFine)
    self.assertTrue(result.wasSuccessful())

  def test_samplers(self) -> None:
    drawn = []

    class TestDraw(BaseTest):
      def test_draw(self) -> None:
        self.assertIsInstance(self.randomInteger, IntSampler)
        self.assertIsInstance(self.randomFloat, FloatSampler)
        self.seedSamplers(11)
        drawn.append(self.randomInteger.item)

    self.assertTrue(self.runTests(TestDraw).wasSuccessful())
    self.assertTrue(self.runTests(TestDraw).wasSuccessful())
    self.assertEqual(drawn[0], drawn[1])

  def test_negative_assertions(self) -> None:
    class TestNegatives(BaseTest):
      def test_negatives(self) -> None:
        self.assertIsNotInstance(1, str)
        self.assertIsNotSubclass(int, str)
        with self.assertRaises(AssertionError):
          self.assertIsNotSubclass(bool, int)

    self.assertTrue(self.runTests(TestNegatives).wasSuccessful())
