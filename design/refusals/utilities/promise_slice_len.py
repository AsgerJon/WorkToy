"""
RefusedSliceLen holds the refusals that belong with
'design.promises.utilities.promise_slice_len'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import sliceLen


class RefusedSliceLen(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A step of zero raises 'ValueError'. Source: the 'sliceLen'
  docstring and its examples.
  """

  def test_zero_step(self) -> None:
    with self.assertRaises(Exception) as refused:
      sliceLen(slice(0, 10, 0), 10)
    self.assertIsInstance(refused.exception, ValueError)
