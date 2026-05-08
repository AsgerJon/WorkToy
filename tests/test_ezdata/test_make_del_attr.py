"""Tests for ``makeDelAttr``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute.ez import EZDeleteException
from . import EZTest
from ._factory_helpers import build, slot


class TestMakeDelAttr(EZTest):

  def test_always_raises(self) -> None:
    cls = build([slot('a', int, 0)])
    obj = cls()
    with self.assertRaises(EZDeleteException):
      del obj.a
