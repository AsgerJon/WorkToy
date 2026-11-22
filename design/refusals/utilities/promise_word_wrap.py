"""
RefusedWordWrap holds the refusals that belong with
'design.promises.utilities.promise_word_wrap'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import wordWrap
from worktoy.waitaminute import TypeException


class RefusedWordWrap(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A width that is no 'int', or a fragment that is no 'str',
  raises 'TypeException'; a width below one raises 'ValueError'. Source: the
  'wordWrap' docstring and its examples.
  """

  def test_bad_width_type(self) -> None:
    with self.assertRaises(Exception) as refused:
      wordWrap('12', 'text')
    self.assertIsInstance(refused.exception, TypeException)

  def test_bad_fragment_type(self) -> None:
    with self.assertRaises(Exception) as refused:
      wordWrap(12, 'text', 7)
    self.assertIsInstance(refused.exception, TypeException)

  def test_width_below_one(self) -> None:
    with self.assertRaises(Exception) as refused:
      wordWrap(0, 'text')
    self.assertIsInstance(refused.exception, ValueError)
