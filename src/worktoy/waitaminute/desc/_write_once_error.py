"""WriteOnceError is a custom error class raised to indicate that a
variable was attempted to be written to more than once."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class WriteOnceError(TypeError):
  """
  WriteOnceError is raised on a second write to a write-once attribute,
  such as a 'FixBox' field that already holds a value or a 'Permuter'
  whose 'Arrangement' is already set. It subclasses 'TypeError'.

  Attributes
  ----------
  desc : object
    The write-once descriptor that rejected the second write.
  oldValue : Any
    The value already stored.
  newValue : Any
    The value whose assignment was rejected.
  """

  __slots__ = ('desc', 'oldValue', 'newValue')

  def __init__(self, desc: object, oldVal: Any, newVal: Any) -> None:
    self.desc = desc
    self.oldValue = oldVal
    self.newValue = newVal
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """Attempted to overwrite write-once attribute at '%s.%s' 
    having existing value: '%s' with new value: '%s'!"""
    owner = getattr(self.desc, '__field_owner__', object())  # no __name__
    ownerName = getattr(owner, '__name__', 'Unknown')
    fieldName = getattr(self.desc, '__field_name__', 'Unknown')
    oldStr = str(self.oldValue)
    newStr = str(self.newValue)
    info = infoSpec % (ownerName, fieldName, oldStr, newStr)
    return textFmt(info)

  __repr__ = __str__
