"""
PromiseBoxRefusals promises the box declarations 'worktoy.desc' refuses
as the class is created.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject


class PromiseBoxRefusals(TestCase):
  """
  One box bound to a second name in one class body gives a second
  attribute of its own. Source: the docstrings of 'AttriBox' and
  'BaseDescriptor'.
  """

  def test_second_name_in_one_body(self) -> None:
    class Pair(BaseObject):
      left = AttriBox[int](1)
      right = left

    pair = Pair()
    pair.left = 5
    self.assertEqual(pair.right, 1)
