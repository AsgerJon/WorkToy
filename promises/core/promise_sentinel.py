"""
PromiseSentinel promises the sentinels of 'worktoy.core.sentinels'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core.sentinels import Sentinel, SentinelMeta
from worktoy.core.sentinels import DELETED, OWNER, THIS, DESC, METACALL
from worktoy.waitaminute.meta import IllegalInstantiation, DuplicateSentinel


class PromiseSentinel(TestCase):
  """
  A sentinel is a marker no real value can be mistaken for. A project
  declares one with a class statement on 'Sentinel', and the class
  itself is the marker: equal to itself alone, usable as a dict key, and
  impossible to instantiate, which raises 'IllegalInstantiation'. A name
  stands for one sentinel in the whole process, so a second class
  statement at a taken name, 'Sentinel' itself included, raises
  'DuplicateSentinel', and that holds across families: a project may
  base a metaclass of its own on 'SentinelMeta' to give its sentinels
  behaviour. The sentinels of worktoy, 'DELETED', 'OWNER', 'THIS',
  'DESC' and 'METACALL', are sentinels like any other. Source: the
  docstrings of the 'sentinels' package, 'Sentinel' and 'SentinelMeta'.
  """

  def test_own_sentinel(self) -> None:
    class PROMISE_PENDING(Sentinel):
      """The value is not known yet."""

    self.assertIsInstance(PROMISE_PENDING, SentinelMeta)
    self.assertEqual(PROMISE_PENDING, PROMISE_PENDING)
    self.assertNotEqual(PROMISE_PENDING, 'PROMISE_PENDING')
    status = {PROMISE_PENDING: 'waiting'}
    self.assertEqual(status[PROMISE_PENDING], 'waiting')

  def test_not_instantiable(self) -> None:
    class PROMISE_UNSET(Sentinel):
      pass

    with self.assertRaises(IllegalInstantiation) as context:
      PROMISE_UNSET()
    self.assertIsInstance(context.exception, TypeError)
    self.assertIs(context.exception.cls, PROMISE_UNSET)

  def test_one_per_name(self) -> None:
    class PROMISE_TWICE(Sentinel):
      pass

    first = PROMISE_TWICE
    with self.assertRaises(DuplicateSentinel) as context:
      class PROMISE_TWICE(Sentinel):
        pass
    e = context.exception
    self.assertIsInstance(e, TypeError)
    self.assertEqual(e.sentinelName, 'PROMISE_TWICE')
    self.assertIs(e.existing, first)
    self.assertEqual(e.module, __name__)

  def test_name_sentinel_taken(self) -> None:
    with self.assertRaises(DuplicateSentinel) as context:
      class Sentinel(metaclass=SentinelMeta):
        pass
    self.assertEqual(context.exception.sentinelName, 'Sentinel')

  def test_family(self) -> None:
    class StateMeta(SentinelMeta):
      def describe(cls) -> str:
        return 'state %s' % cls.__name__

    class PROMISE_ON(metaclass=StateMeta):
      pass

    self.assertEqual(PROMISE_ON.describe(), 'state PROMISE_ON')
    with self.assertRaises(DuplicateSentinel):
      class PROMISE_ON(Sentinel):
        pass

  def test_library_sentinels(self) -> None:
    for sentinel in (DELETED, OWNER, THIS, DESC, METACALL):
      with self.subTest(sentinel=sentinel):
        self.assertIsInstance(sentinel, SentinelMeta)
        self.assertTrue(issubclass(sentinel, Sentinel))
        with self.assertRaises(IllegalInstantiation):
          sentinel()
