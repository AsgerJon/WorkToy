"""WorkToy - Wait A Minute! - ProtectedAttributeError
Raised when the __deleter__ function is invoked on a protected attribute."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.waitaminute import MetaXcept


class ProtectedAttributeError(MetaXcept):
  """WorkToy - Wait A Minute! - ProtectedAttributeError
  Raised when the __deleter__ function is invoked on a protected
  attribute."""

  def __init__(self, attName: str, instance: Any, owner: type,
               *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._attributeName = attName
    self._instance = instance
    self._owner = owner

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    attName = self._attributeName
    insName = str(self._instance)
    clsName = self._owner.__class__.__qualname__
    body = """Attempted to erase protected attribute '%s' from instance: 
    '%s' belonging to class '%s'""" % (attName, insName, clsName)
    return '%s\n%s' % (header, self.justify(body))
