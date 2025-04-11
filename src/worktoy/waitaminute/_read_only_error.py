"""ReadOnlyError is raised when an attempt is made to modify a read-only
attribute. This is a subclass of TypeError and should be used to indicate
that the attribute is read-only. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations


class ReadOnlyError(TypeError):
  """ReadOnlyError is raised when an attempt is made to modify a read-only
  attribute. This is a subclass of TypeError and should be used to indicate
  that the attribute is read-only. """

  def __init__(self, instance: object, desc: object, value: object) -> None:
    fieldName = getattr(desc, '__field_name__', None)
    if fieldName is None:
      TypeError.__init__(self, "Cannot modify read-only attribute.")
    else:
      owner = type(instance)
      ownerName = getattr(owner, '__name__', )
      cls = type(desc)
      clsName = getattr(cls, '__name__', )
      descName = '%s.%s' % (ownerName, fieldName)
      valueStr = repr(value)
      info = """Attempted to set value of read-only attribute: '%s' of 
      descriptor class: '%s' to: '%s'!""" % (descName, clsName, valueStr)
      TypeError.__init__(self, info)
