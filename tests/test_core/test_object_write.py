"""
TestObjectWrite tests the write protocol of 'Object' from 'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.waitaminute.desc import ReadOnlyError
from . import CoreTest, Noisy, Quiet, Skipper


class TestObjectWrite(CoreTest):
  """
  A write through an instance runs with its frame in place and the
  write hooks around '__instance_set__': the hook before sees the value
  as assigned and may end the write with 'SkipSet', the hook after sees
  the value as stored. The default refuses every write, which keeps a
  worktoy value in a class body from being replaced. The tests pin each
  of these and that the frame is gone afterwards, whatever happened.
  """

  def test_default_write_refused(self) -> None:
    class Owner:
      d = Object()

    owner = Owner()
    with self.assertRaises(ReadOnlyError) as context:
      owner.d = 5
    self.assertIs(context.exception.instance, owner)
    self.assertIs(context.exception.desc, Owner.d)
    self.assertEqual(context.exception.newVal, 5)
    self.assertIn("'Owner.d'", str(context.exception))
    self.assertIn('new value: 5!', str(context.exception))
    self.assertFalse(Owner.d.hasContext())
    self.assertIs(owner.d, Owner.d)

  def test_hooks_see_assigned_then_stored(self) -> None:
    class Owner:
      n = Noisy()

      def __init__(self) -> None:
        self.log = []

    owner = Owner()
    owner.n = 5
    self.assertEqual(owner.log,
                     [('preSet', 5), ('set', '5'), ('onSet', '5')])
    self.assertFalse(Owner.n.hasContext())

  def test_on_set_gets_assigned_value_when_nothing_reported(self) -> None:
    class Owner:
      q = Quiet()

      def __init__(self) -> None:
        self.log = []

    owner = Owner()
    owner.q = 5
    self.assertEqual(owner.log, [('onSet', 5, True, Owner)])
    self.assertEqual(owner.q, 5)

  def test_skip_set_ends_write_silently(self) -> None:
    class Owner:
      s = Skipper()

      def __init__(self) -> None:
        self.log = []

    owner = Owner()
    owner.s = 1
    self.assertEqual(owner.log, [('set', 1), ('onSet', 1)])
    owner.s = 1
    self.assertEqual(owner.log, [('set', 1), ('onSet', 1)])
    owner.s = 2
    self.assertEqual(owner.log, [
      ('set', 1), ('onSet', 1), ('set', 2), ('onSet', 2),
    ])
    self.assertEqual(owner.s, 2)
    self.assertFalse(Owner.s.hasContext())

  def test_frame_popped_when_write_raises(self) -> None:
    class Loud:
      def __str__(self) -> str:
        raise ValueError('loud')

    class Owner:
      n = Noisy()

      def __init__(self) -> None:
        self.log = []

    owner = Owner()
    with self.assertRaises(ValueError) as context:
      owner.n = Loud()
    self.assertEqual(str(context.exception), 'loud')
    self.assertFalse(Owner.n.hasContext())
    self.assertEqual(len(owner.log), 1)

  def test_random_writes(self) -> None:
    class Owner:
      q = Quiet()

      def __init__(self) -> None:
        self.log = []

    owner = Owner()
    for word in self.randomWord.row:
      owner.q = word
      with self.subTest(word=word):
        self.assertEqual(owner.q, word)
