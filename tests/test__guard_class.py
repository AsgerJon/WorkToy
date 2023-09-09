"""Test of GuardClass"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
import unittest
from worktoy.worktoyclass import GuardClass
from worktoy.core import Function
from worktoy.waitaminute import UnavailableNameException
from worktoy.waitaminute import UnexpectedStateError, TypeSupportError


class TestGuardClass(unittest.TestCase):

  def setUp(self):
    self.guard = GuardClass()

  def test_noneGuard_with_none(self):
    self.assertIsNone(self.guard.noneGuard(None))

  def test_noneGuard_with_non_none(self):
    with self.assertRaises(UnavailableNameException):
      self.guard.noneGuard("Not None", "varName")

  def test_someGuard_with_none(self):
    with self.assertRaises(UnexpectedStateError):
      self.guard.someGuard(None, "varName")

  def test_someGuard_with_non_none(self):
    obj = "Not None"
    self.assertEqual(self.guard.someGuard(obj, "varName"), obj)

  def test_functionGuard_with_function(self):
    def sample_function():
      pass

    self.assertEqual(self.guard.functionGuard(sample_function),
                     sample_function)

  def test_functionGuard_with_non_function(self):
    with self.assertRaises(TypeSupportError):
      self.guard.functionGuard("Not a function", "name")

  def test_intGuard_with_integer(self):
    integer = 42
    self.assertEqual(self.guard.intGuard(integer, "name"), integer)

  def test_intGuard_with_non_integer(self):
    with self.assertRaises(TypeSupportError):
      self.guard.intGuard("Not an integer", "name")

  def test_floatGuard_with_float(self):
    float_value = 3.14
    self.assertEqual(self.guard.floatGuard(float_value, "name"), float_value)

  def test_floatGuard_with_integer(self):
    integer = 42
    self.assertEqual(self.guard.floatGuard(integer, "name"), integer)

  def test_floatGuard_with_non_float_or_integer(self):
    with self.assertRaises(TypeSupportError):
      self.guard.floatGuard("Not a float", "name")

  def test_strGuard_with_string(self):
    text = "Hello, World!"
    self.assertEqual(self.guard.strGuard(text, "name"), text)

  def test_strGuard_with_non_string(self):
    with self.assertRaises(TypeSupportError):
      self.guard.strGuard(42, "name")


if __name__ == '__main__':
  unittest.main()
