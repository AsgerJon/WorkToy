"""
TestEZSpace tests the EZSpace class from the ezdata module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import DataField, EZData, EZMeta

from typing import TYPE_CHECKING

from worktoy.text import stringList, monoSpace
from worktoy.waitaminute import TypeException, ReservedName

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class TestEZSpace(TestCase):
  """
  TestEZSpace tests the EZSpace class from the ezdata module. As EZSpace
  is part of the custom metaclass creation flow used by the EZData module,
  these tests will create various EZData subclasses.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_good_class(self) -> None:
    """
    Tests a good data class
    """

    class Plane(EZData):
      """
      A simple data class representing a plane.
      """

      x = 0.0
      y = 0.0

      def __abs__(self, ) -> float:
        """
        Returns the absolute value of the plane's coordinates.
        """
        return (self.x ** 2 + self.y ** 2) ** 0.5

    point1 = Plane(69, 420)
    self.assertEqual(point1.x, 69)
    self.assertEqual(point1.y, 420)
    point2 = Plane(69, 420)
    self.assertEqual(point1, point2)
    self.assertFalse(abs(point1) - 69 * 69 - 420 * 420 > 1e-6)
    self.assertEqual(len(point1), 2)

  def test_bad_class(self) -> None:
    """
    Tests a bad data class. For example on the implements __init__ in the
    class body.
    """

    with self.assertRaises(ReservedName) as context:
      class BadPlane(EZData):
        """
        A bad data class representing a plane.
        """

        x = 0.0
        y = 0.0

        def __init__(self, x: float, y: float) -> None:
          """
          Initializes the plane with coordinates.
          """
    e = context.exception
    self.assertEqual(e.resName, '__init__')

  def test_deviant_class(self) -> None:
    """
    Tests a deviant class that uses the '__is_root__' attribute to
    deviate from the standard EZData class creation flow.
    """

    def trustMeBro(callMeMaybe: Any) -> Any:
      """
      This is a decorator that can be used to mark a function as a root
      function in the EZData class.
      """
      callMeMaybe.__is_root__ = True
      return callMeMaybe

    class Sus(EZData):
      """
      A deviant data class that uses the '__is_root__' attribute to
      deviate from the standard EZData class creation flow.
      """

      x = 0.0
      y = 0.0

      @trustMeBro
      def __init__(self, *args) -> None:
        """
        Initializes the deviant data class with coordinates.
        """

    sus = Sus(69, 420)  # Does not actually use __init__ above.
    self.assertEqual(sus.x, 69)
    self.assertEqual(sus.y, 420)

  def test_str_repr(self) -> None:
    """
    Test the output of EZData.__str__ and __repr__.
    """

    class Point(EZData):
      """
      A simple data class representing a point in 2D space.
      """

      x = 0.0
      y = 0.0

    point = Point(69, 420)
    words = stringList("""Point, x=69, y=420""")
    for word in words:
      self.assertIn(word, str(point))
    words = stringList("""Point, 69, 420""")
    for word in words:
      self.assertIn(word, repr(point))

  def test_iter(self) -> None:
    """
    Test the iteration over EZData instances.
    """

    class Point(EZData):
      """
      A simple data class representing a point in 2D space.
      """

      x = 0.0
      y = 0.0

    point = Point(69, 420)
    self.assertEqual(list(point), [69, 420])
    self.assertEqual(len(point), 2)

  def test_eq(self) -> None:
    """
    Test the equality of EZData instances.
    """

    class Point(EZData):
      """
      A simple data class representing a point in 2D space.
      """

      x = 0.0
      y = 0.0

    point1 = Point(69, 420)
    point2 = Point(69, 420)
    point3 = Point(70, 420)
    self.assertEqual(point1, point2)
    self.assertNotEqual(point1, point3)
    self.assertNotEqual(point2, point3)
    testValue = Point.__eq__(point1, 'lmao')
    self.assertIs(testValue, NotImplemented)

  def test_hash(self) -> None:
    """
    Test that EZData instances can be dictionary keys.
    """

    class Point(EZData):
      """
      A simple data class representing a point in 2D space.
      """

      x = 0.0
      y = 0.0

    point1 = Point(69, 420)
    point2 = Point(69, 420)
    point3 = Point(70, 420)
    self.assertEqual(hash(point1), hash(point2))

    # Test that EZData instances can be dictionary keys
    testDict: dict[Point, str] = {point1: 'test'}
    self.assertIn(point1, testDict)
    self.assertIn(point2, testDict)
    self.assertNotIn(point3, testDict)

  def test_dict_like(self) -> None:
    """
    Test that EZData classes support the dict-like syntax:
    point = Point(69, 420)
    point['x'] = 69
    point['y'] = 420
    """

    class Point(EZData):
      """
      A simple data class representing a point in 2D space.
      """

      x = 0.0
      y = 0.0

    point = Point(69, 420)
    self.assertEqual(point['x'], 69)
    self.assertEqual(point['y'], 420)
    point['x'] = 1337
    point['y'] = 80085
    self.assertEqual(point.x, 1337)
    self.assertEqual(point.y, 80085)

    with self.assertRaises(KeyError) as context:
      _ = point['z']
    e = context.exception
    self.assertEqual(str(e), "'z'")

    with self.assertRaises(KeyError) as context:
      point['z'] = 1337
    e = context.exception
    self.assertEqual(str(e), "'z'")

  def test_dot(self, ) -> None:
    """
    Test that EZData classes support the dot syntax:
    point = Point(69, 420)
    point.x = 69
    point.y = 420
    """

    class Point(EZData):
      """
      A simple data class representing a point in 2D space.
      """

      x = 0.0
      y = 0.0

    point = Point(69, 420)
    self.assertEqual(point.x, 69)
    self.assertEqual(point.y, 420)
    point.x = 1337
    point.y = 80085
    self.assertEqual(point.x, 1337)
    self.assertEqual(point.y, 80085)
