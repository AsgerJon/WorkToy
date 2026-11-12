"""
TestObjectRead tests the read protocol of 'Object' from 'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.core.sentinels import DELETED
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import RecursiveRead
from . import CoreTest, Counted, Noisy, SelfReader, EarlyReader
from . import PartnerReader, Agreeable


class TestObjectRead(CoreTest):
  """
  A read through an instance runs with its frame in place and the read
  hooks around '__instance_get__', a deleted value reads as absent, and
  a read made from a read hook of the same descriptor for the same
  instance is refused at that line. The tests pin the read through the
  class, the default read, the order of the hooks, the frame, the
  deleted value, and the refusal with its phase, released afterwards and
  not in the way of reading another instance.
  """

  def test_class_read_gives_descriptor(self) -> None:
    class Owner:
      d = Object()

    self.assertIsInstance(Owner.d, Object)
    self.assertIs(Owner.__dict__['d'], Owner.d)

  def test_default_instance_read_gives_descriptor(self) -> None:
    class Owner:
      d = Object()

    self.assertIs(Owner().d, Owner.d)
    self.assertFalse(Owner.d.hasContext())

  def test_hooks_around_read(self) -> None:
    class Owner:
      n = Noisy()

      def __init__(self) -> None:
        self.log = []

    owner = Owner()
    owner.n = 5
    owner.log.clear()
    self.assertEqual(owner.n, '5')
    self.assertEqual(owner.log,
                     [('preGet', True), ('get', {}), ('onGet', '5')])
    self.assertFalse(Owner.n.hasContext())

  def test_unset_slot_reads_as_missing(self) -> None:
    class Owner:
      n = Noisy()

      def __init__(self) -> None:
        self.log = []

    with self.assertRaises(AttributeError) as context:
      _ = Owner().n
    self.assertEqual(str(context.exception), 'n')
    self.assertFalse(Owner.n.hasContext())

  def test_deleted_reads_as_missing(self) -> None:
    class Owner:
      count = Counted()

    owner = Owner()
    self.assertEqual(owner.count, 0)
    owner.count = 3
    self.assertEqual(owner.count, 3)
    del owner.count
    with self.assertRaises(MissingVariable) as context:
      _ = owner.count
    self.assertEqual(context.exception.varName, 'count')
    self.assertIs(context.exception.instance, owner)
    self.assertEqual(context.exception.expectedTypes, (object,))
    self.assertIn("'Owner.count: object'", str(context.exception))
    self.assertFalse(hasattr(owner, 'count'))

  def test_deleted_guard(self) -> None:
    desc = Object()
    target = object()
    self.assertEqual(desc._deletedGuard(target, 5), 5)
    agreeable = Agreeable()
    self.assertTrue(agreeable == DELETED)
    self.assertIs(desc._deletedGuard(target, agreeable), agreeable)
    with self.assertRaises(MissingVariable) as context:
      desc._deletedGuard(target, DELETED)
    #  It is the descriptor that lacks a name, not the instance read.
    self.assertEqual(context.exception.varName, '__field_name__')
    self.assertIs(context.exception.instance, desc)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'Object.__field_name__: str'", str(context.exception))
    desc.__set_name__(object, 'named')
    with self.assertRaises(MissingVariable) as context:
      desc._deletedGuard(target, DELETED)
    self.assertEqual(context.exception.varName, 'named')
    self.assertIs(context.exception.instance, target)
    self.assertEqual(context.exception.expectedTypes, (object,))
    self.assertIn("'object.named: object'", str(context.exception))

  def test_self_read_from_on_get_refused(self) -> None:
    class Owner:
      f = SelfReader()

    owner = Owner()
    with self.assertRaises(RecursiveRead) as context:
      _ = owner.f
    self.assertIs(context.exception.desc, Owner.f)
    self.assertIs(context.exception.instance, owner)
    self.assertEqual(context.exception.phase, 'onGet')
    self.assertIn("'Owner.f'", str(context.exception))
    self.assertIn("'onGet'", str(context.exception))
    self.assertIsInstance(context.exception, RecursionError)
    self.assertEqual(Owner.f.__get_lock__, [])
    self.assertFalse(Owner.f.hasContext())

  def test_self_read_from_pre_get_refused(self) -> None:
    class Owner:
      f = EarlyReader()

    with self.assertRaises(RecursiveRead) as context:
      _ = Owner().f
    self.assertEqual(context.exception.phase, 'preGet')
    self.assertIs(context.exception.desc, Owner.f)
    self.assertIsInstance(context.exception.instance, Owner)
    self.assertIn("'preGet'", str(context.exception))
    self.assertEqual(Owner.f.__get_lock__, [])

  def test_other_instance_readable_from_hook(self) -> None:
    #  The owners compare equal to anything, so the lock is seen to tell
    #  instances apart by identity.
    class Owner(Agreeable):
      f = PartnerReader()

      def __init__(self, tag: str) -> None:
        self.tag = tag
        self.partner = None
        self.seen = []
        self.selfish = False

    first, second = Owner('first'), Owner('second')
    first.partner = second
    self.assertEqual(first.f, 'first')
    self.assertEqual(first.seen, ['second'])
    self.assertEqual(second.seen, [])
    self.assertEqual(Owner.f.__get_lock__, [])

  def test_self_read_after_partner_read_refused(self) -> None:
    class Owner(Agreeable):
      f = PartnerReader()

      def __init__(self, tag: str) -> None:
        self.tag = tag
        self.partner = None
        self.seen = []
        self.selfish = True

    first, second = Owner('first'), Owner('second')
    first.partner = second
    with self.assertRaises(RecursiveRead) as context:
      _ = first.f
    self.assertIs(context.exception.instance, first)
    self.assertIs(context.exception.desc, Owner.f)
    self.assertEqual(context.exception.phase, 'onGet')
    self.assertIn("'Owner.f'", str(context.exception))
    self.assertEqual(first.seen, ['second'])
    self.assertEqual(Owner.f.__get_lock__, [])

  def test_mutual_read_refused(self) -> None:
    class Owner:
      f = PartnerReader()

      def __init__(self, tag: str) -> None:
        self.tag = tag
        self.partner = None
        self.seen = []
        self.selfish = False

    first, second = Owner('first'), Owner('second')
    first.partner, second.partner = second, first
    with self.assertRaises(RecursiveRead) as context:
      _ = first.f
    self.assertIs(context.exception.instance, first)
    self.assertIs(context.exception.desc, Owner.f)
    self.assertEqual(context.exception.phase, 'onGet')
    self.assertIn("'onGet'", str(context.exception))
    self.assertEqual(Owner.f.__get_lock__, [])
    self.assertFalse(Owner.f.hasContext())

  def test_random_values_round_trip(self) -> None:
    class Owner:
      count = Counted()

    for value in self.randomInteger.row:
      owner = Owner()
      owner.count = value
      with self.subTest(value=value):
        self.assertEqual(owner.count, value)
