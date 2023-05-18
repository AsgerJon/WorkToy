"""Documentation: ArgumentError
Exception raised when an argument is missing or empty.

Args:
  instance (object): The instance where the argument is missing or empty.
  arg (str): The name of the missing or empty argument.

Attributes:
  instance (object): The instance where the argument is missing or empty.
  arg (str): The name of the missing or empty argument.

Raises:
  ArgumentError: If an argument is missing or empty.

"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any


class ArgumentError(Exception):
  """Exception raised when an argument is missing or empty.

  Args:
    instance (object): The instance where the argument is missing or empty.
    arg (str): The name of the missing or empty argument.

  Attributes:
    instance (object): The instance where the argument is missing or empty.
    arg (str): The name of the missing or empty argument.

  Raises:
    ArgumentError: If an argument is missing or empty."""

  def __init__(self, instance: Any, arg: Any) -> None:
    self.instance = instance
    self.arg = arg
    class_name = getattr(getattr(instance, '__class__'), '__name__')
    error_message = (
        "ArgumentError: '%s.%s' is missing or empty for instance '%s'."
        % (class_name, arg, instance)
    )
    super().__init__(error_message)
