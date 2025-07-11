"""
DeferredTypeException is a custom exception class raised to indicate that
a slot was set as an annotation to a deferred type. This specifically
happens when 'from __future__ import annotations' is used allowing type
hinting to methods and classes not available at runtime. While this is
appropriate for methods which ignore type hints at runtime, slots in the
bodies of EZData subclasses actually require types to be available in the
scope containing the class definition.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  pass


class DeferredTypeException(TypeError):
  """
  DeferredTypeException is a custom exception class raised to indicate that
  a slot was set as an annotation to a deferred type. This specifically
  happens when 'from __future__ import annotations' is used allowing type
  hinting to methods and classes not available at runtime. While this is
  appropriate for methods which ignore type hints at runtime, slots in the
  bodies of EZData subclasses actually require types to be available in the
  scope containing the class definition.
  """

  __slots__ = ('fieldName', 'typeName')

  def __init__(self, fieldName: str, typeName: str) -> None:
    self.fieldName = fieldName
    self.typeName = typeName
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """Attempted to set slot '%s' with type: '%s', that could 
    not be resolved at class creation time. """
    info = infoSpec % (self.fieldName, self.typeName)
    return textFmt(info, )

  __repr__ = __str__
