"""
UnboundClassHook is raised when a class body binds a routed
'__class_*__' hook name to a plain function instead of a classmethod.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt


class UnboundClassHook(SyntaxError):
  """
  UnboundClassHook is raised when a class body binds one of the routed
  '__class_*__' hook names to a plain function or a staticmethod. The
  metaclass invokes these hooks as bound classmethods, so a definition
  without '@classmethod' receives no class binding: most hooks then
  fail with a confusing 'TypeError' at call time, and '__class_call__'
  silently swallows the first constructor argument as the class. This
  exception flags the mistake loudly at the class-body line instead.
  It subclasses 'SyntaxError'.

  Attributes
  ----------
  className : str
    The name of the class under construction.
  hookName : str
    The routed hook name bound to a plain function.
  """

  __slots__ = ('className', 'hookName',)

  def __init__(self, className: str, hookName: str, ) -> None:
    self.className = className
    self.hookName = hookName
    SyntaxError.__init__(self, )

  def __str__(self) -> str:
    spec = """The class body of '%s' binds '%s' to a plain function!
    The metaclass invokes the class hooks as bound classmethods, so
    the definition requires the '@classmethod' decorator."""
    info = spec % (self.className, self.hookName)
    return textFmt(info)

  __repr__ = __str__
