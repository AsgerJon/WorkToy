"""TestSpaceUmbrella provides coverage gymnastics for the
'AbstractNamespace' from the 'worktoy.space' module."""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls.space_hooks import AbstractSpaceHook, SpaceDesc
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.meta import ReservedName
from .. import MCLSTest
from worktoy.mcls import BaseObject, AbstractNamespace, AbstractMetaclass

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestSpaceUmbrella(MCLSTest):
  """
  TestSpaceUmbrella provides coverage gymnastics for the
  'AbstractNamespace' from the 'worktoy.space' module.
  """

  def test_reserved_name(self) -> None:
    """Test ReservedNamespaceHook"""
    with self.assertRaises(ReservedName) as context:
      class Breh(BaseObject):
        __match_args__ = 'Never'
        __match_args__ = 'Gonna'
        # __match_args__ = 'Give'
        # __match_args__ = 'You'
        # __match_args__ = 'Up'
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.resName, '__match_args__')

  def test_hook_space_descriptor(self) -> None:
    """Test ReservedNamespaceHook"""
    desc = AbstractSpaceHook.space
    self.assertIsInstance(desc, SpaceDesc)

  def test_pre_compile_good(self, ) -> None:
    """
    This method tests the 'preCompile' method receiving a good type.
    """

    class EmptySpace(AbstractNamespace):
      __owner_hooks_list_name__: str = 'never_gonna_give_you_up'

    space = dict()
    preCompiled = EmptySpace(AbstractMetaclass, '_', (), ).preCompile(space)
    self.assertIsInstance(preCompiled, dict)

  def test_pre_compile_bad_type(self, ) -> None:
    """
    This method tests the 'preCompile' method receiving a bad type.
    """

    class EmptySpace(AbstractNamespace):
      __owner_hooks_list_name__: str = 'never_gonna_give_you_up'

    susSpace = """Imma 'dict' bro, trust me!"""
    with self.assertRaises(TypeException) as context:
      # noinspection PyTypeChecker
      _ = EmptySpace(type, '_', (), ).preCompile(susSpace)
    e = context.exception
    self.assertEqual(e.varName, 'namespace')
    self.assertEqual(e.actualObject, susSpace)
    self.assertIs(e.actualType, str)
    self.assertIn(dict, e.expectedTypes)
    self.assertEqual(str(e), repr(e))
