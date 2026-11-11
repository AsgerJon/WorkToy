"""
TestKeeFlagsHook tests 'KeeFlagsHook' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import warnings

from worktoy.keenum import KeeFlags, KeeFlag, KeeFlagsSpace, KeeFlagsMeta
from worktoy.keenum import KeeFlagsHook, Kee
from worktoy.waitaminute import DeprecatedPromise
from worktoy.waitaminute.keenum import KeeMemberNameError
from . import KeenumTest, Permission


class TestKeeFlagsHook(KeenumTest):
  """
  'KeeFlagsHook' takes every 'Kee', and every deprecated 'KeeFlag', from
  the class body for the namespace's record and leaves every other
  binding alone; a body name that a member takes is refused as the class
  is created. The tests pin the claim, the plain bindings, the refusal
  and the hook by hand.
  """

  def test_flags_claimed(self) -> None:
    space = Permission.__namespace__
    for name in ('READ', 'WRITE', 'EXEC'):
      with self.subTest(name=name):
        self.assertFalse(dict.__contains__(space, name))
        self.assertIsInstance(space[name], Kee)
    self.assertIsInstance(KeeFlagsSpace.classGetHooks()[-1], KeeFlagsHook)
    self.assertIs(KeeFlagsSpace.__dict__['keeFlagsHook'],
                  KeeFlagsSpace.classGetHooks()[-1])

  def test_plain_bindings_kept(self) -> None:
    class Local(KeeFlags):
      READ = Kee[str]()
      label = 'plain'

      def describe(self) -> str:
        return '%s:%s' % (self.label, self.name)

    self.assertEqual(Local.label, 'plain')
    self.assertEqual(Local.READ.describe(), 'plain:READ')

  def test_member_name_bound_plainly_refused(self) -> None:
    with self.assertRaises(KeeMemberNameError) as context:
      class Local(KeeFlags):
        READ = Kee[str]()
        WRITE = Kee[str]()
        READ_WRITE = 'rw'

    self.assertEqual(context.exception.clsName, 'Local')
    self.assertEqual(context.exception.memberName, 'READ_WRITE')
    self.assertIn("enumeration class 'Local' binds 'READ_WRITE'",
                  str(context.exception))
    with self.assertRaises(KeeMemberNameError) as context:
      class Nulled(KeeFlags):
        NULL = 0
        READ = Kee[str]()

    self.assertEqual(context.exception.clsName, 'Nulled')
    self.assertEqual(context.exception.memberName, 'NULL')
    self.assertIn("enumeration class 'Nulled' binds 'NULL'",
                  str(context.exception))

  def test_by_hand(self) -> None:
    space = KeeFlagsSpace(KeeFlagsMeta, 'Hand', ())
    hook = KeeFlagsSpace.__dict__['keeFlagsHook'].__get__(space,
                                                           KeeFlagsSpace)
    self.assertTrue(hook.setItemPhase('READ', Kee[str]()))
    with warnings.catch_warnings():
      warnings.simplefilter('ignore', DeprecatedPromise)
      self.assertTrue(hook.setItemPhase('WRITE', KeeFlag()))
    self.assertFalse(hook.setItemPhase('label', 'plain'))
    self.assertEqual([*space.getDeclaredFlags()], ['READ', 'WRITE'])

  def test_random_plain_names_pass(self) -> None:
    space = KeeFlagsSpace(KeeFlagsMeta, 'Hand', ())
    hook = KeeFlagsSpace.__dict__['keeFlagsHook'].__get__(space,
                                                           KeeFlagsSpace)
    self.randomWord.size = 5
    for word in self.randomWord.row:
      with self.subTest(word=word):
        self.assertFalse(hook.setItemPhase(word, word))
