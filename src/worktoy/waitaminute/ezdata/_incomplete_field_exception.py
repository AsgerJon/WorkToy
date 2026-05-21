"""
IncompleteFieldException is raised at class construction time when an
EZData subclass body contains an EZField that is missing either its
type or its construction arguments.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  pass


class IncompleteFieldException(TypeError):
  """
  IncompleteFieldException is raised at class construction time when
  an EZData subclass body contains an EZField that is missing either
  its type or its construction arguments. The most common shapes
  that produce this state are 'EZField(value)' without a type
  subscript and 'EZField[T]' without trailing parentheses; both
  compile as valid Python but produce a field that cannot supply a
  default value.

  Attributes
  ----------
  clsName : str
    The name of the EZData subclass under construction.
  fieldName : str
    The name of the offending field in the class body.
  missing : str
    A short description of what is missing from the field, such as
    'the field type' or 'the construction arguments'.
  """

  __slots__ = ('clsName', 'fieldName', 'missing')

  def __init__(self, *args) -> None:
    clsName, fieldName, missing, *_ = [*args, None, None, None]
    self.clsName = clsName
    self.fieldName = fieldName
    self.missing = missing
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """EZData subclass '%s' has incomplete field '%s':
    %s. Use 'EZField[T](...)' to declare both the type and the
    construction arguments. """
    info = infoSpec % (self.clsName, self.fieldName, self.missing)
    return textFmt(info, )

  __repr__ = __str__
