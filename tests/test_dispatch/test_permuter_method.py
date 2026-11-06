"""
TestPermuterMethod tests 'PermuterMethod' from 'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import PermuterMethod, Permuter
from worktoy.utilities.combinatorics import Arrangement
from . import DispatchTest


def _method(self: object, a: str, b: str, c: str, **kw) -> tuple:
  return self, a, b, c, kw


class TestPermuterMethod(DispatchTest):
  """
  A flexible overload in a class body is a method, so the instance stays
  first and only the arguments after it are reordered. The tests pin the
  instance passing through untouched, the reordering behind it, the
  keywords, the call without any argument, and the wrong count.
  """

  @staticmethod
  def _cycle() -> Arrangement:
    return Arrangement(('a', 'b', 'c'), (2, 0, 1))

  def test_instance_stays_first(self) -> None:
    permuter = PermuterMethod(_method, self._cycle())
    owner = object()
    self.assertEqual(permuter(owner, 'C', 'A', 'B', k=1),
                     (owner, 'A', 'B', 'C', {'k': 1}))
    self.assertIsInstance(permuter, Permuter)

  def test_no_arguments_gives_none_instance(self) -> None:
    def bare(self: object) -> object:
      return self

    permuter = PermuterMethod(bare, Arrangement((), ()))
    self.assertIsNone(permuter())

  def test_wrong_count_refused(self) -> None:
    permuter = PermuterMethod(_method, self._cycle())
    with self.assertRaises(ValueError) as context:
      permuter(object(), 'A', 'B')
    self.assertIn("'restoreFrom' received '2' values",
                  str(context.exception))
