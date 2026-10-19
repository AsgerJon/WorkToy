"""
ReservedName is raised when a class body reassigns a name reserved by the
interpreter or the metaclass system.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt
from .. import WorkToyException


class ReservedName(WorkToyException, SyntaxError):
  """
  ReservedName is raised when a class body assigns a name that the
  interpreter or the metaclass system reserves and populates automatically,
  such as '__dict__', '__module__', '__qualname__', or '__match_args__'.
  The guard fires only on reassignment, so deferred initialisation of such
  a name is still allowed. It subclasses 'SyntaxError', as the other
  refusals of a class-body line do.

  Attributes
  ----------
  resName : str
    The reserved name that the class body tried to set.
  """

  __slots__ = ('resName',)

  def __init__(self, name: str) -> None:
    self.resName = name
    SyntaxError.__init__(self, )
    #  The traceback of a 'SyntaxError' shows 'msg' rather than 'str()'.
    self.msg = str(self)

  def __str__(self) -> str:
    infoSpec = """Attempted to use reserved name: '%s'!"""
    info = infoSpec % self.resName
    return textFmt(info)

  __repr__ = __str__
