"""
InstanceException is a custom exception raised when a descriptor may be
accessed only through the owning class, but where __get__ receives as
instance argument something other than None.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..text import joinWords, monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any

  from ..attr import _FieldProperties as Desc


class InstanceException(ValueError):
  """
  InstanceException is a custom exception raised when a descriptor may be
  accessed only through the owning class, but where __get__ receives as
  instance argument something other than None.
  """

  descObject = _Attribute()
  descType = _Attribute()
  instance = _Attribute()
  owner = _Attribute()
  fieldName = _Attribute()

  def __init__(self, desc: Desc, ins: Any, ) -> None:
    """Initialize the InstanceException object."""
    self.descObject = desc
    self.descType = type(desc)
    self.instance = ins
    self.owner = type(ins)
    self.fieldName = desc.__field_name__
    infoSpec = """
    '%s' objects may only be accessed through the owning class, 
    not through instances!
    """
    info = monoSpace(infoSpec % (type(desc).__name__,))
    ValueError.__init__(self, info)

  def __eq__(self, other: Any) -> bool:
    """Compare the InstanceException object with another object."""
    cls = type(self)
    if not isinstance(other, cls):
      return False
    if other is self:
      return True
    if self.owner is not other.owner:
      return False
    if self.fieldName != other.fieldName:
      return False
    return True
