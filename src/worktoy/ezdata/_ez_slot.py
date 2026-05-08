"""``EZSlot`` carries the per-field metadata for an EZData class:
its name, declared type, default value, and the name of the class
that owns it. It is constructed with just a name; the type and
default are populated later by the namespace hook."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class EZSlot:
  """Metadata for a single data field of an ``EZData`` class.

  Attributes
  ----------
  name : str
      The field's identifier in the class body.
  typeValue : type
      The declared field type, or ``None`` if no type has been
      assigned yet.
  defaultValue : Any
      The class-body default, or ``None`` if no default has been
      assigned yet.
  ownerName : str
      The name of the ``EZData`` subclass that owns this slot.

  The legacy private dunder names ``__future_name__``,
  ``__type_value__``, ``__default_value__``, and ``__owner_name__``
  are accepted by ``setattr`` and read by the public properties.
  """

  __slots__ = (
      '__future_name__',
      '__type_value__',
      '__default_value__',
      '__owner_name__',
  )

  def __init__(self, name: str) -> None:
    object.__setattr__(self, '__future_name__', name)
    object.__setattr__(self, '__type_value__', None)
    object.__setattr__(self, '__default_value__', None)
    object.__setattr__(self, '__owner_name__', '')

  @property
  def name(self) -> str:
    """Return the field's identifier."""
    return self.__future_name__

  @property
  def typeValue(self) -> type:
    """Return the declared field type."""
    return self.__type_value__

  @property
  def defaultValue(self) -> Any:
    """Return the class-body default value."""
    return self.__default_value__

  @property
  def ownerName(self) -> str:
    """Return the owning class's name."""
    return self.__owner_name__

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, EZSlot):
      return self.__future_name__ == other.__future_name__
    return NotImplemented

  def __hash__(self) -> int:
    return hash(('EZSlot', self.__future_name__))

  def __str__(self) -> str:
    typeName = (self.__type_value__.__name__
                if self.__type_value__ is not None else '?')
    val = self.__default_value__
    if val is None:
      val = '[NONE]'
    return '%s<%s.%s>(%s: %s)' % (
        type(self).__name__, self.__owner_name__,
        self.__future_name__, typeName, val,
    )

  def __repr__(self) -> str:
    return self.__str__()
