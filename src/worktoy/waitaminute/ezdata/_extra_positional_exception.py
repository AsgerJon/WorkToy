"""
ExtraPositionalException is raised when an EZData subclass receives more
positional arguments than it has fields.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from ...utilities import textFmt, NoPickle


class ExtraPositionalException(NoPickle, TypeError):
  """
  Raised when an EZData subclass receives more positional arguments
  than it has fields. Its keyword counterpart is
  'ExtraKeywordException', raised for a keyword argument that names none
  of the fields.

  Attributes
  ----------
  cls: type
    The class that received the extra positional arguments.
  fieldCount: int
    The number of fields declared in the class.
  argCount: int
    The number of positional arguments received by the class.
  """

  __slots__ = ('cls', 'fieldCount', 'argCount')

  def __init__(self, *args) -> None:
    cls, nFields, nArgs, *_ = [*args, None, None, None]
    self.cls = cls
    self.fieldCount = nFields
    self.argCount = nArgs
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """EZData subclass '%s' has %d %s but received %d
    positional %s. """
    fields = 'field' if self.fieldCount == 1 else 'fields'
    arguments = 'argument' if self.argCount == 1 else 'arguments'
    clsName = self.cls.__name__
    counts = (self.fieldCount, fields, self.argCount, arguments)
    info = infoSpec % (clsName, *counts)
    return textFmt(info, )

  __repr__ = __str__
