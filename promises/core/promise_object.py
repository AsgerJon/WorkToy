"""
PromiseObject promises the descriptor protocol of 'Object' from
'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import Object
from worktoy.core.sentinels import DELETED
from worktoy.waitaminute import MissingVariable


class PromiseObject(TestCase):
  """
  A descriptor written on 'Object' defines three methods and nothing
  else: '__instance_get__' gives what a read through an instance
  returns, '__instance_set__' does the write and may return the value it
  stored, and '__instance_delete__' does the deletion, receiving the old
  value. During each of them 'self.instance' and 'self.owner' are the
  instance and the class of the access. A read through the class gives
  the descriptor itself. A deletion stores 'DELETED', after which a read,
  or a second deletion, raises 'MissingVariable', an 'AttributeError', so
  'hasattr' answers False. Source: the 'Object' docstring and its
  example, and the docstrings of the three methods and of 'DELETED'.
  """

  def test_counter(self) -> None:
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
    self.assertEqual(visit.count, 0)
    visit.count = 3
    self.assertEqual(visit.count, 3)
    del visit.count
    self.assertFalse(hasattr(visit, 'count'))
    with self.assertRaises(MissingVariable) as context:
      _ = visit.count
    e = context.exception
    self.assertIsInstance(e, AttributeError)
    self.assertIs(e.instance, visit)
    self.assertEqual(e.varName, 'count')
    self.assertEqual(e.expectedTypes, (object,))
    with self.assertRaises(MissingVariable) as context:
      del visit.count
    self.assertIs(context.exception.instance, visit)
    self.assertEqual(context.exception.varName, 'count')
    self.assertEqual(context.exception.expectedTypes, (object,))

  def test_class_read_gives_descriptor(self) -> None:
    class Plain(Object):
      pass

    class Holder:
      thing = Plain()

    self.assertIs(Holder.thing, vars(Holder)['thing'])

  def test_instance_and_owner_during_access(self) -> None:
    seen = []

    class Watched(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        seen.append((self.instance, self.owner))
        return 1

      def __instance_set__(self, instance, value, **kwargs):
        seen.append((self.instance, self.owner))

      def __instance_delete__(self, instance, old=None, **kwargs):
        seen.append((self.instance, self.owner))

    class Room:
      lamp = Watched()

    room = Room()
    _ = room.lamp
    room.lamp = 2
    del room.lamp
    self.assertGreaterEqual(len(seen), 3)
    for instance, owner in seen:
      self.assertIs(instance, room)
      self.assertIs(owner, Room)

  def test_old_value_on_delete(self) -> None:
    received = []

    class Stored(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        return instance.__dict__.get('_v', 0)

      def __instance_set__(self, instance, value, **kwargs):
        instance.__dict__['_v'] = value

      def __instance_delete__(self, instance, old=None, **kwargs):
        received.append(old)
        instance.__dict__['_v'] = DELETED

    class Holder:
      value = Stored()

    holder = Holder()
    holder.value = 7
    del holder.value
    self.assertEqual(received, [7])
