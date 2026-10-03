"""
TestShadowedClassHook subclasses 'MCLSTest' and pins the refusal of a
routed '__class_*__' hook bound in the body of a class whose metaclass
implements the operation itself. 'AbstractMetaclass' calls each hook from
its own implementation of the operation, so a metaclass implementing
'__len__' again never reaches a '__class_len__', and such a hook used to
be accepted without a word. The namespace raises 'ShadowedClassHook' at
the line binding it instead, naming the metaclass and the method that
take the operation over.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseMeta, BaseObject, AbstractNamespace
from worktoy.waitaminute.meta import ShadowedClassHook

from .. import MCLSTest


class CountMeta(BaseMeta):
  """
  CountMeta measures its classes itself, by the number of names in their
  namespaces, and so never asks a '__class_len__' hook.
  """

  def __len__(cls) -> int:
    return len(cls.__dict__)


class Counted(BaseObject, metaclass=CountMeta):
  """
  Counted is a class of 'CountMeta', so its subclasses are measured by
  the metaclass.
  """


class InitMeta(BaseMeta):
  """
  InitMeta implements '__init__' and hands over to the inherited one, as
  every metaclass '__init__' does, so the '__class_init__' hook still
  runs.
  """

  def __init__(cls, name: str, bases: tuple, space: dict, **kwargs) -> None:
    cls.seen = ['meta']
    BaseMeta.__init__(cls, name, bases, space, **kwargs)


class TestShadowedClassHook(MCLSTest):
  """
  TestShadowedClassHook provides tests for the refusal of a class hook
  whose operation the metaclass implements itself.
  """

  def test_shadowed_hook_refused(self) -> None:
    """A '__class_len__' under a metaclass implementing '__len__' raises
    at the class statement, naming the class, the hook, the metaclass and
    the method."""
    with self.assertRaises(ShadowedClassHook) as context:
      class Foo(Counted):
        @classmethod
        def __class_len__(cls) -> int:
          return 69  # pragma: no cover
    e = context.exception
    self.assertEqual(e.className, 'Foo')
    self.assertEqual(e.hookName, '__class_len__')
    self.assertEqual(e.metaclassName, 'CountMeta')
    self.assertEqual(e.methodName, '__len__')
    self.assertEqual(e.msg, str(e))
    self.assertEqual(str(e), repr(e))
    self.assertIn("'CountMeta'", str(e))
    self.assertIn("'__len__'", str(e))
    self.assertIn("'__class_len__'", str(e))

  def test_inherited_implementation_named(self) -> None:
    """A metaclass derived from 'CountMeta' inherits its '__len__', and
    the exception names 'CountMeta', which implements it."""

    class SubCountMeta(CountMeta):
      pass

    with self.assertRaises(ShadowedClassHook) as context:
      class Foo(BaseObject, metaclass=SubCountMeta):
        @classmethod
        def __class_len__(cls) -> int:
          return 69  # pragma: no cover
    self.assertEqual(context.exception.metaclassName, 'CountMeta')

  def test_shadowed_before_unbound(self) -> None:
    """A plain function at a shadowed hook name is refused as shadowed,
    since no form of the hook could run."""
    with self.assertRaises(ShadowedClassHook):
      class Foo(Counted):
        def __class_len__(cls) -> int:
          return 69  # pragma: no cover

  def test_routed_hook_accepted(self) -> None:
    """A hook for an operation the metaclass leaves to
    'AbstractMetaclass' is accepted and called, beside the operation the
    metaclass implements."""

    class Foo(Counted):
      @classmethod
      def __class_str__(cls) -> str:
        return 'Foo!'

    self.assertEqual(str(Foo), 'Foo!')
    self.assertEqual(len(Foo), len(Foo.__dict__))

  def test_class_init_accepted(self) -> None:
    """A '__class_init__' is accepted under a metaclass implementing
    '__init__', and runs from the inherited '__init__'."""

    class Foo(BaseObject, metaclass=InitMeta):
      @classmethod
      def __class_init__(cls, *args, **kwargs) -> None:
        cls.seen.append('hook')

    self.assertEqual(Foo.seen, ['meta', 'hook'])

  def test_base_object_hooks_unaffected(self) -> None:
    """'BaseMeta' implements none of the operations, so every hook on a
    'BaseObject' is accepted, '__class_call__' included."""

    class Foo(BaseObject):
      @classmethod
      def __class_len__(cls) -> int:
        return 3

      @classmethod
      def __class_call__(cls, *args, **kwargs) -> str:
        return 'called'

    self.assertEqual(len(Foo), 3)
    self.assertEqual(Foo(), 'called')

  def test_namespace_of_plain_metaclass(self) -> None:
    """A namespace built for a metaclass not based on 'AbstractMetaclass'
    calls no hook, and refuses none."""
    space = AbstractNamespace(type, 'Foo', ())
    space['__class_len__'] = classmethod(lambda cls: 3)
    self.assertIn('__class_len__', space)
