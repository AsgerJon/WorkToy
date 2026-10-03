"""
TestMixinClassHook subclasses 'MCLSTest' and pins that a class hook such
as '__class_str__', defined on a plain mixin, reaches a class of a
worktoy metaclass without worktoy bases. The namespace marks every class
hook the class does not define with 'METACALL', and looked for a
definition only in the class body and in the namespaces of worktoy
bases, so the mark hid the hook of the mixin.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseMeta, BaseObject

from .. import MCLSTest


class Mixin:
  """Mixin is a plain class providing a class hook."""

  @classmethod
  def __class_str__(cls) -> str:
    return 'mixin %s' % cls.__name__


class TestMixinClassHook(MCLSTest):
  """
  TestMixinClassHook provides tests for a class hook of a plain mixin.
  """

  def test_mixin_alone(self) -> None:
    """The hook of a mixin reaches a class without worktoy bases."""

    class Foo(Mixin, metaclass=BaseMeta):
      pass

    self.assertEqual(str(Foo), 'mixin Foo')

  def test_mixin_with_worktoy_base(self) -> None:
    """The hook of a mixin before a worktoy base reaches the class, as
    before."""

    class Foo(Mixin, BaseObject):
      pass

    self.assertEqual(str(Foo), 'mixin Foo')

  def test_no_hook(self) -> None:
    """Without a hook anywhere, the metaclass renders the class."""

    class Foo(metaclass=BaseMeta):
      pass

    self.assertIn('Foo', str(Foo))
    self.assertIn('BaseMeta', str(Foo))
