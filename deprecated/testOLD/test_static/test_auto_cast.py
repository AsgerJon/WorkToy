"""TestAutoCast tests the auto casting system. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from worktoy.static.casting import FloatCast, ComplexCast
from worktoy.static.casting import IntCast, AutoCast, Cast


class SomeClass:
  """Some class to test the auto casting system."""

  __pos_args__ = None
  __key_args__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the class."""
    self.__pos_args__ = args
    self.__key_args__ = kwargs


class ChildA(SomeClass):
  """Child class A to test the auto casting system."""
  pass


class ChildB(SomeClass):
  """Child class B to test the auto casting system."""
  pass


class TestAutoCast(TestCase):
  """Test the auto casting system."""

  def setUp(self) -> None:
    """Sets up cast objects for testing."""
    self.castA = AutoCast(ChildA)
    self.castB = AutoCast(ChildB)

  def test_cast(self, ) -> None:
    """Testing the auto casting system."""
    # Test the auto casting system
    self.assertIsInstance(self.castA, AutoCast)
    self.assertIsInstance(self.castB, AutoCast)
    a = self.castA(69, 420)
    b = self.castB(69, 420)
    self.assertIsInstance(a, ChildA)
    self.assertIsInstance(b, ChildB)
