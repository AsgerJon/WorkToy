"""
TestSubTestSkip subclasses 'BaseTest' and pins that 'skipTest' inside a
sub-test block skips the test, as it does outside one. The block used to
record 'unittest.SkipTest' as an error, like any other exception, so the
test failed in 'tearDown' instead of being skipped.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import unittest

from worktoy.work_test import BaseTest, SubTest


class _Skipping(BaseTest):
  """_Skipping skips from inside a sub-test block; it is run by hand
  below, never collected."""

  __test__ = False

  def test_skip(self) -> None:
    with self.subTest(x=1):
      self.skipTest('not today')


class TestSubTestSkip(BaseTest):
  """
  TestSubTestSkip provides tests for 'skipTest' inside a sub-test block.
  """

  def test_skip_propagates(self) -> None:
    """'SkipTest' leaves the block as itself and is not recorded."""
    sub = SubTest()
    with self.assertRaises(unittest.SkipTest):
      with sub:
        raise unittest.SkipTest('not today')
    self.assertEqual(sub.errors, ())
    self.assertEqual(sub.passed, ())

  def test_test_is_skipped(self) -> None:
    """A test skipping inside a sub-test block counts as skipped, not as
    failed."""
    result = unittest.TestResult()
    _Skipping('test_skip').run(result)
    self.assertEqual(len(result.skipped), 1)
    self.assertEqual(result.failures, [])
    self.assertEqual(result.errors, [])
