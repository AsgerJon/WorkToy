"""
Freddy lets you generate slices with the indexing syntax.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator


class _FreddyMeta(type):

  def __getitem__(cls, item: Any) -> Any:
    if isinstance(item, slice):
      return item
    return slice(item)

  def __call__(cls, *__, **_) -> Any:
    return cls  # Just for indexing syntax.

  def randSlice(cls, *args) -> slice:
    a, b, c, *_ = [*args, 1, 10, 1]
    step, start, stop = sorted((a, b, c), )
    return cls[start:stop:step]

  def randSlices(cls, N: int = None, *args) -> Iterator[slice]:
    if N is None:
      yield cls.randSlice(*args)
    else:
      for _ in range(N):
        yield cls.randSlice(*args)


class Freddy(metaclass=_FreddyMeta):
  """
  Freddy lets you generate slices with the indexing syntax.
  """
