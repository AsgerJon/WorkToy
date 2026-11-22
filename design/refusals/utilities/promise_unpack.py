"""
RefusedUnpack holds the refusals that belong with
'design.promises.utilities.promise_unpack'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import unpack
from worktoy.waitaminute import UnpackException


class RefusedUnpack(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. By default a call with nothing iterable raises
  'UnpackException'. Source: the 'unpack' docstring and its examples.
  """

  def test_nothing_iterable_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      unpack(1, 2)
    self.assertIsInstance(refused.exception, UnpackException)

  def test_nothing_iterable_2(self) -> None:
    with self.assertRaises(Exception) as refused:
      unpack()
    self.assertIsInstance(refused.exception, UnpackException)
