"""
TestHookMethodKinds subclasses 'DescTest' and pins that a notification
callback a subclass redefines as a classmethod still fires. The hooks
look each callback up by name on the class of the instance and hand it
to 'flexCall', which takes a plain function only, so the bound method a
classmethod gives used to be refused with 'TypeException' on every
access. The hooks now unwrap the function behind a bound method, as
'hookSetName' has always done.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject

from . import DescTest


class Parent(BaseObject):
  """Parent declares the callbacks as plain methods."""

  x = AttriBox[int](0)
  seen = None

  @x.preGet
  def _preGet(self) -> None:
    type(self).seen = ('preGet', self)

  @x.onSet
  def _onSet(self, value: int) -> None:
    type(self).seen = ('onSet', value)


class ClassMethodChild(Parent):
  """ClassMethodChild redefines the callbacks as classmethods."""

  @classmethod
  def _preGet(cls, *args) -> None:
    ClassMethodChild.seen = ('cls preGet', type(cls).__name__, args)

  @classmethod
  def _onSet(cls, *args) -> None:
    ClassMethodChild.seen = ('cls onSet', type(cls).__name__, args)


class TestHookMethodKinds(DescTest):
  """
  TestHookMethodKinds provides tests for callbacks redefined as
  classmethods.
  """

  def test_plain_methods(self) -> None:
    """The plain methods of the parent fire with the instance."""
    parent = Parent()
    parent.x = 3
    self.assertEqual(Parent.seen, ('onSet', 3))
    _ = parent.x
    self.assertEqual(Parent.seen, ('preGet', parent))

  def test_classmethod_override_fires(self) -> None:
    """A classmethod override fires. The function behind the bound method
    is called as the plain method would be, so the instance lands in its
    first parameter and the value follows."""
    child = ClassMethodChild()
    child.x = 4
    expected = ('cls onSet', 'ClassMethodChild', (4,))
    self.assertEqual(ClassMethodChild.seen, expected)
    _ = child.x
    expected = ('cls preGet', 'ClassMethodChild', ())
    self.assertEqual(ClassMethodChild.seen, expected)
