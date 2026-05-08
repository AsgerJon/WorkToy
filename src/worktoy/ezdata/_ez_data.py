"""The user-facing EZData base class.

Subclasses declare data fields as class-body attributes; the
EZMeta metaclass installs the standard dunder methods at
class-creation time, so authors do not write __init__, __eq__,
__repr__, etc. by hand."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..mcls import BaseObject
from ._ez_meta import EZMeta
from ._trust import trust

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator


class EZData(BaseObject, metaclass=EZMeta):
  """Auto-generating dataclass base.

  Field declarations are class-body attributes, with optional
  type annotations and default values. EZMeta installs init,
  equality, repr, str, iter, len, item access, attribute access,
  hash (when frozen), and ordering operators (when order=True).

  Class keyword arguments
  -----------------------
  frozen : bool, default False
      When True, post-construction writes raise FrozenEZException
      and instances become hashable.
  order : bool, default False
      When True, the comparison operators compare fields
      lexicographically. Defaults that do not support '<' raise
      UnorderedEZException at class creation.
  kw_only : bool, default False
      Reserved tag; not yet enforced.

  Example
  -------
  class Point(EZData):
    x: int = 0
    y: int = 0

  Point(3, 4) == Point(x=3, y=4)  # True
  """

  __slot_objects__ = ()

  @trust
  def __init__(self, *args, **kwargs) -> None:
    """Replaced by EZMeta; signature is generated per class."""

  @trust
  def __iter__(self) -> Iterator:
    """Replaced by EZMeta; yields field values."""

  @trust
  def __len__(self) -> int:
    """Replaced by EZMeta; returns the number of fields."""

  @trust
  def __getitem__(self, key: Any) -> Any:
    """Replaced by EZMeta."""

  @trust
  def __setitem__(self, key: Any, value: Any) -> None:
    """Replaced by EZMeta."""
