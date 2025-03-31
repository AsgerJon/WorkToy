#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
#
# from unittest import TestCase
#
# from worktoy.attr import AttriBox
# from worktoy.base import BaseObject
# from worktoy.waitaminute import DispatchException
# from worktoy.static import overload
#
#
# class Number(BaseObject):
#   """Number is a class that inherits from BaseObject. """
#
#   realVal = AttriBox[float](0)
#
#   def __init__(self, value: float) -> None:
#     self.realVal = float(value)
#
#
# class Complex(Number):
#   """Complex is a class that inherits from Number. """
#
#   imgVal = AttriBox[float](0)
#
#   def __init__(self, real: float, img: float) -> None:
#     self.realVal = real
#     self.imgVal = img
#
#
# class Point(BaseObject):
#   """Point is a class that inherits from BaseObject. """
#
#   x = AttriBox[float](0)
#   y = AttriBox[float](0)
#
#   @overload(float, float)
#   def __init__(self, x: float, y: float) -> None:
#     self.x = x
#     self.y = y
#
#   @overload(Number)
#   def __init__(self, number: Number) -> None:
#     self.x = number.realVal
#     self.y = 0
#
#   @overload(Complex)
#   def __init__(self, complexNumber: Complex) -> None:
#     self.x = complexNumber.realVal
#     self.y = complexNumber.imgVal
#
#
# class Point3D(BaseObject):
#   """Point3D is a class that inherits from Point. """
#
#   z = AttriBox[float](0)
#
#   @overload(float, float, float)
#   def __init__(self, x: float, y: float, z: float) -> None:
#     self.x = x
#     self.y = y
#     self.z = z
#
#   @overload(Complex)
#   def __init__(self, complexNumber: Complex) -> None:
#     self.x = complexNumber.realVal
#     self.y = complexNumber.imgVal
#     self.z = 0
#
#
# class Point2D(Point):
#   """Inheriting from Point to test if further overloads can be added by a
#   subclass. """
#
#   @overload(complex)
#   def __init__(self, complexNumber: complex) -> None:
#     self.x = complexNumber.real
#     self.y = complexNumber.imag
#
#
# class TestOverloadInheritance(TestCase):
#   """TestOverloadInheritance tests that the 'overload' decorator correctly
#   chooses an argument if that argument is an instance of a subclass of the
#   overloaded type."""
#
#   def setUp(self) -> None:
#     """Sets up each test method."""
#     self.complexNumber = Complex(69, 420)
#     self.number = Number(1337)
#     self.complex_ = 1337 + 80085j
#
#   def testNumber(self) -> None:
#     """Tests if Point accepts a Complex as well as a Number."""
#
#     pointNumber = Point(self.number)
#     self.assertEqual(pointNumber.x, 1337)
#     self.assertEqual(pointNumber.y, 0)
#
#   def testComplex(self) -> None:
#     """Tests if Point accepts a Complex as well as a Number."""
#     pointComplex = Point(self.complexNumber)
#     self.assertEqual(pointComplex.x, 69)
#     self.assertEqual(pointComplex.y, 420)
#
#   def testParentOverload(self) -> None:
#     """Tests if the overload correctly dispatches the Complex number to
#     the method with the parent class 'Number' as overload. If the overload
#     indicates class Parent, then the fastCast will not dispatch an
#     instance of Child, but the normal dispatch will."""
#     point3D = Point3D(self.complexNumber)
#     self.assertEqual(point3D.x, 69)
#     self.assertEqual(point3D.y, 420)
#     self.assertEqual(point3D.z, 0)
#
#   def testChildOverload(self) -> None:
#     """If Child is a subclass of Parent and an overload specifies Parent,
#     it should accept child instances as well, but if the overload
#     specifies Child, instances of Parent that are not instances of Child
#     should not be dispatched!"""
#
#     with self.assertRaises(DispatchException) as context:
#       Point3D(self.number)
#       print(context)
#
#   def testInheritedOverloads(self) -> None:
#     """If a Parent provides overloads at a particular name, can a Child
#     class provide additional overloads to the same name?"""
#
#     point2D = Point2D(self.complex_)
#     self.assertEqual(point2D.x, 1337)
#     self.assertEqual(point2D.y, 80085)
