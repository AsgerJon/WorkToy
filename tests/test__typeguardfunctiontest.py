"""Testing the typeGuardFunctionTest"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import unittest
from unittest import skip

from icecream import ic

from _unittestunstupid import UnstupidTest
from worktoy.core import Numerical
from worktoy.waitaminute import typeGuardFunctionTest, TypeGuardError

ic.configureOutput(includeContext=True)


class TypeGuardFunctionTest(UnstupidTest):
  """Testing the typeGuardFunctionTest
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def test_same_type_pass(self):
    def add_numbers(a: int, b: int) -> int:
      return a + b

    invArgs = [{'type': int, 'value': 5}, {'type': int, 'value': 10}]
    expRes = int

    result = typeGuardFunctionTest(add_numbers, invArgs, expRes)
    self.assertEqual(result, add_numbers)

  def test_same_type_fail(self):
    def add_numbers(a: int, b: int) -> int:
      return a + b

    invArgs = [{'type': int, 'value': 5}, {'type': int, 'value': 10}]
    expRes = str

    with self.assertRaises(TypeGuardError):
      typeGuardFunctionTest(add_numbers, invArgs, expRes)

  def test_numerical_type_pass(self):
    """Testing numerical pass through."""

    def add_numbers(a: Numerical, b: Numerical) -> Numerical:
      """Adds two numbers"""
      return a + b

    invArgs = [{'type': float, 'value': 7}, {'type': int, 'value': 7}]
    expRes = Numerical
    result = typeGuardFunctionTest(add_numbers, invArgs, expRes)

    self.assertEqual(result, add_numbers)

  def test_numerical_type_fail(self):
    """Testing proper fail."""

    def add_numbers(a: Numerical, b: Numerical) -> Numerical:
      """Adds two numbers"""
      return a + b

    invArgs = [{'type': float}, {'type': int}]
    expRes = str

    with self.assertRaises(TypeGuardError):
      typeGuardFunctionTest(add_numbers, invArgs, expRes)

  def test_optional_arg_pass(self):
    def greet(name: str, age: int = None) -> str:
      if age is None:
        return f"Hello, {name}!"
      else:
        return f"Hello, {name}! You are {age} years old."

    invArgs = [{'type': str, 'value': 'John'}, {'type': int}]
    expRes = str

    result = typeGuardFunctionTest(greet, invArgs, expRes)
    self.assertEqual(result, greet)

  def test_optional_arg_fail(self):
    def greet(name: str, age: int = None) -> str:
      if age is None:
        return f"Hello, {name}!"
      else:
        return f"Hello, {name}! You are {age} years old."

    invArgs = [{'type': str, 'value': 'John'}, {'type': int}]
    expRes = int

    with self.assertRaises(TypeGuardError):
      typeGuardFunctionTest(greet, invArgs, expRes)

  def test_function_return_none_pass(self):
    def do_nothing() -> None:
      pass

    invArgs = []
    expRes = None

    result = typeGuardFunctionTest(do_nothing, invArgs, expRes)
    self.assertEqual(result, do_nothing)

  def test_function_return_none_fail(self):
    def do_nothing() -> None:
      pass

    invArgs = []
    expRes = int

    with self.assertRaises(TypeGuardError):
      typeGuardFunctionTest(do_nothing, invArgs, expRes)


if __name__ == '__main__':
  unittest.main()
