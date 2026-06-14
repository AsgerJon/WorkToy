"""
KeeBoxValueError is raised when a 'KeeBox' value is of the right type but
matches no member of its enumeration.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations


class KeeBoxValueError(ValueError):
  """
  KeeBoxValueError is raised when a value given to a 'KeeBox' is of the
  enumeration's value type but does not equal the 'value' of any member of
  that enumeration.

  Attributes
  ----------
  desc : KeeBox
    The 'KeeBox' descriptor that failed to resolve the value.
  num : KeeMeta
    The enumeration the value was resolved against.
  value : Any
    The well-typed value that matched no member.
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
    owner = getattr(self.desc, '__field_owner__', object())  # no __name__
    ownerName = getattr(owner, '__name__', 'Unknown')
    fieldName = getattr(self.desc, '__field_name__', 'Unknown')
    fieldType = getattr(self.desc, '__field_type__', None)
    fieldTypeName = getattr(fieldType, '__name__', str(fieldType))
    desc = descSpec % (ownerName, fieldName, fieldTypeName)
    numName = getattr(self.num, '__name__', str(self.num))
    valueType = getattr(self.num, 'valueType', None)
    valueTypeName = getattr(valueType, '__name__', str(valueType))
    value = repr(self.value)
    info = infoSpec % (desc, numName, valueTypeName, value, numName)
    from ...utilities import textFmt
    return textFmt(info, )

  __repr__ = __str__
