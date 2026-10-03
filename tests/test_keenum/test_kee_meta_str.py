"""
TestKeeMetaStr subclasses 'KeeTest' and pins the 'str()' of an
enumeration class. It counted one member as "1 members", and named the
kind 'KeeNum' for an enumeration of a custom metaclass too, whose root is
not 'KeeNum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeMeta

from . import KeeTest


class Single(KeeNum):
  """Single has one member."""
  A = Kee[int](1)


class FontMeta(KeeMeta):
  """FontMeta is a custom metaclass with a root of its own."""


class Font(FontMeta.keeNum):
  """Font is an enumeration of the custom metaclass."""
  ARIAL = Kee[int](1)
  TIMES = Kee[int](2)


class TestKeeMetaStr(KeeTest):
  """
  TestKeeMetaStr provides tests for the 'str()' of an enumeration class.
  """

  def test_single_member(self) -> None:
    """One member is a member."""
    self.assertEqual(str(Single), "<KeeNum 'Single': 1 member>")

  def test_custom_metaclass(self) -> None:
    """The kind is the root of the metaclass."""
    self.assertEqual(str(Font), "<FontMetaNum 'Font': 2 members>")
