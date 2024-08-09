"""TestSingleton tests the Singleton class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.meta import Singleton


class Unique(Singleton):
  """Unique class used to test Singleton"""

  x = AttriBox[float](0.0)
  y = AttriBox[float](0.0)

  name = AttriBox[str]('')

  def __init__(self, *args) -> None:
    """Initializes the Unique class"""
    self.name = args[0] if args else self.name
    self.x = args[1] if len(args) > 1 else self.x
    self.y = args[2] if len(args) > 2 else self.y

  def __str__(self) -> str:
    """String representation"""
    return self.name


class TestSingleton(TestCase):
  """TestSingleton tests the Singleton class. """

  def setUp(self) -> None:
    """Sets up each test method."""

  def testSingleness(self) -> None:
    """Test if the Singleton is truly a Singleton. """
    a = Unique()
    b = Unique()
    self.assertIs(a, b)

  def testUpdate(self) -> None:
    """The Singleton should update the value of the attributes at each
    call to the class"""
    a = Unique('lol', 0, 0, )
    self.assertEqual(a.name, 'lol')
    self.assertEqual(a.x, 0.0)
    self.assertEqual(a.y, 0.0)
    b = Unique('lmao', 69, 420, )
    self.assertIs(a, b)
    self.assertEqual(a.name, 'lmao')
    self.assertEqual(a.x, 69.0)
    self.assertEqual(a.y, 420.0)
