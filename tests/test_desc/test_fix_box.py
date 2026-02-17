"""
TestFixBox provides unit tests specifically for the `FixBox` descriptor.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import FixBox
from worktoy.utilities.mathematics import pi
from worktoy.waitaminute import WriteOnceError
from worktoy.waitaminute.desc import ProtectedError
from . import DescTest, ComplexFix
from .geometry import Point2DFix, CircleFix

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestFixBox(DescTest):
  """
  TestFixBox provides unit tests specifically for the `FixBox`
  descriptor.
  """

  def test_init(self) -> None:
    """
    Testing that 'FixBox' descriptors actively instantiate when owning
    classes instantiate.
    """
    points = [
      Point2DFix(69., 420.),
      Point2DFix(),
      ]
    points.extend(Point2DFix.rands(69, -0.1337, 80085))
    point = Point2DFix(points.pop())
    points.append(point)
    for point in points:
      self.assertIsInstance(point.x, float)
      self.assertIsInstance(point.y, float)
      self.assertIs(Point2DFix.__add__(point, 'breh'), NotImplemented)
      self.assertIs(Point2DFix.__sub__(point, 'breh'), NotImplemented)
      self.assertIs(Point2DFix.__eq__(point, 'breh'), NotImplemented)
      z = complex(point)
      self.assertAlmostEqual(z.real, point.x)
      self.assertAlmostEqual(z.imag, point.y)
      pointStr = str(point)
      xStr = '%.3f' % point.x
      yStr = '%.3f' % point.y
      clsName = type(point).__name__
      expectedStr = """<%s: x=%s, y=%s>""" % (clsName, xStr, yStr)
      self.assertEqual(pointStr, expectedStr)
      expectedRepr = """%s(%s, %s)""" % (clsName, xStr, yStr)
      self.assertEqual(repr(point), expectedRepr)
      self.assertFalse(point.distance(point))
      incremented = point + 69.
      decremented = incremented - 69.
      self.assertAlmostEqual(decremented.x, point.x)
      self.assertAlmostEqual(decremented.y, point.y)
    circles = [
      CircleFix(point, 1337),
      CircleFix(point.x, point.y, 1337),
      CircleFix(point),
      CircleFix(point.x, point.y),
      CircleFix(1337.),
      ]
    expectedStrSpec = """<%s: (x-%s) ** 2 + (y-%s) ** 2 = %s ** 2>"""
    expectedReprSpec = """%s(%s, %s)"""
    circles.extend(CircleFix.rands(69, -0.1337, 80085))
    for circle in circles:
      self.assertIsInstance(circle.radius, float)
      self.assertIsInstance(circle.center, Point2DFix)
      x0Str = '%.3f' % circle.center.x
      y0Str = '%.3f' % circle.center.y
      rStr = '%.3f' % circle.radius
      centerRepr = repr(circle.center)
      clsName = type(circle).__name__
      expectedStr = expectedStrSpec % (clsName, x0Str, y0Str, rStr)
      self.assertEqual(str(circle), expectedStr)
      expectedRepr = expectedReprSpec % (clsName, centerRepr, rStr)
      self.assertEqual(repr(circle), expectedRepr)
      self.assertAlmostEqual(circle.area, pi * circle.radius ** 2)
      self.assertFalse('breh' in circle)
    unitCircle = CircleFix(Point2DFix(0, 0, ), 1)
    for args in self.randFloatTuples(420, 2, 0, 4 / pi):
      point = Point2DFix(*args)
      if abs(point) < 1:
        self.assertIn(point, unitCircle)
      else:
        self.assertFalse(point in unitCircle)
    complexNumbers = [
      ComplexFix(69, 420),
      ComplexFix(1337 + 80085j),
      ComplexFix(),
      ComplexFix(real=1337, imag=80085),
      ]
    complexNumbers.extend(ComplexFix.rands(69, -0.1337, 80085))
    for complexNumber in complexNumbers:
      self.assertIsInstance(complexNumber.RE, float)
      self.assertIsInstance(complexNumber.IM, float)

  def test_good_set(self, ) -> None:
    """
    Testing setting functions as intended.
    """
    point2D = Point2DFix()
    point2D.x = 1337
    point2D.y = 80085
    self.assertEqual(point2D.x, 1337)
    self.assertEqual(point2D.y, 80085)
    circle = CircleFix()
    circle.center = point2D
    circle.radius = .8008135
    self.assertAlmostEqual(circle.center, point2D)
    self.assertAlmostEqual(circle.radius, .8008135)
    self.assertAlmostEqual(circle.area / pi, .8008135 ** 2)
    z = ComplexFix()
    z.RE = 69
    z.IM = 420
    self.assertEqual(z.RE, 69)
    self.assertEqual(z.IM, 420)
    self.assertAlmostEqual(z.ABS * z.ABS, (z * (+z)).RE)

  def test_bad_set(self, ) -> None:
    """
    Testing that setting requires that the attribute is not already set.
    If a getter is called, the lazy instantiation creates an object and
    then sets the attribute to it, counting as setting.
    """
    point2D = Point2DFix(69, 420)
    circle = CircleFix(point2D, 1337)
    z = ComplexFix(69, 420)
    z0 = ComplexFix()  # Has no attributes set
    self.assertEqual(point2D.x, 69)
    self.assertEqual(point2D.y, 420)
    self.assertEqual(circle.center, point2D)
    self.assertEqual(circle.radius, 1337)
    self.assertEqual(z.RE, 69)
    self.assertEqual(z.IM, 420)
    self.assertFalse(z0.RE)  # Lazy instantiation counts as setting
    self.assertFalse(z0.IM)  # both RE and IM falls back to 0.0
    with self.assertRaises(WriteOnceError) as context:
      point2D.x = 1337
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.desc, Point2DFix.x)
    self.assertEqual(e.oldValue, 69)
    self.assertEqual(e.newValue, 1337)
    with self.assertRaises(WriteOnceError) as context:
      point2D.y = 1337
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.desc, Point2DFix.y)
    self.assertEqual(e.oldValue, 420)
    self.assertEqual(e.newValue, 1337)
    newCenter = Point2DFix(1337, 80085)
    with self.assertRaises(WriteOnceError) as context:
      circle.center = newCenter
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.desc, CircleFix.center)
    self.assertIs(e.oldValue, point2D)
    self.assertIs(e.newValue, newCenter)
    with self.assertRaises(WriteOnceError) as context:
      circle.radius = .420
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertAlmostEqual(e.desc, CircleFix.radius)
    self.assertAlmostEqual(e.oldValue, 1337)
    self.assertAlmostEqual(e.newValue, .420)
    with self.assertRaises(WriteOnceError) as context:
      z.RE = 1337
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertAlmostEqual(e.desc, ComplexFix.RE)
    self.assertAlmostEqual(e.oldValue, 69)
    self.assertAlmostEqual(e.newValue, 1337)
    with self.assertRaises(WriteOnceError) as context:
      z.IM = 1337
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertAlmostEqual(e.desc, ComplexFix.IM)
    self.assertAlmostEqual(e.oldValue, 420)
    self.assertAlmostEqual(e.newValue, 1337)
    with self.assertRaises(WriteOnceError) as context:
      z0.RE = 1337
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertAlmostEqual(e.desc, ComplexFix.RE)
    self.assertAlmostEqual(e.oldValue, 0.0)
    self.assertAlmostEqual(e.newValue, 1337)
    with self.assertRaises(WriteOnceError) as context:
      z0.IM = 1337
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertAlmostEqual(e.desc, ComplexFix.IM)
    self.assertAlmostEqual(e.oldValue, 0.0)
    self.assertAlmostEqual(e.newValue, 1337)

  def test_bad_delete(self, ) -> None:
    """
    Testing that deleting attributes that are not set raises appropriate
    errors.
    """
    point2D = Point2DFix(69, 420)
    self.assertEqual(point2D.x, 69)
    self.assertEqual(point2D.y, 420)
    circle = CircleFix(point2D, 1337)
    self.assertEqual(circle.center, point2D)
    self.assertEqual(circle.radius, 1337)
    z = ComplexFix(69, 420)
    self.assertEqual(z.RE, 69)
    self.assertEqual(z.IM, 420)
    with self.assertRaises(ProtectedError) as context:
      del point2D.x
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.instance, point2D)
    self.assertIs(e.desc, Point2DFix.x)
    self.assertAlmostEqual(e.oldVal, 69)
    with self.assertRaises(ProtectedError) as context:
      del point2D.y
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.instance, point2D)
    self.assertIs(e.desc, Point2DFix.y)
    self.assertAlmostEqual(e.oldVal, 420)
    with self.assertRaises(ProtectedError) as context:
      del circle.center
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.instance, circle)
    self.assertIs(e.desc, CircleFix.center)
    self.assertIs(e.oldVal, point2D)
    with self.assertRaises(ProtectedError) as context:
      del circle.radius
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.instance, circle)
    self.assertIs(e.desc, CircleFix.radius)
    self.assertAlmostEqual(e.oldVal, 1337)
    with self.assertRaises(ProtectedError) as context:
      del z.RE
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.instance, z)
    self.assertIs(e.desc, ComplexFix.RE)
    self.assertAlmostEqual(e.oldVal, 69)
    with self.assertRaises(ProtectedError) as context:
      del z.IM
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertIs(e.instance, z)
    self.assertIs(e.desc, ComplexFix.IM)
    self.assertAlmostEqual(e.oldVal, 420)

  def test_gymnastics(self) -> None:
    """
    Covering certain edge cases.
    """

    class Bar:
      foo = FixBox[int]()

    bar = Bar()
    setattr(Bar.foo, '__context_instance__', bar)
    setattr(Bar.foo, '__context_owner__', Bar)
    with self.assertRaises(RecursionError):
      Bar.foo.__instance_get__(bar, Bar, _recursion=True)
    with self.assertRaises(RecursionError):
      Bar.foo.__instance_set__(bar, 'baz', _recursion=True)
