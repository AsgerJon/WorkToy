"""
TestAbstractSpaceHook tests 'AbstractSpaceHook' from
'worktoy.mcls.space_hooks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.mcls import AbstractNamespace
from worktoy.mcls.space_hooks import AbstractSpaceHook
from . import MclsTest, LoggedSpace, LoggedMeta


class TestAbstractSpaceHook(MclsTest):
  """
  'AbstractSpaceHook' is the piece a namespace is assembled from: it
  registers itself with the namespace class it is declared in, binds to
  the namespace that reads it, and does nothing in any phase unless a
  subclass says otherwise. The tests pin the defaults of the seven
  phases, the registration, the refusal of a plain owner, and the two
  routes of the read.
  """

  def test_phase_defaults(self) -> None:
    hook = AbstractSpaceHook()
    space = LoggedSpace(LoggedMeta, 'A', ())
    compiled = {'x': 1}
    self.assertIsNone(hook.preparePhase(space))
    self.assertIsNone(hook.getItemPhase('x', 1))
    self.assertFalse(hook.setItemPhase('x', 1))
    self.assertFalse(hook.setItemPhase('x', 1, 0))
    self.assertFalse(hook.delItemPhase('x'))
    self.assertFalse(hook.delItemPhase('x', 1))
    self.assertIs(hook.preCompilePhase(compiled), compiled)
    self.assertIs(hook.postCompilePhase(compiled), compiled)
    self.assertEqual(compiled, {'x': 1})
    self.assertIs(hook.newClassPhase(int), int)

  def test_is_an_object(self) -> None:
    self.assertIsSubclass(AbstractSpaceHook, Object)
    hook = AbstractSpaceHook(1, k=2)
    self.assertEqual(hook.getPosArgs(), (1,))
    self.assertEqual(hook.getKeyArgs(), {'k': 2})

  def test_declared_in_namespace_class_registers(self) -> None:
    class Space(AbstractNamespace):
      extra = AbstractSpaceHook()

    hook = Space.__dict__['extra']
    self.assertIs(Space.classGetHooks()[-1], hook)
    self.assertEqual(hook.getFieldName(), 'extra')
    self.assertIs(hook.getFieldOwner(), Space)
    self.assertNotIn(hook, AbstractNamespace.classGetHooks())

  def test_declared_in_plain_class_fails(self) -> None:
    with self.assertRaises((AttributeError, RuntimeError)):
      class Plain:
        extra = AbstractSpaceHook()

    hook = AbstractSpaceHook()
    with self.assertRaises(AttributeError):
      hook.__set_name__(int, 'extra')

  def test_read_through_class_gives_hook(self) -> None:
    hook = LoggedSpace.__dict__['loggingHook']
    self.assertIs(LoggedSpace.loggingHook, hook)
    self.assertIs(hook.__get__(None, LoggedSpace), hook)

  def test_read_through_namespace_binds(self) -> None:
    space = LoggedSpace(LoggedMeta, 'A', ())
    hook = LoggedSpace.__dict__['loggingHook']
    self.assertIs(hook.__get__(space, LoggedSpace), hook)
    self.assertIs(hook.space, space)
    for bound in space.getHooks():
      with self.subTest(hook=type(bound).__name__):
        self.assertIs(bound.space, space)
