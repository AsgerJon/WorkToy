"""TestSpaceUmbrella provides coverage gymnastics for the
'AbstractNamespace' from the 'worktoy.space' module."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls.space_hooks import AbstractSpaceHook, SpaceDesc
from worktoy.waitaminute.meta import ReservedName
from .. import MCLSTest

from worktoy.mcls import BaseObject, BaseSpace, BaseMeta

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Dict, Optional, TypeAlias, Self


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
