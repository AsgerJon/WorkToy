"""
TestSuperOverload subclasses 'OverloadTest' and pins that an overloaded
method may delegate to the overloaded method it overrides through
'super'. The subclass and the parent each own a 'Dispatcher' under the
same name, and reaching the parent through 'super' must run the parent's
function rather than coming back around to the subclass. Reaching the
parent first must likewise leave the subclass override in place for
every later call.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from . import OverloadTest


class Parent(BaseObject):
  """Parent declares the overloaded 'describe' that the subclasses below
  override and reach back into through 'super'."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def describe(self, n: int) -> str:
    return 'parent %d' % n


class Child(Parent):
  """Child overrides 'describe' under the same signature and wraps the
  text returned by the parent version."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def describe(self, n: int) -> str:
    return 'child > %s' % super().describe(n)


class GrandChild(Child):
  """GrandChild adds a third link to the chain, so a single call passes
  through three dispatchers sharing the name 'describe'."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def describe(self, n: int) -> str:
    return 'grandchild > %s' % super().describe(n)


class Shape(BaseObject):
  """Shape has an overloaded constructor recording the number of sides.
  Python looks up '__init__' through the instance during construction,
  which makes the constructor the most common place for an overloaded
  override to delegate through 'super'."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  sides = AttriBox[int](0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def __init__(self, sides: int) -> None:
    self.sides = sides


class Polygon(Shape):
  """Polygon overrides the overloaded constructor of 'Shape', hands the
  side count on to it through 'super', and then sets its own label."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  label = AttriBox[str]('')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def __init__(self, sides: int) -> None:
    super().__init__(sides)
    self.label = 'polygon'


class TestSuperOverload(OverloadTest):
  """
  TestSuperOverload pins that 'super' inside an overloaded override
  reaches the parent's overloaded function, at every depth and in the
  constructor, and that doing so leaves the override intact.
  """

  def test_super_in_overloaded_method(self) -> None:
    """
    Testing that the override reaches the parent version through
    'super' exactly once. A dispatcher that hands the parent's lookup
    back to the subclass loops until the interpreter raises
    'RecursionError'.
    """
    self.assertEqual(Parent().describe(1), 'parent 1')
    self.assertEqual(Child().describe(1), 'child > parent 1')

  def test_super_through_three_levels(self) -> None:
    """
    Testing that each link in a chain of three overrides reaches the
    next one up, so the call visits every level once, from the
    grandchild up to the parent.
    """
    expected = 'grandchild > child > parent 2'
    self.assertEqual(GrandChild().describe(2), expected)

  def test_super_in_overloaded_constructor(self) -> None:
    """
    Testing that an overloaded constructor may delegate to the
    overloaded constructor it overrides. Both the side count stored by
    the parent and the label set by the subclass must be present
    afterwards.
    """
    polygon = Polygon(5)
    self.assertEqual(polygon.sides, 5)
    self.assertEqual(polygon.label, 'polygon')

  def test_parent_access_keeps_override(self) -> None:
    """
    Testing that reaching the parent version through 'super' from
    outside the class does not replace the override on that instance.
    The parent call must return the parent text, and a later ordinary
    call must still reach the override.
    """
    child = Child()
    self.assertEqual(super(Child, child).describe(3), 'parent 3')
    self.assertEqual(child.describe(3), 'child > parent 3')
