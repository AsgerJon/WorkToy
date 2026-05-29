"""
ExtraPositionalException is raised when an EZData subclass receives more
positional arguments than it has fields.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  pass


class ExtraPositionalException(TypeError):
  """
  Raised when an EZData subclass receives more positional arguments
  than it has fields. Unknown keyword arguments are silently ignored
  to support orthogonal kwarg injection, but extra positional
  arguments almost always indicate a caller mistake.

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
    infoSpec = """EZData subclass '%s' has %d fields but received %d
    positional arguments. """
    info = infoSpec % (self.cls.__name__, self.fieldCount, self.argCount)
    return textFmt(info, )

  __repr__ = __str__
