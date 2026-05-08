"""Recursive flattener for varargs.

The ``unpack`` function expands every iterable in the positional
arguments (other than ``str`` / ``bytes``) until none remain,
producing a flat tuple."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def unpack(*args: Any, **kwargs) -> tuple[Any, ...]:
  """Flatten nested iterables in positional arguments.

  Iterables are expanded recursively; ``str`` and ``bytes`` are
  treated as atomic and never split into their characters/bytes.

  Parameters
  ----------
  *args : Any
      The values to unpack.
  **kwargs
      shallow : bool, optional
          If ``True``, only the top level is expanded; nested
          iterables are left intact. Defaults to ``False``.
      strict : bool, optional
          If ``True`` (default), raises when no iterable was found
          among ``args``. If ``False``, the arguments are returned
          unchanged in that case.

  Returns
  -------
  tuple
      The flattened tuple.

  Raises
  ------
  UnpackException
      If ``strict`` is ``True`` and no iterable was supplied.

  Examples
  --------
  >>> unpack([1, 2], (3, [4, 5]))
  (1, 2, 3, 4, 5)
  >>> unpack([1, [2, 3]], shallow=True)
  (1, [2, 3])
  >>> unpack('abc', [1, 2])
  ('abc', 1, 2)
  """
  if not args:
    if kwargs.get('strict', True):
      from worktoy.waitaminute import UnpackException
      raise UnpackException(*args, )
    return ()
  out = []
  iterableFound = False
  for arg in args:
    if isinstance(arg, (str, bytes,)):
      out.append(arg)
      continue
    if isinstance(arg, Iterable):
      if kwargs.get('shallow', False):
        out.extend(arg)
      else:
        out = [*out, *unpack(*arg, shallow=False, strict=False)]
      iterableFound = True
      continue
    out.append(arg)
  if iterableFound or not kwargs.get('strict', True):
    return (*out,)
  from worktoy.waitaminute import UnpackException
  raise UnpackException(*args, )
