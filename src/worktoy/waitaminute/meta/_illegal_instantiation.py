"""
IllegalInstantiation is raised when a class is instantiated under
conditions that forbid it.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt


class IllegalInstantiation(TypeError):
  """
  IllegalInstantiation is raised when a class is instantiated under
  conditions that forbid it, such as calling a 'Sentinel' subclass (meant
  to be used as a singleton type, never instantiated) or the
  un-instantiable 'ValidSlice' validator. It subclasses 'TypeError'.

  Attributes
  ----------
  cls : type
    The class whose illegal instantiation was attempted.
  """

  __slots__ = ('cls',)

  def __init__(self, cls_: type) -> None:
    self.cls = cls_
    TypeError.__init__(self, )

  def __str__(self, ) -> str:
    clsName = self.cls.__name__
    infoSpec = """Illegal instantiation of class '%s'"""
    info = infoSpec % clsName
    return textFmt(info)

  __repr__ = __str__
