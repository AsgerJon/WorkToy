"""'EZMeta' is the metaclass for 'EZData' and its subclasses."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..mcls import Base, BaseMeta
from ..waitaminute.ez import EZMultipleInheritance
from ._ez_space import EZSpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class EZMeta(BaseMeta):
  """Metaclass for 'EZData'; constructs an 'EZSpace' namespace."""

  @classmethod
  def __prepare__(
      mcls, name: str, bases: Base, **kwargs,
  ) -> EZSpace:
    """Build the 'EZSpace' namespace for the class body."""
    return EZSpace(mcls, name, bases, **kwargs)

  def __new__(
      mcls, name: str, bases: Base, space: EZSpace, **kwargs
  ) -> Any:
    """Translate CPython's layout-conflict 'TypeError' into the typed
    'EZMultipleInheritance' so users see what actually went wrong."""
    try:
      return BaseMeta.__new__(mcls, name, bases, space, **kwargs)
    except TypeError as typeError:
      msg = str(typeError)
      if 'multiple bases have instance lay-out conflict' in msg:
        raise EZMultipleInheritance(name, *bases) from typeError
      raise
