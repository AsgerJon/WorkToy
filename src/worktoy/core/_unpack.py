"""
The 'unpack' function squeezes a tuple of arguments until no array like
member remains.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Iterable

from worktoy.waitaminute import UnpackException

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, TypeAlias, Any


def unpack(*args: Any, **kwargs) -> tuple[Any, ...]:
  """
  Recursively unpacks iterables from positional arguments.

  This function traverses the given positional arguments and flattens
  any array-like values (iterables), except for str and bytes, which
  are treated as atomic.

  Supported keyword arguments:

  - shallow (bool, default False):
    If True, only unpacks the first level of nested iterables.

  - strict (bool, default True):
    If True, raises ValueError if no iterable argument was found.
    If False, returns arguments unchanged if no iterable is found.

  Args:
    *args: Positional arguments to unpack.
    **kwargs: Optional 'shallow' and 'strict' flags.

  Returns:
    tuple[Any, ...]: A flattened tuple of arguments.

  Raises:
    ValueError: If strict is True and no iterable was found.
  """
  if not args:
    if kwargs.get('strict', True):
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
  raise UnpackException(*args, )
