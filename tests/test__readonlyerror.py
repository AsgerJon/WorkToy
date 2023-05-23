"""Testing ReadOnlyError"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import unittest
from typing import Any

from worktoy.waitaminute import ReadOnlyError


class MyClass:
  """Example class that raises ReadOnlyError exceptions."""

  def __init__(self, value: Any) -> None:
    self._value = value

  @property
  def value(self) -> Any:
    """Getter for the value property."""
    return self._value

  @value.setter
  def value(self, new_value: Any) -> None:
    """Setter for the value property."""
    raise ReadOnlyError("value", "setter")

  @value.deleter
  def value(self) -> None:
    """Deleter for the value property."""
    raise ReadOnlyError("value", "deleter")


class TestReadOnlyError(unittest.TestCase):
  """Unit tests for ReadOnlyError"""

  def setUp(self) -> None:
    """Set up test fixtures"""
    pass

  def tearDown(self) -> None:
    """Tear down test fixtures"""
    pass

  def test_read_only_exception(self) -> None:
    """Test ReadOnlyError exception"""
    my_obj = MyClass("initial_value")

    # Accessing the value property should not raise an exception
    self.assertEqual(my_obj.value, "initial_value")

    # Attempting to set the value property should raise ReadOnlyError
    with self.assertRaises(ReadOnlyError):
      my_obj.value = "new_value"

    # Attempting to delete the value property should raise ReadOnlyError
    with self.assertRaises(ReadOnlyError):
      del my_obj.value
