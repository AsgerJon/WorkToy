"""
ConfessedEqualAcrossFieldOrders confesses that two 'EZData' instances of
one lineage holding equal values are not equal across two orders of
their fields.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase, skip

from worktoy.ezdata import EZData


class ConfessedEqualAcrossFieldOrders(TestCase):
  """
  Promised in 1.2.0: two 'EZData' instances are equal when their values
  are and they are of one lineage, a class and its subclasses.

  Taken back in 1.2.1, for a subclass holding its
  fields in another order than the class it is compared with, as a class
  based on two dataclasses that declare the same names in opposite
  orders does. The promise read two ways there, and the two contradict
  each other. An instance iterates and unpacks as its values, and by
  position 'Size(1, 2)' and 'Both(1, 2)' hold the same values while each
  name holds another one. By name 'Size(width=1, height=2)' and
  'Both(width=1, height=2)' hold the same values while they iterate and
  unpack differently, and would have to hash alike over two different
  tuples.

  That a class and a subclass holding the same fields in the same order
  are equal over equal values, a frozen subclass included, is still
  owed, in 'promises/ezdata/promise_generated.py'.
  """

  @skip('Confessed after 1.2.0: not across two orders of the fields.')
  def test_equal_by_position(self) -> None:
    class Size(EZData):
      width = 0
      height = 0

    class Turned(EZData):
      height = 0
      width = 0

    class Both(Size, Turned):
      pass

    self.assertEqual(Size(1, 2), Both(1, 2))
