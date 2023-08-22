"""WorkToy - MetaAttribute
This is the metaclass used by the BaseAttribute and AbstractAttribute
classes. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import AbstractMetaType, Method


class MetaAttribute(AbstractMetaType):
  """WorkToy - MetaAttribute
  This is the metaclass used by the BaseAttribute and AbstractAttribute
  classes. """

  def __instancecheck__(cls, obj: object) -> bool:
    """A class created with this metaclass, which supports a particular
    type, will recognize instances of that type as instances of itself.
    Actual instances of the Attribute class are also recognized if they
    are instances of the attribute class or of a subclass of the attribute
    class."""
    if isinstance(obj, cls):
      return True
    typeCheck = getattr(cls, '_typeCheck', None)
    if not isinstance(typeCheck, Method):
      return False
    return True if typeCheck(cls, obj) else False
