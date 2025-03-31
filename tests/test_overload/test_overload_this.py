#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
#
# from unittest import TestCase
#
# from worktoy.static import overload, THIS
# from worktoy.attr import AttriBox
# from worktoy.base import BaseObject
#
# try:
#   from typing import TYPE_CHECKING
# except ImportError:
#   TYPE_CHECKING = False
#
# if TYPE_CHECKING:
#   from typing import Self
# else:
#   Any = object
#
#
#   class Self:
#     IM: float
#     RE: float
#
# eps = 1e-10
#
#
# class Complex(BaseObject):
#   """Complex is a class that inherits from BaseObject. """
#
#   RE = AttriBox[float](0)
#   IM = AttriBox[float](0)
#
#   @overload(float, float)
#   def __init__(self, re: float, im: float) -> None:
#     self.RE = re
#     self.IM = im
#
#   @overload(THIS)
#   def __init__(self, other: Self) -> None:
#     self.RE = other.RE
#     self.IM = other.IM
#
#   @overload()
#   def __init__(self) -> None:
#     self.RE = 0
#     self.IM = 0
#
#
# class TestOverloadThis(TestCase):
#   """TestOverloadThis tests that the overload protocol implemented in
#   'worktoy' supports the use of 'THIS' when overloading functions. """
#
#   def setUp(self) -> None:
#     """Sets up each test"""
#     self.complex = Complex(69, 420)
#     self.complexCopy = Complex(self.complex)
#
#   def test_init(self) -> None:
#     """Testing that points have initialized correctly"""
#     self.assertEqual(self.complex.RE, 69)
#     self.assertEqual(self.complex.IM, 420)
#     self.assertEqual(self.complexCopy.RE, 69)
#     self.assertEqual(self.complexCopy.IM, 420)
