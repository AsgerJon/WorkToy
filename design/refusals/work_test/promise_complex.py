"""
RefusedComplex holds the refusals that belong with
'design.promises.work_test.promise_complex'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.work_test import ComplexMixin, ComplexTest


class RefusedComplex(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A class listing the bank without a test case raises
  'TypeError'. Source: the docstrings of 'ComplexMixin' and 'ComplexTest'.
  """

  def test_bank_needs_a_test_case(self) -> None:
    class Simple(ComplexMixin):
      pass

    with self.assertRaises(Exception) as refused:
      class TestBare(ComplexTest):
        targets = (Simple,)
    self.assertIsInstance(refused.exception, TypeError)
