"""TestAttriBox tests the AttriBox implementation of the descriptor
protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import random
from time import time
from unittest import TestCase

from icecream import ic

from worktoy.desc import AttriBox, SCOPE
from worktoy.ezdata import EZData
from worktoy.parse import maybe

ic.configureOutput(includeContext=True)


class Point3D(EZData):
  """Space point"""

  x = AttriBox[int](-1)
  y = AttriBox[int](-1)
  z = AttriBox[int](-1)


class Float:
  """Float class"""
  __fallback_value__ = 69.
  __inner_value__ = None

  def __init__(self, *args, ) -> None:
    pass

  def __str__(self) -> str:
    """String representation"""
    return '%.3f' % float(self.__inner_value__)

  def __repr__(self, ) -> str:
    """Code representation"""
    return '%s(%.3f)' % (self.__class__.__name__, self.__inner_value__)

  def __float__(self) -> float:
    """Float representation"""
    return maybe(self.__inner_value__, self.__fallback_value__)


class ClassName:
  """ClassName class"""
  __fallback_name__ = 'LMAO'
  __inner_name__ = None

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, str):
        self.__inner_name__ = arg
        break
    else:
      self.__inner_name__ = self.__fallback_name__

  def __str__(self, ) -> str:
    """String representation"""
    return self.__inner_name__

  def __repr__(self, ) -> str:
    """Code representation"""
    return '%s(%s)' % (self.__class__.__name__, self.__inner_name__)


class Instance:
  """Class representing the instance of the class owning the descriptor
  class. """

  __owning_instance__ = None
  __owning_class__ = None

  def __init__(self, owningInstance: object) -> None:
    self.__owning_instance__ = owningInstance
    self.__owning_class__ = owningInstance.__class__

  def __str__(self) -> str:
    """String representation"""
    return '%s(%s)' % (self.__class__.__name__, self.__owning_instance__)


class BoxClass:
  """Box class"""

  label = AttriBox[ClassName](
      SCOPE >> (lambda cls: getattr(cls, '__name__')))


class TestAttriBox(TestCase):
  """TestAttriBox tests the AttriBox implementation of the descriptor
  protocol. """

  @classmethod
  def setUpClass(cls, ) -> None:
    """Set up the test class."""

  @classmethod
  def tearDownClass(cls, ) -> None:
    """Tear down the test class."""

  def setUp(self) -> None:
    """Set up the test."""
    self.box = BoxClass()
    self.point = Point3D(69, 420, 1337)

  def test_get_set(self, ) -> None:
    """Tests the creation of an instance of the Point3D class. """
    roll = Float(random())
    self.box.x = roll
    self.assertAlmostEqual(float(self.box.x), float(roll))

  def test_errors(self, ) -> None:
    """Tests the creation of an instance of the Point3D class. """
    with self.assertRaises(TypeError):
      self.point.x = .1337
    with self.assertRaises(TypeError):
      self.point.y = 69 + 420 * 1j
    with self.assertRaises(TypeError):
      self.point.z = '1337'

  def test_scope(self, ) -> None:
    """Tests the creation of an instance of the Point3D class. """
    self.assertEqual(str(self.box.label), self.box.__class__.__name__)
