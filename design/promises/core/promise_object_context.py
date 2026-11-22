"""
PromiseObjectContext promises the access context of an 'Object' from
'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import threading
from unittest import TestCase

from worktoy.core import Object


class PromiseObjectContext(TestCase):
  """
  'self.instance' and 'self.owner' answer during an access only. Asked
  outside one, an 'Object' no class holds has no such attribute, so 'hasattr'
  answers False. Code driving the protocol by hand opens an access with
  'createContext(instance, owner)' and closes it with 'exitContext()', which
  brings back the access opened before it. Each thread sees its own accesses,
  so two threads reading through one descriptor at once each get their own
  instance. A read hook, 'preGet' or 'onGet', may read the field of another
  instance. Source: the 'Object' docstring, the docstrings of
  'getContextInstance', 'createContext', 'exitContext' and '_runReadHook',
  and the 1.1.0 changelog entries "Descriptors and namespace hooks keep their
  state per thread" and "A read hook reading its own field is refused with
  RecursiveRead".
  """

  def test_outside_access(self) -> None:
    class Plain(Object):
      pass

    class Holder:
      thing = Plain()

    placed = vars(Holder)['thing']
    self.assertFalse(hasattr(Plain(), 'instance'))
    self.assertFalse(hasattr(Plain(), 'owner'))

  def test_by_hand(self) -> None:
    class Plain(Object):
      pass

    class Holder:
      thing = Plain()

    placed, holder = vars(Holder)['thing'], Holder()
    placed.createContext(holder, Holder)
    try:
      self.assertIs(placed.instance, holder)
      self.assertIs(placed.owner, Holder)
    finally:
      placed.exitContext()

  def test_by_hand_nested(self) -> None:
    class Plain(Object):
      pass

    class Holder:
      thing = Plain()

    placed, outer, inner = vars(Holder)['thing'], Holder(), Holder()
    placed.createContext(outer, Holder)
    try:
      placed.createContext(inner, Holder)
      try:
        self.assertIs(placed.instance, inner)
      finally:
        placed.exitContext()
      self.assertIs(placed.instance, outer)
    finally:
      placed.exitContext()

  def test_threads_apart(self) -> None:
    barrier = threading.Barrier(2, timeout=10)

    class Slow(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        barrier.wait()
        return self.instance

    class Box:
      who = Slow()

    boxes = (Box(), Box())
    results = {}

    def read(box: Box) -> None:
      results[id(box)] = box.who is box

    threads = [threading.Thread(target=read, args=(b,)) for b in boxes]
    for thread in threads:
      thread.start()
    for thread in threads:
      thread.join()
    self.assertEqual(sorted(results.values()), [True, True])

  def test_recursive_read(self) -> None:
    class Gauge(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        return instance.levelValue

      def hookOnGet(self, instance, value, **kwargs) -> None:
        if instance.peer is not None:
          _ = instance.peer.level
        if instance.checkSelf:
          _ = instance.level

    class Tank:
      level = Gauge()

      def __init__(self, levelValue: int, peer: Tank = None,
                   checkSelf: bool = False) -> None:
        self.levelValue, self.peer = levelValue, peer
        self.checkSelf = checkSelf

    self.assertEqual(Tank(1, Tank(2, Tank(3))).level, 1)
    tank = Tank(5, checkSelf=True)
