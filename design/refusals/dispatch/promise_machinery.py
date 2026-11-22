"""
RefusedMachinery holds the refusals that belong with
'design.promises.dispatch.promise_machinery'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.dispatch import flexCall
from worktoy.waitaminute import TypeException


class RefusedMachinery(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A function wrapped by 'flexCall' still raises 'TypeError' for
  a missing required argument, and 'flexCall' of anything but a plain
  function raises 'TypeException'. Source: the docstrings of these names.
  """

  def test_flex_call_1(self) -> None:
    def add(a: int, b: int) -> int:
      return a + b

    wrapped = flexCall(add)
    with self.assertRaises(Exception) as refused:
      wrapped(1)
    self.assertIsInstance(refused.exception, TypeError)

  def test_flex_call_2(self) -> None:
    def add(a: int, b: int) -> int:
      return a + b

    wrapped = flexCall(add)
    with self.assertRaises(Exception) as refused:
      flexCall(len)
    self.assertIsInstance(refused.exception, TypeException)
