"""SubclassException should be raised when a class is not a subclass of
the expected base class. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class SubclassException(TypeError):
  """SubclassException should be raised when a class is not a subclass of
  the expected base class."""

  def __init__(self, obj: object, expBase: type, ) -> None:
    """Initialize the exception with the object and expected base class."""
    if isinstance(obj, type):
      cls = obj
      infoSpec = """Expected subclass of '%s', but received '%s%s' having 
      the following method resolution order: <br><tab>%s"""
      objStr = ''
    else:
      cls = type(obj)
      infoSpec = """Expected object of a subclass of '%s', but received
      object: '%s' of type: '%s' having the following method resolution
      order: <br><tab>%s"""
      objStr = str(obj)
    expName = expBase.__name__
    clsName = cls.__name__
    clsMRO = cls.__mro__
    mroStr = '<br><tab>'.join([base.__name__ for base in clsMRO])
    info = infoSpec % (expName, objStr, clsName, mroStr)
    TypeError.__init__(self, info)
