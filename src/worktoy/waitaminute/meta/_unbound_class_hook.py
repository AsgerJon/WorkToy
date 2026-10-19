"""
UnboundClassHook is raised when a class body binds a routed
'__class_*__' hook name to a function that is not a classmethod.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Optional


class UnboundClassHook(WorkToyException, SyntaxError):
  """
  UnboundClassHook is raised when a class body binds one of the routed
  '__class_*__' hook names to a plain function or a staticmethod. The
  metaclass invokes these hooks as bound classmethods, so a definition
  without '@classmethod' receives no class binding: most hooks then
  fail with a confusing 'TypeError' at call time, and '__class_call__'
  silently swallows the first constructor argument as the class. This
  exception flags the mistake loudly at the class-body line instead.
  A hook inherited from a plain base, one no worktoy metaclass built and
  so never checked, is held to the same rule as the class is created, and
  the message then names that base. It subclasses 'SyntaxError'.

  Attributes
  ----------
  className : str
    The name of the class under construction.
  hookName : str
    The routed hook name bound to a plain function or a staticmethod.
  baseName : str or None
    The name of the base the hook is inherited from, or None when the
    class body binds it itself.
  """

  __slots__ = ('className', 'hookName', 'baseName',)

  def __init__(
      self,
      className: str,
      hookName: str,
      baseName: Optional[str] = None,
  ) -> None:
    self.className = className
    self.hookName = hookName
    self.baseName = baseName
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    if self.baseName is None:
      spec = """The class body of '%s' binds '%s' to a function without
      the '@classmethod' decorator! The metaclass invokes the class hooks
      as bound classmethods, so the definition requires it."""
      info = spec % (self.className, self.hookName)
      return textFmt(info)
    spec = """The class '%s' inherits '%s' from its base '%s', where it
    is a function without the '@classmethod' decorator! The metaclass
    invokes the class hooks as bound classmethods, so the definition
    requires it."""
    info = spec % (self.className, self.hookName, self.baseName)
    return textFmt(info)

  __repr__ = __str__
