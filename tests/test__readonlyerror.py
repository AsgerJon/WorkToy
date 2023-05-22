"""Testing ReadOnlyError"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import unittest
from typing import Any

from worktoy.stringtools import monoSpace


class ReadOnlyError(Exception):
  """Custom exception for read-only operations."""

  def __init__(self, var_name: str, function: str) -> None:
    """Initialize the ReadOnlyError exception.

    Args:
        var_name (str): Name of the variable.
        function (str): Name of the function invoking the error.
    """
    self.var_name = var_name
    self.function = function
    super().__init__(self.__str__())

  def __str__(self) -> str:
    """Return a string representation of the exception.

    Returns:
        str: String representation of the exception.
    """
    return monoSpace(
      f"Tried to access {self.var_name} using {self.function}, which is "
      f"not a permitted operation!"
    )


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
