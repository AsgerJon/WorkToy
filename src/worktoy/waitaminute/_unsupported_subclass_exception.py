"""WorkToy - Wait A Minute! - UnsupportedSubclassException
This exception should be raised when encountering a variable of correct
type, but of incorrect subclass."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MetaXcept


class UnsupportedSubclassException(MetaXcept):
  """WorkToy - Wait A Minute! - UnsupportedSubclassException
  This exception should be raised when encountering a variable of correct
  type, but of incorrect subclass."""

  def __init__(self, name: str, exp: type, obj: object,
               *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._actualName = self.pretty(name)
    self._expectedParent = self.pretty(exp)
    self._actualVariable = self.pretty(obj)

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    name = self._actualName
    exp = self._expectedParent
    obj = self._actualVariable
    msg = """Expected argument: '%s' to be an instance of a subclass of 
    '%s', but received '%s' of type: '%s' having the following 
    incompatible method resolution order:"""
    body = self.monoSpace(msg % (name, exp, obj, type(obj)))
    _mro = [arg for arg in type(obj).__mro__()]
    _mro = [self.pretty(arg) for arg in _mro]
    _mro = '<br>  '.join(_mro)
    body = '%s<br>%s' % (body, _mro)
    return '%s\n%s' % (header, self.justify(body))
