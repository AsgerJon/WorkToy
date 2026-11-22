"""
RefusedObjectContext holds the refusals that belong with
'design.promises.core.promise_object_context'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import Object
from worktoy.waitaminute.desc import WithoutException, RecursiveRead


class RefusedObjectContext(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. Asked outside an access, a descriptor placed in a class raises
  'WithoutException', a 'RuntimeError'. Closing an access with none open
  raises 'WithoutException'. A read hook, 'preGet' or 'onGet', reading its
  own field for the same instance raises 'RecursiveRead', a 'RecursionError',
  naming the hook. Source: the 'Object' docstring, the docstrings of
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
    with self.assertRaises(Exception) as refused:
      _ = placed.instance
    self.assertIsInstance(refused.exception, WithoutException)

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
    with self.assertRaises(Exception) as refused:
      placed.exitContext()
    self.assertIsInstance(refused.exception, WithoutException)

  def test_recursive_read_before(self) -> None:
    class Gauge(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        return 1

      def hookPreGet(self, instance, **kwargs) -> None:
        _ = instance.level

    class Tank:
      level = Gauge()

    with self.assertRaises(Exception) as refused:
      _ = Tank().level
    self.assertIsInstance(refused.exception, RecursiveRead)

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

    tank = Tank(5, checkSelf=True)
    with self.assertRaises(Exception) as refused:
      _ = tank.level
    self.assertIsInstance(refused.exception, RecursiveRead)
