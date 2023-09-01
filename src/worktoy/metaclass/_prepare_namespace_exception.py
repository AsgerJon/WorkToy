"""WorkToy - Wait A Minute! - PrepareNameSpaceException
This exception refers to unexpected behaviour from namespaces returned by
custom implementation of __prepare__ in a metaclass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MetaXcept


class PrepareNameSpaceException(MetaXcept):
  """WorkToy - Wait A Minute! - PrepareNameSpaceException
  This exception refers to unexpected behaviour from namespaces returned by
  custom implementation of __prepare__ in a metaclass."""

  _requiredMethods = ['__getitem__', '__setitem__', '__contains__']

  @classmethod
  def missingMethods(cls,
                     obj: object, *missingMethods,
                     ) -> PrepareNameSpaceException:
    """Version raised when a required method is missing."""
    m = """Custom classes used by the __prepare__ method must support 
    the following methods: <br>%s""" % ('<br>'.join(cls._requiredMethods))
    b = """But object %s is missing: <br>%s<br>"""
    nameSpaceObject = str(obj)
    if len(nameSpaceObject) > 77:
      nameSpaceObject = nameSpaceObject[:77]
    body = b % (nameSpaceObject, '<br>'.join(missingMethods))
    msg = '%s<br>%s' % (m, body)
    out = cls(msg)
    if isinstance(out, PrepareNameSpaceException):
      return out

  def __init__(self, msg: str, *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._msg = msg

  def __str__(self) -> str:
    return self._msg
