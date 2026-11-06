"""
TestReservedNamespaceHook tests 'ReservedNamespaceHook' from
'worktoy.mcls.space_hooks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractNamespace, BaseMeta, BaseSpace, BaseObject
from worktoy.waitaminute.meta import ReservedName
from . import MclsTest


class TestReservedNamespaceHook(MclsTest):
  """
  'ReservedNamespaceHook' lets the interpreter bind a reserved name once
  and refuses a class body binding it again. The tests pin the refusal
  of a rebound module, qualified name and docstring, the first binding
  of a reserved name the interpreter left out, the hook called by hand
  through a namespace, and that ordinary names pass.
  """

  def test_rebound_module_refused(self) -> None:
    with self.assertRaises(ReservedName) as context:
      class A(BaseObject):
        __module__ = 'elsewhere'

    self.assertEqual(context.exception.resName, '__module__')
    self.assertIn('__module__', str(context.exception))

  def test_rebound_qualname_refused(self) -> None:
    with self.assertRaises(ReservedName) as context:
      class A(BaseObject):
        __qualname__ = 'Other'

    self.assertEqual(context.exception.resName, '__qualname__')
    self.assertIn("'__qualname__'", str(context.exception))

  def test_rebound_doc_refused(self) -> None:
    with self.assertRaises(ReservedName) as context:
      class A(BaseObject):
        """The docstring binds '__doc__' first."""
        __doc__ = 'second'

    self.assertEqual(context.exception.resName, '__doc__')
    self.assertIn("'__doc__'", str(context.exception))

  def test_first_binding_passes(self) -> None:
    class A(BaseObject):
      __doc__ = 'given by the body'
      __match_args__ = ('x',)

    self.assertEqual(A.__doc__, 'given by the body')
    self.assertEqual(A.__match_args__, ('x',))
    with self.assertRaises(ReservedName) as context:
      class B(BaseObject):
        __match_args__ = ('x',)
        __match_args__ = ('y',)

    self.assertEqual(context.exception.resName, '__match_args__')
    self.assertIn("'__match_args__'", str(context.exception))

  def test_by_hand_through_namespace(self) -> None:
    space = BaseSpace(BaseMeta, 'A', ())
    space['__module__'] = 'first'
    self.assertEqual(space['__module__'], 'first')
    with self.assertRaises(ReservedName) as context:
      space['__module__'] = 'second'
    self.assertEqual(context.exception.resName, '__module__')
    self.assertIn("reserved name: '__module__'", str(context.exception))
    self.assertEqual(space['__module__'], 'first')
    hook = AbstractNamespace.__dict__['reservedNameHook']
    bound = hook.__get__(space, BaseSpace)
    self.assertFalse(bound.setItemPhase('__name__', 'x'))
    self.assertFalse(bound.setItemPhase('plain', 'x', 'old'))

  def test_random_names_pass(self) -> None:
    space = BaseSpace(BaseMeta, 'A', ())
    self.randomWord.size = 8
    for word in self.randomWord.row:
      space[word] = 1
      space[word] = 2
      with self.subTest(word=word):
        self.assertEqual(space[word], 2)
