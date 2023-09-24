"""WorkToy - Core - ShareAttribute 
Subclass of Attribute recording set events on objects exposing which
attributes on the object that has been specifically set to a value
different from the default."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.descriptors import Attribute


class ShareAttribute(Attribute):
  """Subclass of Attribute recording set events on objects exposing which 
  attributes on the object that has been specifically set to a value 
  different from the default."""

  def __init__(self, *args, **kwargs) -> None:
    Attribute.__init__(self, *args, **kwargs)

  def __set__(self, obj: Any, newValue: Any) -> None:
    """Reimplementation of setter. """
    name = '__specified_attributes__'
    existing = getattr(obj, name, [])
    setattr(obj, name, [*existing, self._getFieldName()])
    Attribute.__set__(self, obj, newValue)

