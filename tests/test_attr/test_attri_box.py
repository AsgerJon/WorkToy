"""
TestAttriBox tests the AttriBox class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from tests import WYD

from unittest import TestCase

from worktoy.attr import AttriBox
from worktoy.static.zeroton import THIS, OWNER, DELETED
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute import VariableNotNone
from . import PlanePoint, PlaneCircle

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class Yikes(Exception):
  pass


class Foo:
  """
  Foo is a class
  """

  __wrapped__ = None

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    self.__wrapped__ = args[0]
    if isinstance(args[0], complex):
      raise Yikes


class Bar:
  """
  Bar accepts 'Foo' objects in its constructor
  """

  ham = AttriBox[Foo](OWNER)
  eggs = AttriBox[Foo](THIS)


class TestAttriBox(TestCase):
  """TestAttriBox tests the AttriBox class."""

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def setUp(self) -> None:
    """Set up the test case."""
    self.point1 = PlanePoint(.80085, .1337)
    self.point2 = PlanePoint(69, 420)
    self.point3 = PlanePoint(1337 + 80085j)
    self.circle1 = PlaneCircle(self.point1, 69.0)
    self.circle2 = PlaneCircle(self.point2, 420)

  def test_boxes(self, ) -> None:
    """Test the AttriBox class."""
    self.assertIsInstance(PlanePoint.x, AttriBox)
    self.assertIsInstance(PlanePoint.y, AttriBox)
    self.assertIsInstance(PlaneCircle.center, AttriBox)
    self.assertIsInstance(PlaneCircle.radius, AttriBox)

  def test_init(self, ) -> None:
    """Test the AttriBox class initialization."""
    self.assertIsInstance(self.point1, PlanePoint)
    self.assertIsInstance(self.point2, PlanePoint)
    self.assertIsInstance(self.point3, PlanePoint)
    self.assertIsInstance(self.circle1, PlaneCircle)
    self.assertIsInstance(self.circle2, PlaneCircle)

  def test_good_get(self, ) -> None:
    """Test getting values. """
    self.assertEqual(self.point1.x, .80085)
    self.assertEqual(self.point1.y, .1337)
    self.assertEqual(self.point2.x, 69)
    self.assertEqual(self.point2.y, 420)
    self.assertEqual(self.point3.x, 1337)
    self.assertEqual(self.point3.y, 80085)
    self.assertEqual(self.circle1.center.x, .80085)
    self.assertEqual(self.circle1.center.y, .1337)
    self.assertEqual(self.circle1.radius, 69.0)
    self.assertEqual(self.circle2.center.x, 69)
    self.assertEqual(self.circle2.center.y, 420)
    self.assertEqual(self.circle2.radius, 420)

  def test_good_set(self, ) -> None:
    """Test setting values."""
    self.assertEqual(self.point1.x, .80085)
    self.assertEqual(self.point1.y, .1337)
    self.point1.x = 69.
    self.point1.y = 420
    self.assertEqual(self.point1.x, 69.)
    self.assertEqual(self.point1.y, 420)

    self.assertEqual(self.point2.x, 69.)
    self.assertEqual(self.point2.y, 420.)
    self.point2.x = 1337
    self.point2.y = 80085
    self.assertEqual(self.point2.x, 1337)
    self.assertEqual(self.point2.y, 80085)

    self.assertEqual(self.point3.x, 1337)
    self.assertEqual(self.point3.y, 80085)
    self.point3.x = 0.80085
    self.point3.y = 0.1337
    self.assertEqual(self.point3.x, 0.80085)
    self.assertEqual(self.point3.y, 0.1337)

    self.assertEqual(self.circle1.center.x, self.point1.x)
    self.assertEqual(self.circle1.center.y, self.point1.y)
    self.assertEqual(self.circle1.radius, 69.0)
    self.circle1.center = self.point2
    self.circle1.radius = 420
    self.assertEqual(self.circle1.center.x, self.point2.x)
    self.assertEqual(self.circle1.center.y, self.point2.y)
    self.assertEqual(self.circle1.radius, 420)

    self.assertEqual(self.circle2.center.x, self.point2.x)
    self.assertEqual(self.circle2.center.y, self.point2.y)
    self.assertEqual(self.circle2.radius, 420)
    self.circle2.center = self.point3
    self.circle2.radius = 69.0
    self.assertEqual(self.circle2.center.x, self.point3.x)
    self.assertEqual(self.circle2.center.y, self.point3.y)
    self.assertEqual(self.circle2.radius, 69.0)

  def test_get_missing_field_type(self) -> None:
    """
    Test retrieving field type from AttriBox object not having one set.
    """
    box = AttriBox()  # Missing field type
    with self.assertRaises(MissingVariable) as context:
      box.getFieldType()
    exception = context.exception
    self.assertIs(exception.varType[0], type)
    self.assertEqual(exception.varName, 'AttriBox.__field_type__')

  def test_get_wrong_field_type(self) -> None:
    """
    Test retrieving field type from AttriBox object having wrong type set.
    """
    susType = 'imma type, trust!'
    box = AttriBox()
    setattr(box, '__field_type__', susType)  # Set wrong type
    with self.assertRaises(TypeException) as context:
      box.getFieldType()
    exception = context.exception
    self.assertEqual(exception.varName, '__field_type__')
    self.assertEqual(exception.actualObject, susType)
    self.assertIs(exception.expectedType[0], type)
    self.assertIs(exception.actualType, str)

  def test_set_wrong_field_type(self) -> None:
    """
    Test setting field type on AttriBox object with wrong type.
    """
    box = AttriBox()
    susType = 'imma type, trust!'
    with self.assertRaises(TypeException) as context:
      box.setFieldType(susType)
    exception = context.exception
    self.assertEqual(exception.varName, 'fieldType')
    self.assertEqual(exception.actualObject, susType)
    self.assertIs(exception.expectedType[0], type)

  def test_set_duplicate_field_type(self) -> None:
    """
    Test setting field type on AttriBox object that already has one set.
    """
    box = AttriBox(int)
    with self.assertRaises(VariableNotNone) as context:
      box.setFieldType(float)
    exception = context.exception
    self.assertEqual(exception.name, 'AttriBox.__field_type__')
    self.assertIs(exception.value, int)

  def test_instantiate_box_field_type(self) -> None:
    """
    Test instantiating AttriBox with field type.
    """
    bar = Bar()
    setattr(bar, Bar.ham.getPrivateName(), None)
    self.assertIsInstance(bar.ham, Foo)
    self.assertIs(bar.ham.__wrapped__, Bar)
    self.assertIsInstance(bar.eggs, Foo)
    self.assertIs(bar.eggs.__wrapped__, bar)

  def test_bad_set(self) -> None:
    """
    Tests bad setting of AttriBox
    """
    bar = Bar()
    with self.assertRaises(TypeException) as context:
      bar.ham = 69 + 420j
    exception = context.exception
    self.assertIsInstance(exception, TypeException)
    self.assertIsInstance(exception.__cause__, Yikes)

  def test_bad_delete(self) -> None:
    """
    Tests bad deletion of AttriBox
    """
    bar = Bar()
    del bar.ham
    self.assertIs(getattr(bar, Bar.ham.getPrivateName(), ), DELETED)
