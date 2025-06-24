"""
The 'permutate' module receives any number of positional arguments and
returns a list of tuples each containing a unique permutation of the
arguments.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeAlias

  Permutation: TypeAlias = tuple[Any, ...]
  IntPerms: TypeAlias = list[tuple[int, ...]]
  Permutations: TypeAlias = list[Permutation]


def permutate(*args, **kwargs) -> Permutations:
  """
  Generate all unique permutations of the provided arguments.

  Args:
    *args: Positional arguments to permutate.
    **kwargs: Keyword arguments (not used in this function).

  Returns:
    list[tuple]: A list of tuples, each containing a unique permutation
    of the provided arguments.
  """
  if not args:
    return [()]
  if len(args) == 1:
    return [args]
  if len(args) == 2:
    return [args, (*reversed(args),)]
  out = []
  for i, arg in enumerate(args):
    rest = permutate(*[a for j, a in enumerate(args) if j != i])
    for perm in rest:
      out.append((arg, *perm))
  return out
