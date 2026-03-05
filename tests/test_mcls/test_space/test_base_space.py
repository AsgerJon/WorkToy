"""
TestBaseSpace tests the BaseSpace class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from .. import MCLSTest
from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class GrandParent(BaseObject):
  """Subclasses 'BaseObject', but is otherwise empty. """


class Parent(GrandParent):
  __bar_int__ = 'Parent.overload(int)'
  __bar_str__ = 'Parent.overload(str)'

  @overload(int)
  def bar(self, *args) -> Any:
    """bar method that takes an integer and returns its square."""
    return self.__bar_int__

  @overload(str)
  def bar(self, *args) -> Any:
    """bar method that takes a string and returns its length."""
    return self.__bar_str__


class Child(Parent):
  __bar_int_int__ = 'Child.overload(int, int)'
  __bar_int__ = 'Child.overload(int)'

  @overload(int, int)
  def bar(self, *args) -> Any:
    """bar method that takes two integers and returns their sum."""
    return self.__bar_int_int__

  @overload(int)
  def bar(self, *args) -> Any:
    """bar method that takes an integer and returns its square."""
    return self.__bar_int__


class TestBaseSpace(MCLSTest):
  """
  TestBaseSpace tests the BaseSpace class.
  """

  def test_overload(self, ) -> None:
    """Tests overload"""
    parent = Parent()
    self.assertEqual(parent.bar(69, ), parent.__bar_int__)
    self.assertEqual(parent.bar('foo'), parent.__bar_str__)
    child = Child()
    self.assertEqual(child.bar(69, ), child.__bar_int__)
    self.assertEqual(child.bar('foo'), child.__bar_str__)
    self.assertEqual(child.bar(69, 420), child.__bar_int_int__)
    self.assertEqual(Parent.__bar_str__, Child.__bar_str__)
