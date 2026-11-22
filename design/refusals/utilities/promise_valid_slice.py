"""
RefusedValidSlice holds the refusals that belong with
'design.promises.utilities.promise_valid_slice'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import ValidSlice


class RefusedValidSlice(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. 'ValidSlice' itself cannot be instantiated and raises
  'TypeError'. Source: the 'ValidSlice' docstring and its examples.
  """

  def test_not_instantiable(self) -> None:
    with self.assertRaises(Exception) as refused:
      ValidSlice()
    self.assertIsInstance(refused.exception, TypeError)
