"""
PromiseObjectHooks promises the notification hooks of 'Object' from
'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import Object
from worktoy.core.control_flow import SkipSet, ControlFlow
from worktoy.core.sentinels import DELETED


class PromiseObjectHooks(TestCase):
  """
  Around each access, an 'Object' calls hooks a subclass may define:
  'hookPreGet' before a read and 'hookOnGet' after it with the value;
  'hookPreSet' before a write with the value assigned, and 'hookOnSet'
  after it with the value '__instance_set__' returned, or with the value
  assigned when it returned 'None'; 'hookPreDelete' and 'hookOnDelete'
  around a deletion; and 'hookSetName' when the descriptor is placed in
  a class. Raising 'SkipSet' in 'hookPreSet' ends the write silently:
  nothing is stored and 'hookOnSet' is not called; any other exception,
  another signal included, reaches the line that assigned. 'hookOnSet'
  runs after the value is stored, so raising there refuses nothing. A
  deletion first reads the old value, with '_deleting=True' handed to
  '__instance_get__' so it can avoid building a default, and with no
  read hooks; then come 'hookPreDelete', '__instance_delete__' and
  'hookOnDelete'. Source: the 'Object' docstring and the docstrings of
  '__set__', '__delete__', its hooks, '__instance_get__' and 'SkipSet'.
  """

  def test_order(self) -> None:
    log = []

    class Logged(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        log.append('get')
        return instance.__dict__.get('_v', 0)

      def __instance_set__(self, instance, value, **kwargs):
        log.append('set')
        instance.__dict__['_v'] = value

      def __instance_delete__(self, instance, old=None, **kwargs):
        log.append('delete')
        instance.__dict__['_v'] = DELETED

      def hookPreGet(self, instance, **kwargs) -> None:
        log.append('preGet')

      def hookOnGet(self, instance, value, **kwargs) -> None:
        log.append('onGet')

      def hookPreSet(self, instance, value, **kwargs) -> None:
        log.append('preSet')

      def hookOnSet(self, instance, value, **kwargs) -> None:
        log.append('onSet')

      def hookPreDelete(self, instance, **kwargs) -> None:
        log.append('preDelete')

      def hookOnDelete(self, instance, **kwargs) -> None:
        log.append('onDelete')

    class Holder:
      value = Logged()

    holder = Holder()
    del log[:]
    _ = holder.value
    self.assertEqual(log, ['preGet', 'get', 'onGet'])
    del log[:]
    holder.value = 1
    self.assertEqual(log, ['preSet', 'set', 'onSet'])
    del log[:]
    del holder.value
    self.assertEqual(log, ['get', 'preDelete', 'delete', 'onDelete'])

  def test_on_set_after_store(self) -> None:
    class Strict(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        return instance.__dict__.get('_v', 0)

      def __instance_set__(self, instance, value, **kwargs):
        instance.__dict__['_v'] = value

      def hookOnSet(self, instance, value, **kwargs) -> None:
        raise ValueError('too late to refuse')

    class Holder:
      value = Strict()

    holder = Holder()
    with self.assertRaises(ValueError):
      holder.value = 4
    self.assertEqual(holder.value, 4)

  def test_other_signal_propagates(self) -> None:
    class Halt(ControlFlow):
      """The write must stop here."""

    class Guarded(Object):
      def __instance_set__(self, instance, value, **kwargs):
        instance.__dict__['_v'] = value

      def hookPreSet(self, instance, value, **kwargs) -> None:
        raise Halt

    class Holder:
      value = Guarded()

    with self.assertRaises(Halt):
      Holder().value = 1

  def test_values_handed_to_hooks(self) -> None:
    seen = []

    class Doubling(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        return instance.__dict__.get('_v', 0)

      def __instance_set__(self, instance, value, **kwargs):
        instance.__dict__['_v'] = value * 2
        return value * 2

      def hookOnGet(self, instance, value, **kwargs) -> None:
        seen.append(('onGet', value))

      def hookPreSet(self, instance, value, **kwargs) -> None:
        seen.append(('preSet', value))

      def hookOnSet(self, instance, value, **kwargs) -> None:
        seen.append(('onSet', value))

    class Holder:
      value = Doubling()

    holder = Holder()
    holder.value = 5
    _ = holder.value
    self.assertEqual(seen, [('preSet', 5), ('onSet', 10), ('onGet', 10)])

  def test_on_set_gets_assigned_value_when_none_returned(self) -> None:
    seen = []

    class Plain(Object):
      def __instance_set__(self, instance, value, **kwargs):
        instance.__dict__['_v'] = value

      def hookOnSet(self, instance, value, **kwargs) -> None:
        seen.append(value)

    class Holder:
      value = Plain()

    Holder().value = 'assigned'
    self.assertEqual(seen, ['assigned'])

  def test_skip_set(self) -> None:
    seen = []

    class Unchanged(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        return instance.__dict__.get('_v', 0)

      def __instance_set__(self, instance, value, **kwargs):
        instance.__dict__['_v'] = value

      def hookPreSet(self, instance, value, **kwargs) -> None:
        if value == instance.__dict__.get('_v', 0):
          raise SkipSet

      def hookOnSet(self, instance, value, **kwargs) -> None:
        seen.append(value)

    class Holder:
      value = Unchanged()

    holder = Holder()
    holder.value = 3
    holder.value = 3
    self.assertEqual(holder.value, 3)
    self.assertEqual(seen, [3])

  def test_set_name(self) -> None:
    placed = []

    class Placed(Object):
      def hookSetName(self, owner, name, **kwargs) -> None:
        placed.append((owner.__name__, name))

    class Holder:
      thing = Placed()

    self.assertEqual(placed, [('Holder', 'thing')])
    self.assertIs(vars(Holder)['thing'].getFieldOwner(), Holder)
    self.assertEqual(vars(Holder)['thing'].getFieldName(), 'thing')

  def test_deleting_flag(self) -> None:
    flags = []

    class Lazy(Object):
      def __instance_get__(self, instance, owner, **kwargs):
        flags.append(kwargs.get('_deleting', False))
        return instance.__dict__.get('_v', 0)

      def __instance_delete__(self, instance, old=None, **kwargs):
        instance.__dict__['_v'] = DELETED

    class Holder:
      value = Lazy()

    holder = Holder()
    _ = holder.value
    del holder.value
    self.assertEqual(flags, [False, True])
