"""
TestAbstractNamespaceHooks tests the hook registry of 'AbstractNamespace'
from 'worktoy.mcls'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractNamespace, BaseSpace
from worktoy.mcls.space_hooks import ReservedNamespaceHook, NamespaceHook
from worktoy.mcls.space_hooks import LoadSpaceHook
from worktoy.waitaminute.meta import DuplicateHook
from . import MclsTest, LoggingHook, LoggedSpace, ClaimedSpace, LoggedMeta


class TestAbstractNamespaceHooks(MclsTest):
  """
  A namespace class runs the hooks its bases declared and then its own,
  each once, in a fixed order, and refuses a second hook at a name a
  base's hook holds. The tests pin the order on the namespace classes of
  the folder, the list each class keeps, the registration of the same
  hook twice, the refusal, and the binding of every hook to the
  namespace reading it.
  """

  def test_every_namespace_has_two_hooks(self) -> None:
    hooks = AbstractNamespace.classGetHooks()
    self.assertEqual(len(hooks), 2)
    self.assertIsInstance(hooks[0], ReservedNamespaceHook)
    self.assertIsInstance(hooks[1], NamespaceHook)
    self.assertIs(hooks[0], AbstractNamespace.__dict__['reservedNameHook'])
    self.assertIs(hooks[1], AbstractNamespace.__dict__['nameHook'])

  def test_bases_first_then_own(self) -> None:
    base = AbstractNamespace.classGetHooks()
    self.assertEqual(BaseSpace.classGetHooks()[:2], base)
    self.assertIsInstance(BaseSpace.classGetHooks()[2], LoadSpaceHook)
    self.assertEqual(LoggedSpace.classGetHooks()[:2], base)
    self.assertIs(LoggedSpace.classGetHooks()[2],
                  LoggedSpace.__dict__['loggingHook'])
    claimed = ClaimedSpace.classGetHooks()
    self.assertEqual(claimed[:3], LoggedSpace.classGetHooks())
    names = [hook.getFieldName() for hook in claimed[3:]]
    self.assertEqual(names, ['claimingHook', 'refusingHook', 'swappingHook'])

  def test_each_hook_once(self) -> None:
    hooks = ClaimedSpace.classGetHooks()
    self.assertEqual(len(hooks), 6)
    self.assertEqual(len(set(map(id, hooks))), 6)

  def test_list_kept_on_each_class(self) -> None:
    name = AbstractNamespace.getHookListName()
    self.assertEqual(name, '__hook_objects__')
    self.assertEqual(len(AbstractNamespace.__dict__[name]), 2)
    self.assertEqual(len(LoggedSpace.__dict__[name]), 3)
    self.assertEqual(len(ClaimedSpace.__dict__[name]), 6)
    self.assertEqual(ClaimedSpace.__dict__[name],
                     ClaimedSpace.classGetHooks())

  def test_same_hook_again_is_nothing(self) -> None:
    hook = LoggedSpace.__dict__['loggingHook']
    before = LoggedSpace.classGetHooks()
    LoggedSpace.addHook(hook)
    self.assertEqual(LoggedSpace.classGetHooks(), before)

  def test_second_hook_at_a_name_refused(self) -> None:
    with self.assertRaises((DuplicateHook, RuntimeError)) as context:
      class Other(LoggedSpace):
        loggingHook = LoggingHook()

    exception = context.exception.__cause__ or context.exception
    self.assertEqual(exception.owner.__name__, 'Other')
    self.assertEqual(exception.name, 'loggingHook')
    self.assertIs(exception.existingHook,
                  LoggedSpace.__dict__['loggingHook'])
    self.assertIsInstance(exception.newHook, LoggingHook)
    self.assertIn("'Other'", str(exception))

    stray = LoggingHook()
    object.__setattr__(stray, '__field_name__',
                       str.join('', ['logging', 'Hook']))
    with self.assertRaises(DuplicateHook) as context:
      LoggedSpace.addHook(stray)
    exception = context.exception
    self.assertIs(exception.owner, LoggedSpace)
    self.assertEqual(exception.name, 'loggingHook')
    self.assertIs(exception.existingHook,
                  LoggedSpace.__dict__['loggingHook'])
    self.assertIs(exception.newHook, stray)
    self.assertIn("'LoggedSpace'", str(exception))

  def test_same_hook_means_the_same_object(self) -> None:
    class Agreeing(LoggingHook):
      def __eq__(self, other: object) -> bool:
        return True

    agreeing = Agreeing()
    self.assertTrue(agreeing == object())
    object.__setattr__(agreeing, '__field_name__', 'loggingHook')
    with self.assertRaises(DuplicateHook) as context:
      LoggedSpace.addHook(agreeing)
    self.assertIs(context.exception.newHook, agreeing)
    self.assertIs(context.exception.owner, LoggedSpace)
    self.assertEqual(context.exception.name, 'loggingHook')
    self.assertIs(context.exception.existingHook,
                  LoggedSpace.__dict__['loggingHook'])
    self.assertIn("'loggingHook'", str(context.exception))

  def test_hook_added_to_base_reaches_subclasses(self) -> None:
    class Space(AbstractNamespace):
      """A namespace class with the two hooks every namespace has."""

    class Sub(Space):
      own = LoggingHook()

    late = LoggingHook()
    object.__setattr__(late, '__field_name__', 'late')
    Space.addHook(late)
    names = [hook.getFieldName() for hook in Sub.classGetHooks()]
    self.assertEqual(names, ['reservedNameHook', 'nameHook', 'own', 'late'])

  def test_hooks_bound_to_namespace(self) -> None:
    space = ClaimedSpace(LoggedMeta, 'A', ())
    bound = [*space.getHooks()]
    self.assertEqual(bound, ClaimedSpace.classGetHooks())
    for hook in bound:
      with self.subTest(hook=hook.getFieldName()):
        self.assertIs(hook.space, space)
