"""
RefusedObject holds the refusals that belong with
'design.promises.core.promise_object'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import Object
from worktoy.core.sentinels import DELETED
from worktoy.waitaminute import MissingVariable


class RefusedObject(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. After a deletion, a read, or a second deletion, raises
  'MissingVariable', an 'AttributeError'. Source: the 'Object' docstring and
  its example, and the docstrings of the three methods and of 'DELETED'.
  """

  def test_counter_1(self) -> None:
    class Counted(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        return getattr(instance, '_count', 0)

      def __instance_set__(self, instance, value, **kwargs):
        instance._count = value

      def __instance_delete__(self, instance, old=None, **kwargs):
        instance._count = DELETED

    class Visit:
      count = Counted()

    visit = Visit()
    visit.count = 3
    del visit.count
    with self.assertRaises(Exception) as refused:
      _ = visit.count
    self.assertIsInstance(refused.exception, MissingVariable)

  def test_counter_2(self) -> None:
    class Counted(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        return getattr(instance, '_count', 0)

      def __instance_set__(self, instance, value, **kwargs):
        instance._count = value

      def __instance_delete__(self, instance, old=None, **kwargs):
        instance._count = DELETED

    class Visit:
      count = Counted()

    visit = Visit()
    visit.count = 3
    del visit.count
    with self.assertRaises(Exception) as refused:
      del visit.count
    self.assertIsInstance(refused.exception, MissingVariable)
