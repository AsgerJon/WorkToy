"""
TypeCastException is raised by the 'typeCast' function in the
'worktoy.utilities' module when a value cannot be cast to the target type
without loss. It also surfaces wherever 'typeCast' backs another feature,
such as the SLOW tier of the overload dispatcher and 'AttriBox'
assignment.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TypeCastException(TypeError):
  """
  TypeCastException is raised by the 'typeCast' function in the
  'worktoy.utilities' module when a value cannot be cast to the target
  type without loss.

  Attributes
  ----------
  type_ : type
    The target type the cast was attempting to reach.
  arg : Any
    The value that could not be cast.
  """

  __slots__ = ('type_', 'arg')

  def __init__(self, type_: type, arg: Any) -> None:
    self.type_ = type_
    self.arg = arg
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """Unable to cast value '%s' to type '%s'!"""
    typeStr = self.type_.__name__
    argStr = str(self.arg)
    info = infoSpec % (argStr, typeStr)
    from ...utilities import textFmt
    return textFmt(info)

  __repr__ = __str__
