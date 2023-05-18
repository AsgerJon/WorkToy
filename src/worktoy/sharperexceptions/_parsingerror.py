"""Documentation: Parsing Error"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen

from typing import Any


#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
class ParsingError(Exception):
  """Exception raised for parsing errors.

  Attributes:
    variable: The variable that is unexpectedly None.
    expected_type: The expected type of the variable.
  """

  def __init__(self, variable: Any, expected_type: type) -> None:
    self.variable = variable
    self.expected_type = expected_type
    message = f"Error parsing variable: {variable}. Expected type: " \
              f"{expected_type}."
    super().__init__(message)
