"""
TestNoPickleMangledSlots subclasses 'UtilitiesTest' and pins that the
copies 'NoPickle' makes keep a slot declared with a private name, such
as '__secret'. Python stores such a slot under its mangled name,
'_Slotted__secret', and the copy looked it up under the name as
declared, which no instance holds, so the copy lost it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from copy import copy, deepcopy

from worktoy.utilities import NoPickle

from . import UtilitiesTest


class Slotted(NoPickle):
  """Slotted declares a private slot and a public one."""

  __slots__ = ('__secret', 'public')

  def __init__(self, secret: list, public: int) -> None:
    self.__secret = secret
    self.public = public

  def peek(self) -> list:
    return self.__secret


class _Underscored(NoPickle):
  """_Underscored has a name starting with an underscore, which the
  mangling drops."""

  __slots__ = ('__secret',)

  def __init__(self) -> None:
    self.__secret = 'kept'

  def peek(self) -> str:
    return self.__secret


class TestNoPickleMangledSlots(UtilitiesTest):
  """
  TestNoPickleMangledSlots provides tests for copying private slots.
  """

  def test_copy_keeps_private_slot(self) -> None:
    """A shallow copy keeps the private slot, sharing its value."""
    secret = [1, 2]
    copied = copy(Slotted(secret, 3))
    self.assertIs(copied.peek(), secret)
    self.assertEqual(copied.public, 3)

  def test_deepcopy_keeps_private_slot(self) -> None:
    """A deep copy keeps the private slot, copying its value."""
    secret = [1, 2]
    copied = deepcopy(Slotted(secret, 3))
    self.assertEqual(copied.peek(), secret)
    self.assertIsNot(copied.peek(), secret)

  def test_underscored_class(self) -> None:
    """A class named with a leading underscore mangles without it."""
    self.assertEqual(copy(_Underscored()).peek(), 'kept')
