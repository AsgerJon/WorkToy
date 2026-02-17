"""
KeeBoxValueError is a custom exception class raised to indicate that a
value specified in the positional arguments of a 'KeeBox' object does
match a valid object of the value type of the given enumeration type.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class KeeBoxValueError(ValueError):
  """
  KeeBoxValueError is a custom exception class raised to indicate that a
  value specified in the positional arguments of a 'KeeBox' object does
  match a valid object of the value type of the given enumeration type.
  """

  __slots__ = ('desc', 'num', 'value')

  def __init__(self, *args) -> None:
    self.desc, self.num, self.value, *_ = (*args, None, None, None)
    ValueError.__init__(self, )

  def __str__(self, ) -> str:
    infoSpec = """The '%s' descriptor with field enumeration: '%s', 
    having value type: '%s', received value of correct type: '%s', 
    which does not match the 'value' of any member of the '%s' 
    enumeration!"""
    descSpec = """%s.%s: %s"""
    ownerName = getattr(self.desc, '__field_owner__', ).__name__
    fieldName = getattr(self.desc, '__field_name__', )
    fieldType = str(getattr(self.desc, '__field_type__', ))
    desc = descSpec % (ownerName, fieldName, fieldType)
    num = str(self.num)
    valueType = str(type(self.value))
    info = infoSpec % (desc, num, valueType, repr(self.value), fieldType)
    from ...utilities import textFmt
    return textFmt(info, )

  __repr__ = __str__
