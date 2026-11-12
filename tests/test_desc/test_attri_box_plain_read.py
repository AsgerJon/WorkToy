"""
TestAttriBoxPlainRead tests the read of a stored value through an
'AttriBox' from 'worktoy.desc' that has no read hook to run.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.waitaminute import MissingVariable, TypeException
from . import DescTest, Part, CountingBox


class TestAttriBoxPlainRead(DescTest):
  """
  A box holding a stored value, with no read callback registered and
  no read hook overridden, hands the value out without a frame and
  without the hook phases, since no code of the builder runs in such a
  read. Every other read goes the full way. The tests count the frames
  a 'CountingBox' pushes to tell the two apart, and pin: the first read
  of each instance building through the full read and the later ones
  pushing nothing, the value being the same object, a write followed by
  a read, the box settling once whether its hooks are its own, a read
  callback before or after the read sending every read the full way,
  one registered after reads were made, a subclass overriding a hook or
  the fetch, the refusal of a deleted value, a value that is never
  asked anything, and a storage name that is no name.
  """

  def test_stored_value_pushes_no_frame(self) -> None:
    class Owner:
      part = CountingBox[Part](1, key=2)

    box = Owner.part
    self.assertIs(box, Owner.part)
    self.assertEqual(box.frames, 0)
    self.assertIsNone(box.__reads_plainly__)
    owner = Owner()
    built = owner.part
    self.assertEqual(box.frames, 1)
    self.assertIs(box.__reads_plainly__, True)
    for _ in range(3):
      self.assertIs(owner.part, built)
    self.assertEqual(box.frames, 1)
    other = Owner()
    self.assertIsNot(other.part, built)
    self.assertEqual(box.frames, 2)
    self.assertIs(other.part, other.part)
    self.assertEqual(box.frames, 2)

  def test_write_then_read(self) -> None:
    class Owner:
      n = CountingBox[int](1)

    owner = Owner()
    owner.n = 5
    self.assertEqual(Owner.n.frames, 1)
    self.assertEqual(owner.n, 5)
    self.assertEqual(owner.n, 5)
    self.assertEqual(Owner.n.frames, 1)

  def test_read_callbacks_go_the_full_way(self) -> None:
    before = []
    after = []

    class Owner:
      early = CountingBox[int](1)
      late = CountingBox[int](2)

      @early.preGet
      def _early(self) -> None:
        before.append(self)

      @late.onGet
      def _late(self, value: int) -> None:
        after.append(value)

    owner = Owner()
    for _ in range(3):
      self.assertEqual(owner.early, 1)
      self.assertEqual(owner.late, 2)
    self.assertEqual(before, [owner, owner, owner])
    self.assertEqual(after, [2, 2, 2])
    self.assertEqual(Owner.early.frames, 3)
    self.assertEqual(Owner.late.frames, 3)

  def test_callback_registered_after_reads(self) -> None:
    seen = []

    class Owner:
      n = CountingBox[int](1)

    owner = Owner()
    self.assertEqual((owner.n, owner.n), (1, 1))
    self.assertEqual(Owner.n.frames, 1)

    class Child(Owner):
      @Owner.n.onGet
      def _saw(self, value: int) -> None:
        seen.append(value)

    child = Child()
    self.assertEqual((child.n, child.n), (1, 1))
    self.assertEqual(seen, [1, 1])
    self.assertEqual(Owner.n.frames, 3)

  def test_overridden_hooks_go_the_full_way(self) -> None:
    calls = []

    class Before(CountingBox):
      def hookPreGet(self, instance: object, **kwargs) -> None:
        calls.append('before')

    class After(CountingBox):
      def hookOnGet(self, instance: object, value: object, **kwargs) -> None:
        calls.append('after')

    class Fetch(CountingBox):
      def __instance_get__(self, instance: object, owner: type,
          **kwargs) -> object:
        calls.append('fetch')
        return AttriBox.__instance_get__(self, instance, owner, **kwargs)

    class Owner:
      before = Before[int](1)
      after = After[int](2)
      fetch = Fetch[int](3)

    owner = Owner()
    for name, value in (('before', 1), ('after', 2), ('fetch', 3)):
      with self.subTest(name=name):
        box = getattr(Owner, name)
        self.assertEqual(getattr(owner, name), value)
        del calls[:]
        for _ in range(3):
          self.assertEqual(getattr(owner, name), value)
        self.assertEqual(calls, [name, name, name])
        self.assertEqual(box.frames, 4)
        self.assertIs(box.__reads_plainly__, False)

  def test_deleted_value_refused(self) -> None:
    class Owner:
      n = CountingBox[int](1)

    owner = Owner()
    self.assertEqual((owner.n, owner.n), (1, 1))
    del owner.n
    frames = Owner.n.frames
    with self.assertRaises(MissingVariable) as context:
      _ = owner.n
    self.assertEqual(context.exception.varName, 'n')
    self.assertIs(context.exception.instance, owner)
    self.assertEqual(context.exception.expectedTypes, (object,))
    self.assertIn("'Owner.n: object'", str(context.exception))
    self.assertEqual(Owner.n.frames, frames + 1)
    owner.n = 6
    self.assertEqual((owner.n, owner.n), (6, 6))

  def test_value_is_never_asked(self) -> None:
    asked = []

    class Agreeable:
      """A value claiming to equal whatever it is compared with."""

      def __eq__(self, other: object) -> bool:
        asked.append(other)
        return True

      def __ne__(self, other: object) -> bool:
        asked.append(other)
        return False

      __hash__ = object.__hash__

    class Owner:
      value = CountingBox[Agreeable]()

    owner = Owner()
    built = owner.value
    frames = Owner.value.frames
    del asked[:]
    for _ in range(3):
      self.assertIs(owner.value, built)
    self.assertEqual(asked, [])
    self.assertEqual(Owner.value.frames, frames)
    #  The value does answer when it is asked.
    self.assertTrue(built == 5)
    self.assertFalse(built != 5)
    self.assertEqual(asked, [5, 5])

  def test_storage_name_that_is_no_name(self) -> None:
    class Owner:
      n = CountingBox[int](1)

    owner = Owner()
    self.assertEqual(owner.n, 1)
    object.__setattr__(Owner.n, '__storage_name__', 5)
    with self.assertRaises(TypeException) as context:
      _ = owner.n
    self.assertEqual(context.exception.varName, '__storage_name__')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'__storage_name__'", str(context.exception))
