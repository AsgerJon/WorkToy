"""
UnboundCastHook is raised when a class defines '__cast_as__' without the
'@classmethod' decorator.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from .. import WorkToyException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Optional


class UnboundCastHook(WorkToyException, SyntaxError):
  """
  UnboundCastHook is raised when 'typeCast' finds a '__cast_as__' that is
  not a classmethod on the class it is casting to, or on a base of it.
  'typeCast' calls the hook on the class to make an instance, so a plain
  function would run with the value bound as 'self', and a staticmethod
  could not build a subclass. The refusal is raised at the cast, the
  first moment the hook is used, and it is no 'TypeError', so the cast
  passes of an overloaded method do not read it as a signature that
  merely failed to match. It subclasses 'SyntaxError', as the other
  refusals of a class-body line do.

  Attributes
  ----------
  className : str
    The name of the class whose body defines the hook.
  targetName : str or None
    The name of the class being cast to, when it inherits the hook from
    'className' rather than defining it itself.
  """

  __slots__ = ('className', 'targetName')

  def __init__(
      self,
      className: str,
      targetName: Optional[str] = None
      ) -> None:
    self.className = className
    if targetName == className:
      targetName = None
    self.targetName = targetName
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    spec = """The class '%s' defines '__cast_as__' without the
    '@classmethod' decorator! 'typeCast' calls the hook on the class to
    make an instance, so the definition requires it."""
    info = spec % self.className
    if self.targetName is not None:
      info = """%s The class '%s' inherits it.""" % (info, self.targetName)
    return textFmt(info)

  __repr__ = __str__
