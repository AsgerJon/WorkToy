#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
#
# from worktoy.attr import AttriBox
# from worktoy.base import BaseObject
# from worktoy.static import overload, THIS
#
# from worktoy.ezdata import EZData
# from worktoy.waitaminute import DispatchException
#
# try:
#   from typing import Self
# except ImportError:
#   Self = object
#
#
# class Point2D(BaseObject):
#   """Plane point"""
#
#   x = AttriBox[float](0)
#   y = AttriBox[float](0)
#
#   @overload(float, float)
#   def __init__(self, x: float, y: float) -> None:
#     self.x = x
#     self.y = y
#
#   @overload(complex)
#   def __init__(self, z: complex) -> None:
#     self.x = z.real
#     self.y = z.imag
#
#   @overload(THIS)
#   def __init__(self, other: Self) -> None:
#     self.x = other.x
#     self.y = other.y
#
#   @overload()
#   def __init__(self) -> None:
#     self.x = 0
#     self.y = 0
#
#
# class Complex(BaseObject):
#   """Complex number"""
#
#   RE = AttriBox[float](0)
#   IM = AttriBox[float](0)
#
#   def __init__(self, *args) -> None:
#     self.RE, self.IM = [*args, 0, 0][:2]
#
#
# # class PlanePoint(Point2D):
# #   """Point in the plane"""
# #
# #   @overload(Complex)
# #   def __init__(self, z: Complex) -> None:
# #     self.x = z.RE
# #     self.y = z.IM
#
#
# class TestOverloadsInSubclasses(TestCase):
#   """TestOverloadsInSubclasses tests that a subclass can add overloads to a
#   method overloaded in the parent class."""
#
#   def testIntFloats(self, ) -> None:
#     """Tests if ints are correctly static to floats. """
#
#     point = Point2D(1., 2.)
#
#   #
#   # def setUp(self) -> None:
#   #   """Sets up each test method."""
#   #   self.pointIntInt = Point2D(1, 2)
#   #   self.pointComplex = Point2D(1 + 2j)
#   #   self.pointEmpty = Point2D()
#   #   self.pointPoint = Point2D(self.pointIntInt)
#   #
#   #   self.planeIntInt = PlanePoint(3, 4)
#   #   self.planeComplex = PlanePoint(3 + 4j)
#   #   self.planeEmpty = PlanePoint()
#   #   self.planeCustomComplex = PlanePoint(Complex(3, 4))
#   #   self.planePlane = PlanePoint(self.planeIntInt)
#   #
#   #   self.pointPlane = Point2D(self.planeIntInt)
#   #
#   # def test_point(self) -> None:
#   #   """Tests the Point2D class."""
#   #   self.assertEqual(self.pointIntInt.x, 1)
#   #   self.assertEqual(self.pointIntInt.y, 2)
#   #
#   #   self.assertEqual(self.pointComplex.x, 1)
#   #   self.assertEqual(self.pointComplex.y, 2)
#   #
#   #   self.assertEqual(self.pointEmpty.x, 0)
#   #   self.assertEqual(self.pointEmpty.y, 0)
#   #
#   #   self.assertEqual(self.pointPoint.x, 1)
#   #   self.assertEqual(self.pointPoint.y, 2)
#   #
#   # def test_plane(self) -> None:
#   #   """Tests the PlanePoint class."""
#   #   self.assertEqual(self.planeIntInt.x, 3)
#   #   self.assertEqual(self.planeIntInt.y, 4)
#   #
#   #   self.assertEqual(self.planeComplex.x, 3)
#   #   self.assertEqual(self.planeComplex.y, 4)
#   #
#   #   self.assertEqual(self.planeEmpty.x, 0)
#   #   self.assertEqual(self.planeEmpty.y, 0)
#   #
#   #   self.assertEqual(self.planeCustomComplex.x, 3)
#   #   self.assertEqual(self.planeCustomComplex.y, 4)
#   #
#   #   self.assertEqual(self.planePlane.x, 3)
#   #   self.assertEqual(self.planePlane.y, 4)
#   #
#   #   self.assertEqual(self.pointPlane.x, 3)
#   #   self.assertEqual(self.pointPlane.y, 4)
#   #
#   # def test_error(self, ) -> None:
#   #   """Testing proper error handling"""
#   #
#   #   with self.assertRaises(DispatchException) as context:
#   #     PlanePoint(Point2D(69, 420))
