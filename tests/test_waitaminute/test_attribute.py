#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
#
# from unittest import TestCase
#
# from worktoy.attr import AttriBox
# from worktoy.mcls import BaseObject
# from worktoy.static import overload
# from worktoy.static.zeroton import THIS
# from worktoy.waitaminute import _Attribute, TypeException
#
# try:
#   from typing import TYPE_CHECKING
# except ImportError:
#   try:
#     from typing_extensions import TYPE_CHECKING
#   except ImportError:
#     TYPE_CHECKING = False
#
# if TYPE_CHECKING:
#   from typing import Any, Callable, Self
#
#
# class _TestError(Exception):
#   """_TestError indicates a value outside a required interval."""
#
#   valueReceived = _Attribute()
#   valueMinimum = _Attribute()
#   valueMaximum = _Attribute()
#
#   def __init__(self, *args) -> None:
#     """Initialize the TestWarning exception."""
#     self.valueReceived = args[0]
#     self.valueMinimum = args[1]
#     self.valueMaximum = args[2]
#     infoSpec = """Received value: %s not in required interval: [%s, %s]"""
#     valAct = self.valueReceived
#     valMin = self.valueMinimum
#     valMax = self.valueMaximum
#     info = infoSpec % (valAct, valMin, valMax)
#     Exception.__init__(self, info)
#
#
# class UnitPoint(BaseObject):
#   """UnitPoint provides a point in a unit square."""
#
#   x = AttriBox[float](0.0)
#   y = AttriBox[float](0.0)
#
#   @staticmethod
#   def validateValue(value: float) -> None:
#     """Validate the UnitPoint object."""
#     if value ** 2 > 1:
#       raise _TestError(value, -1, 1)
#
#   @staticmethod
#   def validateType(value: object) -> None:
#     """Validate the type of the value."""
#     if not isinstance(value, (int, float)):
#       raise TypeException('value', value, (int, float))
#
#   @overload(float, float)
#   @overload(float, int)
#   @overload(int, float)
#   @overload(int, int)
#   def __init__(self, x: float, y: float) -> None:
#     """Initialize the UnitPoint object."""
#     x, y = float(x), float(y)
#     self.validateType(x)
#     self.validateType(y)
#     self.validateValue(x)
#     self.validateValue(y)
#     self.x = x
#     self.y = y
#
#   @overload(complex)
#   def __init__(self, value: complex) -> None:
#     """Initialize the UnitPoint object."""
#     x, y = float(value.real), float(value.imag)
#     self.__init__(x, y)
#
#   @overload(THIS)
#   def __init__(self, other: UnitPoint) -> None:
#     """Initialize the UnitPoint object."""
#     x, y = float(other.x), float(other.y)
#     self.__init__(x, y)
#
#   @overload()
#   def __init__(self, **kwargs) -> None:
#     """Initialize the UnitPoint object."""
#     x = kwargs.get('x', 0.0)
#     y = kwargs.get('y', 0.0)
#     self.validateType(x)
#     self.validateType(y)
#     self.validateValue(x)
#     self.validateValue(y)
#
#   def __str__(self, ) -> str:
#     """String representation of the UnitPoint object."""
#     return """(%s, %s)""" % (self.x, self.y)
#
#   def __repr__(self, ) -> str:
#     """String representation of the UnitPoint object."""
#     clsName = type(self).__name__
#     return """%s%s""" % (clsName, self.__str__())
#
#   def __complex__(self, ) -> complex:
#     """Convert the UnitPoint object to a complex number."""
#     return self.x + self.y * 1j
#
#
# class TestAttribute(TestCase):
#   """TestWaitAMinute tests the custom exceptions from the
#   'worktoy.waitaminute' module."""
#
#   def setUp(self) -> None:
#     """Sets up the test case."""
#     self.p1 = UnitPoint(0.69, 0.420)
#     self.p2 = UnitPoint(0.1337, 0.80085)
#     self.p3 = UnitPoint(self.p1)
#
#   def test_attribute(self, ) -> None:
#     """Test the Attribute descriptor. """
#     self.assertEqual(self.p1.x, 0.69)
#     self.assertEqual(self.p1.y, 0.420)
#     self.assertEqual(self.p2.x, 0.1337)
#     self.assertEqual(self.p2.y, 0.80085)
#     self.assertEqual(self.p3.x, 0.69)
#     self.assertEqual(self.p3.y, 0.420)
#
#   def test_errors(self) -> None:
#     """Test the Attribute descriptor. """
#     with self.assertRaises(_TestError):
#       UnitPoint(2.0, 0.0)
#     with self.assertRaises(_TestError):
#       UnitPoint(0.0, 2.0)
#     with self.assertRaises(_TestError):
#       UnitPoint(2.0 + 1j)
#     with self.assertRaises(TypeException):
#       UnitPoint(x='69', y='420')
