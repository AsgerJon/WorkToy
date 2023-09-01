"""WorkToy - Wait A Minute! - DisabledFunctionError
When a child class disables a method inherited, this error is invoked if
the method is attempted to be in invoked on the child"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MetaXcept


class DisabledFunctionError(MetaXcept):
  """WorkToy - Wait A Minute! - DisabledFunctionError
  Raised if attempting to invoke a disabled method. For example,
  if a subclass has disabled a parent class method."""

  def __init__(self,
               parentClass: type,
               childClass: type, *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._parentClass = parentClass
    self._childClass = childClass

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    parent = self._parentClass.__qualname__
    child = self._childClass.__qualname__
    msg = """The function '%s' defined on class '%s' is disabled on 
    subclass: '%s'!""" % (self.getSourceFunctionName(), parent, child)
    return '%s\n%s' % (header, self.justify(msg))
