"""
PromiseSentinel promises the sentinels of 'worktoy.core.sentinels'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core.sentinels import Sentinel, SentinelMeta
from worktoy.core.sentinels import DELETED, OWNER, THIS, DESC, METACALL


class PromiseSentinel(TestCase):
  """
  A sentinel is a marker no real value can be mistaken for. A project
  declares one with a class statement on 'Sentinel', and the class itself is
  the marker: equal to itself alone and usable as a dict key. A name stands
  for one sentinel in the whole process, and that holds across families: a
  project may base a metaclass of its own on 'SentinelMeta' to give its
  sentinels behaviour. The sentinels of worktoy, 'DELETED', 'OWNER', 'THIS',
  'DESC' and 'METACALL', are sentinels like any other. Source: the docstrings
  of the 'sentinels' package, 'Sentinel' and 'SentinelMeta'.
  """

  def test_own_sentinel(self) -> None:
    class PROMISE_PENDING(Sentinel):
      """The value is not known yet."""

    self.assertIsInstance(PROMISE_PENDING, SentinelMeta)
    self.assertEqual(PROMISE_PENDING, PROMISE_PENDING)
    self.assertNotEqual(PROMISE_PENDING, 'PROMISE_PENDING')
    status = {PROMISE_PENDING: 'waiting'}
    self.assertEqual(status[PROMISE_PENDING], 'waiting')

  def test_family(self) -> None:
    class StateMeta(SentinelMeta):
      def describe(cls) -> str:
        return 'state %s' % cls.__name__

    class PROMISE_ON(metaclass=StateMeta):
      pass

    self.assertEqual(PROMISE_ON.describe(), 'state PROMISE_ON')

  def test_library_sentinels(self) -> None:
    for sentinel in (DELETED, OWNER, THIS, DESC, METACALL):
      with self.subTest(sentinel=sentinel):
        self.assertIsInstance(sentinel, SentinelMeta)
        self.assertTrue(issubclass(sentinel, Sentinel))
