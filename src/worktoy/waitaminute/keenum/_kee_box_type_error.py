"""
KeeBoxTypeError is raised when a 'KeeBox' cannot resolve its arguments to
the value type of its enumeration.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover

  from ...keenum import KeeBox


class KeeBoxTypeError(TypeError):
  """
  KeeBoxTypeError is a custom exception class raised to indicate that a
  given 'KeeBox' descriptor could not resolve given arguments to member of
  the value type of the field enumeration of the descriptor.

  Attributes
  ----------
  box : KeeBox
    The 'KeeBox' descriptor that failed to resolve.
  posArgs : tuple
    The arguments that failed to resolve to the value type.
  """

  __slots__ = ('box', 'posArgs')

  def __init__(self, box: KeeBox, *args) -> None:
    self.box, self.posArgs = box, args
    TypeError.__init__(self, )

  def __str__(self, ) -> str:
    infoSpec = """The '%s' descriptor with field enumeration: '%s' having 
    value type: '%s' could not be instantiated with the given arguments: 
    <br><tab>%s<br>"""
    descSpec = """%s.%s: %s"""
    ownerName = getattr(self.box, '__field_owner__', ).__name__
    fieldName = getattr(self.box, '__field_name__', )
    fieldType = str(getattr(self.box, '__field_type__', ))
    desc = descSpec % (ownerName, fieldName, fieldType)
    num = str(self.box.fieldType)
    valueType = str(self.box.fieldType.valueType)
    argSpec = """<%s: %s>"""
    argTypes = (*(type(arg).__name__ for arg in self.posArgs),)
    argStrs = (*(repr(arg) for arg in self.posArgs),)
    argInfos = (*(argSpec % (t, s) for s, t in zip(argStrs, argTypes)),)
    argInfo = '<br><tab>'.join(argInfos)
    info = infoSpec % (desc, num, valueType, argInfo)
    from ...utilities import textFmt
    return textFmt(info, )

  __repr__ = __str__
