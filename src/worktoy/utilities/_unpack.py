"""
The 'unpack' function flattens nested iterables in its arguments.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator, Optional


def _iterate(arg: Any) -> Optional[Iterator]:
  """Return an iterator over 'arg', or None when 'arg' does not iterate.
  An object may claim to be iterable and still refuse: every worktoy
  class does, since its metaclass defines '__iter__' for the
  '__class_iter__' hook, and iterating one without the hook raises
  'TypeError', as 'iter' does for anything not iterable."""
  if not isinstance(arg, Iterable):
    return None
  try:
    return iter(arg)
  except TypeError:
    return None


def _flatten(arg: Any, items: Iterator) -> list[Any]:
  """Flatten the 'items' of 'arg' recursively. An item that is 'arg'
  itself, as an 'ARGS' yields and a list holding itself contains, is
  kept whole, since unpacking it again would never end."""
  out = []
  for item in items:
    if item is arg:
      out.append(item)
      continue
    out.extend(unpack(item, shallow=False, strict=False))
  return out


def unpack(*args, **kwargs) -> tuple[Any, ...]:
  """Flatten nested iterables in positional arguments.

  Iterables are expanded recursively; the text types 'str', 'bytes' and
  'bytearray' are treated as atomic and never split into their
  characters or integers. An object that claims to be iterable but
  refuses iteration, such as a worktoy class without a '__class_iter__'
  hook, is kept whole.

  Parameters
  ----------
  *args : Any
      The values to unpack.
  **kwargs
      shallow : bool, optional
          If True, only the top level is expanded; nested iterables
          are left intact. Defaults to False.
      strict : bool, optional
          If True (default), raises when no iterable was supplied;
          this covers both an empty call and a call where no
          argument is iterable. If False, the input is passed
          through: an empty call returns '()' and non-iterable
          arguments are returned in a tuple as-is.

  Returns
  -------
  tuple
      The flattened tuple.

  Raises
  ------
  UnpackException
      If 'strict' is True and no iterable was supplied.

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
    if isinstance(arg, (str, bytes, bytearray,)):
      out.append(arg)
      continue
    items = _iterate(arg)
    if items is not None:
      if kwargs.get('shallow', False):
        out.extend(items)
      else:
        out.extend(_flatten(arg, items))
      iterableFound = True
      continue
    out.append(arg)
  if iterableFound or not kwargs.get('strict', True):
    return (*out,)
  from worktoy.waitaminute import UnpackException
  raise UnpackException(*args, )
