"""TestAttriBox tests the AttriBox implementation of the descriptor
protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from worktoy.desc import AttriClass, AttriBox
from worktoy.ezdata import EZData
from worktoy.parse import maybe
from worktoy.worktest import WorkTest


class Integer(AttriClass):
  """Integer is a descriptor for integer attributes."""

  __inner_value__ = None

  def __init__(self, *args, **kwargs) -> None:
    print('Creating Integer')
    for arg in args:
      if isinstance(arg, int):
        self.__inner_value__ = arg
        break
    AttriClass.__init__(self, )

  def __eq__(self, other: object) -> bool:
    """Equality test for two integers"""
    if isinstance(other, Integer):
      return self.__inner_value__ == other.__inner_value__
    if isinstance(other, int):
      return self.__inner_value__ == other
    return NotImplemented


class Point3D(EZData):
  """Space point"""

  x = AttriBox[Integer](-1)
  y = AttriBox[Integer](-1)
  z = AttriBox[Integer](-1)

  def getPrivateNames(self) -> dict[str, str]:
    """Getter for the names of the private variables. """
    cls = self.__class__
    if TYPE_CHECKING:
      assert isinstance(cls.x, AttriBox)
      assert isinstance(cls.y, AttriBox)
      assert isinstance(cls.z, AttriBox)
    xName = cls.x._getPrivateName()
    yName = cls.y._getPrivateName()
    zName = cls.z._getPrivateName()
    return dict(x=xName, y=yName, z=zName)

  def getPrivateValues(self) -> dict[str, Optional[Integer]]:
    """Getter-function for the private values."""
    names = self.getPrivateNames()
    x = getattr(self, names['x'], None)
    y = getattr(self, names['y'], None)
    z = getattr(self, names['z'], None)
    return dict(x=x, y=y, z=z)

  def peek(self) -> str:
    """Peeks at the private values"""
    values = self.getPrivateValues()
    x = str(maybe(values['x'], 'None'))
    y = str(maybe(values['y'], 'None'))
    z = str(maybe(values['z'], 'None'))
    return 'peek: x=%s, y=%s, z=%s' % (x, y, z)

  def __str__(self) -> str:
    """String representation"""
    if TYPE_CHECKING:
      assert isinstance(self.x, int)
      assert isinstance(self.y, int)
      assert isinstance(self.z, int)
    return """(%d, %d, %d)""" % (self.x, self.y, self.z)

  def __setattr__(self, key, value) -> None:
    """Replaces instances of int with Integer."""
    object.__setattr__(self, key, value)


class TestAttriBox(WorkTest):
  """TestAttriBox tests the AttriBox implementation of the descriptor
  protocol. """

  def test_instance_peek(self, ) -> None:
    """Tests the creation of an instance of the Point3D class. """
    point = Point3D()
    values = point.getPrivateValues()
    self.assertIsNone(values['x'])
    self.assertIsNone(values['y'])
    self.assertIsNone(values['z'])
    print(point.x)
    values = point.getPrivateValues()
    self.assertEqual(values['x'], -1)
    self.assertIsNone(values['y'])
    self.assertIsNone(values['z'])
    print(point.y)
    values = point.getPrivateValues()
    self.assertEqual(values['x'], -1)
    self.assertEqual(values['y'], -1)
    self.assertIsNone(values['z'])
    print(point.z)
    values = point.getPrivateValues()
    self.assertEqual(values['x'], -1)
    self.assertEqual(values['y'], -1)
    self.assertEqual(values['z'], -1)
