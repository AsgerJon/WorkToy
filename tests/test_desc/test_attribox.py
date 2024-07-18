"""TestAttriBox tests the AttriBox implementation of the descriptor
protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import inspect
import os
from typing import Optional, TYPE_CHECKING

from worktoy.desc import AttriClass, AttriBox
from worktoy.ezdata import EZData, EndFields, BeginFields
from worktoy.parse import maybe
from worktoy.worktest import WorkTest


class Integer(AttriClass):
  """Integer is a descriptor for integer attributes."""

  __inner_value__ = None

  def __init__(self, *args, **kwargs) -> None:
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

  BeginFields
  x = AttriBox[Integer](-1)
  y = AttriBox[Integer](-1)
  z = AttriBox[Integer](-1)
  EndFields

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

  @classmethod
  def getStubFileName(cls) -> str:
    """Returns the name of the stub file. """
    return inspect.getfile(cls).replace('.py', '.pyi')

  @classmethod
  def clearStubFile(cls) -> None:
    """Removes the stub file. """
    stubFile = cls.getStubFileName()
    if os.path.exists(stubFile):
      os.remove(stubFile)
      print('Removed stub file: %s' % stubFile)

  @classmethod
  def setUpClass(cls, ) -> None:
    """Set up the test class."""

  @classmethod
  def tearDownClass(cls, ) -> None:
    """Tear down the test class."""
    cls.clearStubFile()

  def test_instance_peek(self, ) -> None:
    """Tests the creation of an instance of the Point3D class. """
    point = Point3D()
    values = point.getPrivateValues()
    self.assertIsNone(values['x'])
    self.assertIsNone(values['y'])
    self.assertIsNone(values['z'])
    if point.x:
      pass
    values = point.getPrivateValues()
    self.assertEqual(values['x'], -1)
    self.assertIsNone(values['y'])
    self.assertIsNone(values['z'])
    if point.y:
      pass
    values = point.getPrivateValues()
    self.assertEqual(values['x'], -1)
    self.assertEqual(values['y'], -1)
    self.assertIsNone(values['z'])
    if point.z:
      pass
    values = point.getPrivateValues()
    self.assertEqual(values['x'], -1)
    self.assertEqual(values['y'], -1)
    self.assertEqual(values['z'], -1)

  def test_stub_file(self, ) -> None:
    """Tests the creation of a stub file. """
    stubFile = self.getStubFileName()
    with open(stubFile, 'r') as f:
      lines = f.readlines()
    for line in lines:
      if ':' in line:
        varName, typeName = line.split(':')
        varName = varName.strip()
        typeName = typeName.strip()
        if varName and typeName:
          self.assertIsInstance(getattr(Point3D, varName), AttriBox)
          boxClass = AttriBox.getInnerClass(getattr(Point3D, varName))
          self.assertIs(boxClass, Integer)
