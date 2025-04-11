#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
#
# from unittest import TestCase
#
# from worktoy.static import overload
# from worktoy.base import BaseObject
# from worktoy.attr import AttriBox
# from worktoy.ezdata import EZData
#
#
# class Parent(BaseObject):
#   """Parent class"""
#
#   x = AttriBox[int](0)
#   y = AttriBox[int](0)
#
#   @overload(int, int)
#   def __init__(self, *args) -> None:
#     self.x = args[0]
#     self.y = args[1]
#
#
# class Child(Parent):
#   """Child class"""
#
#   z = AttriBox[int](0)
#
#   @overload(int, int, int)
#   def __init__(self, *args) -> None:
#     self.x = args[0]
#     self.y = args[1]
#     self.z = args[2]
#
#
# class GrandChild(Child):
#   """GrandChild class"""
#
#   w = AttriBox[int](0)
#
#   @overload(int, int, int, int)
#   def __init__(self, *args) -> None:
#     self.x = args[0]
#     self.y = args[1]
#     self.z = args[2]
#     self.w = args[3]
#
#
# class FastParent(EZData):
#   """Parent class"""
#
#   x = AttriBox[int](0)
#   y = AttriBox[int](0)
#
#   @overload(int, int)
#   def __init__(self, *args) -> None:
#     self.x = args[0]
#     self.y = args[1]
#
#
# class FastChild(Parent):
#   """Child class"""
#
#   z = AttriBox[int](0)
#
#   @overload(int, int, int)
#   def __init__(self, *args) -> None:
#     self.x = args[0]
#     self.y = args[1]
#     self.z = args[2]
#
#
# class FastGrandChild(Child):
#   """GrandChild class"""
#
#   w = AttriBox[int](0)
#
#   @overload(int, int, int, int)
#   def __init__(self, *args) -> None:
#     self.x = args[0]
#     self.y = args[1]
#     self.z = args[2]
#     self.w = args[3]
#
#
# class TestOverloadPolymorphism(TestCase):
#   """TestOverloadPolymorphism tests that a Child class can add overloads to
#   an overloaded function in the Parent class."""
#
#   def setUp(self) -> None:
#     """Sets up each test method."""
#     self.parentPoint = Parent(69, 420)
#     self.childParentPoint = Child(69, 420, )
#     self.childChildPoint = Child(69, 420, 1337)
#     self.grandChildParentPoint = GrandChild(69, 420, )
#     self.grandChildChildPoint = GrandChild(69, 420, 1337)
#     self.grandChildGrandChildPoint = GrandChild(69, 420, 1337, 80085)
#     self.fastParentPoint = Parent(69, 420)
#     self.fastChildChildPoint = Child(69, 420, 1337)
#     self.fastGrandChildParentPoint = GrandChild(69, 420, )
#     self.fastGrandChildChildPoint = GrandChild(69, 420, 1337)
#     self.fastGrandChildGrandChildPoint = GrandChild(69, 420, 1337, 80085)
#
#   def testBase(self) -> None:
#     """Test if the __init__ method works correctly."""
#     self.assertEqual(self.parentPoint.x, 69)
#     self.assertEqual(self.parentPoint.y, 420)
#     #
#     self.assertEqual(self.childParentPoint.x, 69)
#     self.assertEqual(self.childParentPoint.y, 420)
#     self.assertEqual(self.childParentPoint.z, 0)
#
#     self.assertEqual(self.childChildPoint.x, 69)
#     self.assertEqual(self.childChildPoint.y, 420)
#     self.assertEqual(self.childChildPoint.z, 1337)
#
#     self.assertEqual(self.grandChildParentPoint.x, 69)
#     self.assertEqual(self.grandChildParentPoint.y, 420)
#     self.assertEqual(self.grandChildParentPoint.z, 0)
#     self.assertEqual(self.grandChildParentPoint.w, 0)
#
#     self.assertEqual(self.grandChildChildPoint.x, 69)
#     self.assertEqual(self.grandChildChildPoint.y, 420)
#     self.assertEqual(self.grandChildChildPoint.z, 1337)
#     self.assertEqual(self.grandChildChildPoint.w, 0)
#
#     self.assertEqual(self.grandChildGrandChildPoint.x, 69)
#     self.assertEqual(self.grandChildGrandChildPoint.y, 420)
#     self.assertEqual(self.grandChildGrandChildPoint.z, 1337)
#     self.assertEqual(self.grandChildGrandChildPoint.w, 80085)
#
#   def testFast(self) -> None:
#     """Testing the EZData implementation"""
#     self.assertEqual(self.fastParentPoint.x, 69)
#     self.assertEqual(self.fastParentPoint.y, 420)
#     #
#     self.assertEqual(self.fastChildChildPoint.x, 69)
#     self.assertEqual(self.fastChildChildPoint.y, 420)
#     self.assertEqual(self.fastChildChildPoint.z, 1337)
#
#     self.assertEqual(self.fastGrandChildParentPoint.x, 69)
#     self.assertEqual(self.fastGrandChildParentPoint.y, 420)
#     self.assertEqual(self.fastGrandChildParentPoint.z, 0)
#     self.assertEqual(self.fastGrandChildParentPoint.w, 0)
#
#     self.assertEqual(self.fastGrandChildChildPoint.x, 69)
#     self.assertEqual(self.fastGrandChildChildPoint.y, 420)
#     self.assertEqual(self.fastGrandChildChildPoint.z, 1337)
#     self.assertEqual(self.fastGrandChildChildPoint.w, 0)
#
#     self.assertEqual(self.fastGrandChildGrandChildPoint.x, 69)
#     self.assertEqual(self.fastGrandChildGrandChildPoint.y, 420)
#     self.assertEqual(self.fastGrandChildGrandChildPoint.z, 1337)
#     self.assertEqual(self.fastGrandChildGrandChildPoint.w, 80085)
