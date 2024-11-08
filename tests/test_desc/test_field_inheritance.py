"""TestFieldInheritance tests that subclassing a Field owner allows the
subclass to change the Field accessor behaviour by reimplementing the
decorated methods in the parent class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import Field
from worktoy.parse import maybe


class Parent:
  """Parent class"""

  __fallback_name__ = 'Unnamed'
  __instance_name__ = None

  name = Field(_root=True)

  @name.GET
  def _getName(self) -> str:
    """Get the name."""
    instanceName = maybe(self.__instance_name__, self.__fallback_name__)
    return 'Parent: %s' % instanceName

  @name.SET
  def _setName(self, name: str) -> None:
    """Set the name."""
    self.__instance_name__ = name

  def __init__(self, name: str) -> None:
    """Constructor for the Parent class."""
    self.name = name


class Child(Parent):
  """Child class"""

  def _getName(self, ) -> str:
    """Get the name."""
    instanceName = maybe(self.__instance_name__, self.__fallback_name__)
    return 'Child: %s' % instanceName


class TestFieldInheritance(TestCase):
  """TestFieldInheritance tests that subclassing a Field owner allows the
  subclass to change the Field accessor behaviour by reimplementing the
  decorated methods in the parent class. """

  def setUp(self, ) -> None:
    """Set up the test case."""
    self.parent = Parent('Alice')
    self.child = Child('Bob')

  def test_parent(self, ) -> None:
    """Test the parent class."""
    self.assertEqual(self.parent.name, 'Parent: Alice')
    self.parent.name = 'Charlie'
    self.assertEqual(self.parent.name, 'Parent: Charlie')

  def test_child(self, ) -> None:
    """Test the child class."""
    self.assertEqual(self.child.name, 'Child: Bob')
    self.child.name = 'David'
    self.assertEqual(self.child.name, 'Child: David')
