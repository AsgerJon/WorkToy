"""
TestKeeSpaceHook tests 'KeeSpaceHook' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeSpace, KeeSpaceHook, KeeMeta
from worktoy.waitaminute.keenum import KeeMemberNameError
from worktoy.waitaminute.meta import UnboundClassHook
from . import KeenumTest


class TestKeeSpaceHook(KeenumTest):
  """
  'KeeSpaceHook' takes every 'Kee' from the class body for the
  namespace's record, refuses a member's name bound twice in either
  order, and refuses a '__class_resolve__' that is no classmethod. The
  tests pin each on class statements and on the hook called by hand.
  """

  def test_kee_claimed(self) -> None:
    class Local(KeeNum):
      A = Kee[int](1)
      other = 'plain'

    space = Local.__namespace__
    self.assertFalse(dict.__contains__(space, 'A'))
    self.assertIsInstance(space['A'], Kee)
    self.assertTrue(dict.__contains__(space, 'other'))
    self.assertEqual(Local.other, 'plain')
    self.assertIs(KeeSpace.__dict__['keeSpaceHook'],
                  KeeSpace.classGetHooks()[-1])
    self.assertIsInstance(KeeSpace.classGetHooks()[-1], KeeSpaceHook)

  def test_plain_value_at_a_member_name_refused(self) -> None:
    with self.assertRaises(KeeMemberNameError) as context:
      class Local(KeeNum):
        A = Kee[int](1)
        A = 'plain'

    self.assertEqual(context.exception.clsName, 'Local')
    self.assertEqual(context.exception.memberName, 'A')
    self.assertIn("'A'", str(context.exception))

  def test_member_at_a_plain_name_refused(self) -> None:
    with self.assertRaises(KeeMemberNameError) as context:
      class Local(KeeNum):
        A = 'plain'
        A = Kee[int](1)

    self.assertEqual(context.exception.clsName, 'Local')
    self.assertEqual(context.exception.memberName, 'A')
    self.assertIn("The class body of enumeration class 'Local' binds 'A'",
                  str(context.exception))

  def test_inherited_member_name_refused(self) -> None:
    class Base(KeeNum):
      A = Kee[int](1)

    with self.assertRaises(KeeMemberNameError) as context:
      class Sub(Base):
        A = 'plain'

    self.assertEqual(context.exception.clsName, 'Sub')
    self.assertEqual(context.exception.memberName, 'A')
    self.assertIn("The class body of enumeration class 'Sub' binds 'A'",
                  str(context.exception))

  def test_class_resolve_must_be_a_classmethod(self) -> None:
    def resolve(cls, identifier: object) -> object:
      """Neither a classmethod nor refused by Python."""

    for value in (resolve, staticmethod(resolve)):
      with self.subTest(value=type(value).__name__):
        with self.assertRaises(UnboundClassHook) as context:
          class Local(KeeNum):
            A = Kee[int](1)
            __class_resolve__ = value

        self.assertEqual(context.exception.className, 'Local')
        self.assertEqual(context.exception.hookName, '__class_resolve__')
        self.assertIsNone(context.exception.baseName)
        self.assertIn("The class body of 'Local' binds '__class_resolve__'",
                      str(context.exception))
        self.assertIn("'@classmethod'", str(context.exception))

  def test_by_hand(self) -> None:
    space = KeeSpace(KeeMeta, 'Hand', ())
    hook = KeeSpace.__dict__['keeSpaceHook'].__get__(space, KeeSpace)
    self.assertFalse(hook.setItemPhase('plain', 1))
    self.assertTrue(hook.setItemPhase('A', Kee[int](1)))
    self.assertTrue(space.hasNum('A'))
    self.assertFalse(hook.setItemPhase('__class_resolve__', None))
    self.assertFalse(hook.setItemPhase('__class_resolve__',
                                       classmethod(lambda cls, i: i)))

  def test_random_plain_names_pass(self) -> None:
    space = KeeSpace(KeeMeta, 'Hand', ())
    hook = KeeSpace.__dict__['keeSpaceHook'].__get__(space, KeeSpace)
    self.randomWord.size = 6
    for word in self.randomWord.row:
      with self.subTest(word=word):
        self.assertFalse(hook.setItemPhase(word, word))

  def test_resolver_name_by_equality_and_its_neighbours(self) -> None:
    space = KeeSpace(KeeMeta, 'Hand', ())
    hook = [h for h in space.getHooks() if isinstance(h, KeeSpaceHook)][0]

    def plain(cls, identifier) -> None:
      """A resolver written without classmethod."""

    with self.assertRaises(UnboundClassHook) as context:
      hook.setItemPhase(str.join('', ['__class_', 'resolve__']), plain)
    self.assertEqual(context.exception.className, 'Hand')
    self.assertEqual(context.exception.hookName, '__class_resolve__')
    self.assertIsNone(context.exception.baseName)
    self.assertIn("The class body of 'Hand' binds '__class_resolve__'",
                  str(context.exception))
    self.assertFalse(hook.setItemPhase('describe', plain))
    self.assertFalse(hook.setItemPhase('__bool__', plain))
    self.assertFalse(hook.setItemPhase('__str__', plain))
