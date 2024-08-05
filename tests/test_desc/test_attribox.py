"""TestAttriBox tests the AttriBox implementation of the descriptor
protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from random import random
from typing import Any
from unittest import TestCase

from icecream import ic

from worktoy.desc import AttriBox, TYPE, THIS, Field, ATTR, BOX
from worktoy.ezdata import EZData
from worktoy.meta import BaseObject, overload
from worktoy.parse import maybe
from worktoy.text import typeMsg

ic.configureOutput(includeContext=True)


class NoDefaults(BaseObject):
  """NoDefaults class"""
  attrStr = AttriBox[str]()
  attrFloat = AttriBox[float]()
  attrInt = AttriBox[int]()
  attrBool = AttriBox[bool]()
  attrList = AttriBox[list]()
  attrDict = AttriBox[dict]()


class SomeDefaults(BaseObject):
  """SomeDefaults class"""
  attrStr = AttriBox[str]('LMAO')
  attrFloat = AttriBox[float](69.)
  attrInt = AttriBox[int](69)
  attrBool = AttriBox[bool](True)
  attrList = AttriBox[list]([1, 2, 3])
  attrDict = AttriBox[dict]({'a': 1, 'b': 2, 'c': 3})


class Point(BaseObject):
  """Float point class"""

  x = AttriBox[float]()
  y = AttriBox[float]()

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y

  def __str__(self) -> str:
    """String representation"""
    return """%.3f, %.3f""" % (self.x, self.y)


class Point3D(Point):  #
  """Subclass of Point, testing AttriBox inheritance"""


class Aware(BaseObject):
  """Class aware of owning class and owning instance"""

  __field_owner__ = None
  __field_instance__ = None

  owner = Field()
  instance = Field()

  @overload(type, object)
  def __init__(self, cls: type, this: object, ) -> None:
    if not isinstance(this, cls):
      e = typeMsg('this', this, cls)
      raise TypeError(e)
    self.owner = cls
    self.instance = this

  @overload(object, type)
  def __init__(self, this: object, cls: type, ) -> None:
    self.__init__(cls, this, )

  @owner.GET
  def _getOwner(self) -> type:
    """Getter-function for owner"""
    return self.__field_owner__

  @owner.SET
  def _setOwner(self, owner: type) -> None:
    """Setter-function for owner"""
    self.__field_owner__ = owner

  @instance.GET
  def _getInstance(self) -> object:
    """Getter-function for instance"""
    return self.__field_instance__

  @instance.SET
  def _setInstance(self, instance: object) -> None:
    """Setter-function for instance"""
    self.__field_instance__ = instance


class MyStuff(BaseObject):
  """Owner of aware attributes"""

  whoDat = AttriBox[Aware](TYPE, THIS, )
  meLOL = AttriBox[Aware](ATTR, BOX)


class TestAttriBox(TestCase):
  """TestAttriBox tests the AttriBox implementation of the descriptor
  protocol. """

  def setUp(self, ) -> None:
    """Set up the test class."""
    self.x = random()
    self.y = random()
    self.point = Point(self.x, self.y, )

  def test_inheritance(self) -> None:
    """Testing if AttriBox instances are inherited correctly."""
    point3D = Point3D(69., 420.)
    self.assertTrue(isinstance(point3D, Point))
    self.assertTrue(isinstance(point3D, Point3D))

  def test_reset(self, ) -> None:
    """Testing if AttriBox instances can be reset."""
    testValues = SomeDefaults()
    testValues.attrStr = '%s | bla' % testValues.attrStr
    oldStr = '%s' % testValues.attrStr
    SomeDefaults.attrStr.reset(testValues)
    newStr = '%s' % testValues.attrStr
    self.assertNotEqual(oldStr, newStr)

  def test_zeroton(self, ) -> None:
    """Test if the special Zeroton classes THIS and TYPE are working
    correctly."""
    myStuff = MyStuff()
    self.assertEqual(myStuff.whoDat.owner, MyStuff)
    self.assertEqual(myStuff.whoDat.instance, myStuff)
    self.assertEqual(myStuff.meLOL.owner, AttriBox)
    self.assertEqual(myStuff.meLOL.instance, MyStuff.meLOL)

  def test_no_default(self) -> None:
    """Tests that the box instance correctly defaults to False values."""
    noDefaults = NoDefaults()
    self.assertFalse(noDefaults.attrStr)
    self.assertFalse(noDefaults.attrFloat)
    self.assertFalse(noDefaults.attrInt)
    self.assertFalse(noDefaults.attrBool)
    self.assertFalse(noDefaults.attrList)
    self.assertFalse(noDefaults.attrDict)

  def test_default(self) -> None:
    """Tests that the box instance correctly retrieves default values."""
    someDefaults = SomeDefaults()
    self.assertEqual(someDefaults.attrStr, 'LMAO')
    self.assertEqual(someDefaults.attrFloat, 69.)
    self.assertEqual(someDefaults.attrInt, 69)
    self.assertTrue(someDefaults.attrBool)
    self.assertEqual(someDefaults.attrList, [1, 2, 3])
    self.assertEqual(someDefaults.attrDict, {'a': 1, 'b': 2, 'c': 3})

  def test_get(self) -> None:
    """Test the get-method of the AttriBox class. """
    self.assertEqual(self.point.x, self.x)
    self.assertEqual(self.point.y, self.y)

  def test_set(self) -> None:
    """Test the set-method of the AttriBox class. """
    x = random() + 1
    y = random() + 1
    self.point.x = x
    self.point.y = y
    self.assertEqual(self.point.x, x)
    self.assertEqual(self.point.y, y)
