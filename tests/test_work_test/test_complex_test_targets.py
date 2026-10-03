"""
TestComplexTestTargets subclasses 'BaseTest' and pins that 'ComplexTest'
skips itself when it has no targets. It is collected as a test wherever
it is imported, and used to run its methods against nothing, then pop
the library file holding it from 'sys.modules' in 'tearDownClass'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import unittest

from worktoy import work_test
from worktoy.work_test import BaseTest

from . import SimpleComplex


class _Targeted(work_test.ComplexTest):
  """_Targeted runs the shared tests against 'SimpleComplex'; it is run by
  hand below, never collected."""

  __test__ = False
  targets = (SimpleComplex,)


class TestComplexTestTargets(BaseTest):
  """
  TestComplexTestTargets provides tests for 'ComplexTest' with and without
  targets.
  """

  def test_untargeted_skips(self) -> None:
    """'ComplexTest' itself, without targets, skips every test and leaves
    the library file holding it loaded."""
    result = unittest.TestResult()
    loader = unittest.defaultTestLoader
    suite = loader.loadTestsFromTestCase(work_test.ComplexTest)
    suite.run(result)
    self.assertGreater(result.testsRun, 0)
    self.assertEqual(len(result.skipped), result.testsRun)
    self.assertIn('worktoy.work_test._complex_test', sys.modules)

  def test_targets_set_in_set_up_class(self) -> None:
    """Targets a subclass sets in its 'setUpClass' are found."""

    class _Late(work_test.ComplexTest):
      __test__ = False

      @classmethod
      def setUpClass(cls) -> None:
        super().setUpClass()
        cls.targets = (SimpleComplex,)

    result = unittest.TestResult()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(_Late)
    suite.run(result)
    self.assertEqual(result.skipped, [])
    self.assertTrue(result.wasSuccessful())

  def test_targeted_runs(self) -> None:
    """With targets the tests run and pass."""
    result = unittest.TestResult()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(_Targeted)
    suite.run(result)
    self.assertGreater(result.testsRun, 0)
    self.assertTrue(result.wasSuccessful())
