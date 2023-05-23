"""Transforms strings from snake_case to camelCase"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations
import re


def snakeCaseToCamelCase(string):
  """Replaces all instances of snake_case with camelCase in a given string.
  Args:

      string (str): The input string containing snake_case.
  Returns:
      str: The resulting string with snake_case replaced by camelCase."""

  def camelCase(match):
    """Convert snake_case match to camelCase"""
    return match.group(1).upper()

  # Use regular expression to find snake_case and replace with camelCase
  pattern = r'_(\w)'
  result = re.sub(pattern, camelCase, string)

  return result
