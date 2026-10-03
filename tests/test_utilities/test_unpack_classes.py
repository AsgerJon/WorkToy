"""
TestUnpackClasses subclasses 'UtilitiesTest' and pins that 'unpack' keeps
whole an object that claims to be iterable but refuses iteration, as
every worktoy class does: its metaclass defines '__iter__' for the
'__class_iter__' hook, so 'isinstance(cls, Iterable)' answers 'True' for
any of them, and iterating one without the hook raises 'TypeError'.
'unpack' used to trust the claim, so 'unpack([BaseObject, int])' raised.
An enumeration, which does iterate, is still flattened.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Iterable

from worktoy.keenum import KeeNum, Kee
from worktoy.mcls import BaseObject
from worktoy.utilities import unpack, joinWords

from . import UtilitiesTest


class Color(KeeNum):
  """Color is an enumeration, which iterates over its members."""

  RED = Kee[int](1)
  BLUE = Kee[int](2)


class TestUnpackClasses(UtilitiesTest):
  """
  TestUnpackClasses provides tests for 'unpack' given worktoy classes.
  """

  def test_class_kept_whole(self) -> None:
    """A worktoy class that does not iterate is kept whole."""
    self.assertIsInstance(BaseObject, Iterable)
    self.assertEqual(unpack([BaseObject, int]), (BaseObject, int))
    self.assertEqual(unpack(BaseObject, [1], strict=False), (BaseObject, 1))

  def test_join_words(self) -> None:
    """'joinWords' given such a class names it."""
    self.assertEqual(joinWords(BaseObject, 'int'), '%s and int' % BaseObject)

  def test_enumeration_flattened(self) -> None:
    """An enumeration iterates and is flattened as before."""
    self.assertEqual(unpack([Color]), (Color.RED, Color.BLUE))
    self.assertEqual(unpack(Color, shallow=True), (Color.RED, Color.BLUE))
