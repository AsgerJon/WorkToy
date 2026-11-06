"""
TestObjectDelete tests the delete protocol of 'Object' from
'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.core.sentinels import DELETED
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import ProtectedError
from . import CoreTest, Counted, Noisy


class TestObjectDelete(CoreTest):
  """
  A deletion through an instance runs with its frame in place, reads the
  old value without the read hooks, hands it to '__instance_delete__'
  between the delete hooks, and fails a second time as a plain attribute
  does. The default refuses. The tests pin the refusal with the old
  value, the marking with 'DELETED', the order of the hooks, the old
  value of a slot never written, and the frame being gone afterwards.
  """

  def test_default_delete_refused(self) -> None:
    class Owner:
      d = Object()

    owner = Owner()
    with self.assertRaises(ProtectedError) as context:
      del owner.d
    self.assertIs(context.exception.instance, owner)
    self.assertIs(context.exception.desc, Owner.d)
    self.assertIs(context.exception.oldVal, Owner.d)
    self.assertIn("'Owner.d'", str(context.exception))
    self.assertFalse(Owner.d.hasContext())

  def test_deletion_marks_and_second_deletion_fails(self) -> None:
    class Owner:
      count = Counted()

    owner = Owner()
    owner.count = 3
    del owner.count
    self.assertIs(owner._count, DELETED)
    with self.assertRaises(MissingVariable) as context:
      del owner.count
    self.assertEqual(context.exception.varName, 'count')
    self.assertIs(context.exception.instance, owner)
    self.assertEqual(context.exception.expectedTypes, (object,))
    self.assertIn("'Owner.count: object'", str(context.exception))
    self.assertFalse(Owner.count.hasContext())

  def test_hooks_around_delete(self) -> None:
    class Owner:
      n = Noisy()

      def __init__(self) -> None:
        self.log = []

    owner = Owner()
    owner.n = 1
    owner.log.clear()
    del owner.n
    self.assertEqual(owner.log, [
      ('get', {'_deleting': True}),
      ('preDelete', Owner),
      ('delete', '1'),
      ('onDelete', None),
    ])
    self.assertFalse(Owner.n.hasContext())
    with self.assertRaises(MissingVariable) as context:
      _ = owner.n
    self.assertEqual(context.exception.varName, 'n')
    self.assertIs(context.exception.instance, owner)
    self.assertEqual(context.exception.expectedTypes, (object,))
    self.assertIn("'Owner.n: object'", str(context.exception))

  def test_unwritten_slot_deletes_with_none(self) -> None:
    class Owner:
      n = Noisy()

      def __init__(self) -> None:
        self.log = []

    owner = Owner()
    del owner.n
    self.assertEqual(owner.log, [
      ('get', {'_deleting': True}),
      ('preDelete', Owner),
      ('delete', None),
      ('onDelete', None),
    ])

  def test_frame_popped_when_delete_raises(self) -> None:
    class Owner:
      d = Object()

    owner = Owner()
    with self.assertRaises(ProtectedError) as context:
      del owner.d
    self.assertIs(context.exception.instance, owner)
    self.assertIs(context.exception.desc, Owner.d)
    self.assertIs(context.exception.oldVal, Owner.d)
    self.assertIn("'Owner.d'", str(context.exception))
    self.assertFalse(Owner.d.hasContext())
    self.assertEqual(Owner.d.__call_chain__, [])
