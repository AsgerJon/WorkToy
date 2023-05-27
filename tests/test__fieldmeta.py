#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from typing import NoReturn
import unittest

from worktoy.field import FieldMeta


class MyClass(FieldMeta):
  """Sample class"""

  def my_function(self) -> NoReturn:
    """Sample method"""
    pass

  def __str__(self) -> str:
    """Sample magic method"""
    return "MyClass"


class AnotherClass(FieldMeta):
  """Another sample class"""

  def __init__(self) -> None:
    """Sample initializer"""
    pass

  def some_method(self) -> NoReturn:
    """Sample method"""
    pass


class TestFieldMeta(unittest.TestCase):
  """Unit tests for FieldMeta"""

  def test_my_class(self) -> NoReturn:
    """Test MyClass"""
    obj = MyClass()
    self.assertEqual(obj.my_function.__cls__, MyClass)

  def test_another_class(self) -> NoReturn:
    """Test AnotherClass"""
    obj = AnotherClass()
    self.assertEqual(obj.some_method.__cls__, AnotherClass)
