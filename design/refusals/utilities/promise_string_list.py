"""
RefusedStringList holds the refusals that belong with
'design.promises.utilities.promise_string_list'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import stringList
from worktoy.waitaminute import TypeException


class RefusedStringList(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A separator of any other type raises 'TypeException'. Source:
  the 'stringList' docstring and its examples.
  """

  def test_bad_separator(self) -> None:
    with self.assertRaises(Exception) as refused:
      stringList('a, b', separator=7)
    self.assertIsInstance(refused.exception, TypeException)
