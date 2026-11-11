"""
ConfessedIterationByIndex confesses that an enumeration does not
iterate its members by their index.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase, skip

from ..keenum._week_day import WeekDay


class ConfessedIterationByIndex(TestCase):
  """
  Promised in 1.1.0: an enumeration iterates its members in index
  order.

  Taken back in 1.2.0. A member is one object shared by its enumeration
  and every subclass of it, and it carries one index, its position in
  the class that declared it. The order of a class is the order of the
  class, and cannot be read off a number each member carries from
  somewhere else. The members a plain enumeration gives when iterated,
  and their order, are still owed, in
  'promises/keenum/promise_enumeration.py' and
  'promises/keenum/promise_declaring.py'. The 'index' of a member is
  deprecated as well: 'promises/deprecations/promise_member_index.py'.
  """

  @skip('Confessed in 1.2.0: iteration is not by the index of members.')
  def test_index_order(self) -> None:
    indexes = [member.index for member in WeekDay]
    self.assertEqual(indexes, sorted(indexes))
