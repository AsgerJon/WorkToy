#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
#
# from unittest import TestCase
#
# from worktoy.ezdata import EZData
# from worktoy.static import overload, TypeSig
#
# try:
#   from typing import Never
# except ImportError:
#   try:
#     from typing import NoReturn as Never
#   except ImportError:
#     Never = None
#
#
# class PlanePoint(EZData):
#   """Represents a point in the plane"""
#
#   x = 0
#   y = 0
#
#   @overload(int, int)
#   def __init__(self, x: int, y: int):
#     self.x = x
#     self.y = y
#
#   @overload(int)
#   def __init__(self, x: int):
#     self.x = x
#     self.y = 0
#
#   @overload()
#   def __init__(self):
#     pass
#
#   @overload.fallback
#   def __init__(self, *args, **kwargs) -> Never:
#     e = """Fallback overload function called! Received the following type
#     signature: %s"""
#     typeSig = TypeSig(*[type(arg) for arg in args], )
#     raise TypeError(e % str(typeSig))
#
#
# class TestOverloadFallback(TestCase):
#   """TestOverloadFallback tests that the overloading protocol correctly
#   attempts to call the indicated fallback function when none of the other
#   overloads match the type signature of the arguments received. """
#
#   def setUp(self) -> None:
#     self.point0args = PlanePoint()
#     self.point1args = PlanePoint(69)
#     self.point2args = PlanePoint(69, 420)
#
#   def test_init(self, ) -> None:
#     """Testing that the class still initializes correctly in the presence
#     of the fallback overload."""
#     self.assertEqual(self.point0args.x, 0)
#     self.assertEqual(self.point0args.y, 0)
#     self.assertEqual(self.point1args.x, 69)
#     self.assertEqual(self.point1args.y, 0)
#     self.assertEqual(self.point2args.x, 69)
#     self.assertEqual(self.point2args.y, 420)
#
#   def test_error(self) -> None:
#     """Tests that the fallback overload is correctly called, when unable
#     tao match the type signature of the arguments received. The expected
#     exception is DispatchException, which should be raised when the
#     fallback overload raises any exception. """
#
#     with self.assertRaises(TypeError) as context:
#       PlanePoint('hello', 'world')
#
#     with self.assertRaises(TypeError):
#       PlanePoint(1, 2, 3)
