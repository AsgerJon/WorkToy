"""
TestPermuterWithoutArrangement subclasses 'DispatcherTest' and pins that
calling a 'Permuter' that never received an 'Arrangement' raises
'MissingVariable' naming '__arg_arrangement__'. It used to fail on the
internal attribute, with an 'AttributeError' about 'None'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import Permuter, PermuterMethod
from worktoy.utilities.combinatorics import Arrangement
from worktoy.waitaminute import MissingVariable

from . import DispatcherTest


def _pair(a: int, b: int) -> tuple:
  return a, b


class TestPermuterWithoutArrangement(DispatcherTest):
  """
  TestPermuterWithoutArrangement provides tests for a 'Permuter' called
  without an 'Arrangement'.
  """

  def test_permuter(self) -> None:
    """A 'Permuter' raises 'MissingVariable'."""
    with self.assertRaises(MissingVariable) as context:
      Permuter(_pair)(1, 2)
    self.assertEqual(context.exception.varName, '__arg_arrangement__')

  def test_permuter_method(self) -> None:
    """A 'PermuterMethod' raises 'MissingVariable' as well."""
    with self.assertRaises(MissingVariable):
      PermuterMethod(_pair)(None, 1)

  def test_with_arrangement(self) -> None:
    """With an 'Arrangement' the arguments are restored."""
    permuter = Permuter(_pair, Arrangement(('a', 'b'), (1, 0)))
    self.assertEqual(permuter(2, 1), (1, 2))
