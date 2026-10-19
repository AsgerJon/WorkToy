"""
NamelessCallback is raised when a callback decorator of a descriptor
receives a function without a name of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class NamelessCallback(WorkToyException, SyntaxError):
  """
  NamelessCallback is raised when a callback decorator of a descriptor,
  one of the notification decorators of 'BaseDescriptor' or the accessor
  decorators of 'Field', receives a function without a name of its own:
  a lambda, whose name is '<lambda>', or a callable with no '__name__'
  at all, such as a 'functools.partial'. The descriptor records only the
  name, and looks the callback up by it on the class of the instance at
  each access, so a subclass can override it by redefining the name. A
  nameless function could never be found that way, and the first access
  used to fail with 'MissingVariable' naming '<lambda>'. The class body
  fails at the decorator instead. It subclasses 'SyntaxError', as the
  other refusals of a class-body line do.

  Attributes
  ----------
  desc : Any
    The descriptor whose decorator refused the callback.
  role : str
    The name of the decorator, such as 'onSet' or 'GET'.
  callback : Any
    The callback that was refused.
  """

  __slots__ = ('desc', 'role', 'callback')

  def __init__(self, desc: Any, role: str, callback: Any) -> None:
    self.desc = desc
    self.role = role
    self.callback = callback
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    spec = """The '%s' decorator of the '%s' descriptor received '%s',
    which has no name of its own. A callback is looked up by name on the
    class of the instance, so it must be defined with 'def' under the
    name it is to be found by."""
    descName = type(self.desc).__name__
    callbackName = getattr(self.callback, '__name__', None)
    callbackStr = callbackName or repr(self.callback)
    return textFmt(spec % (self.role, descName, callbackStr))

  __repr__ = __str__
