"""ProtectedError is raised to indicate an attempt to delete a protected
object. For example, a descriptor class could implement the '__delete__'
method to always raise this exception. This provides a more detailed
error. Particularly because both TypeError and AttributeError are being
suggested by large language models. Neither of which is wrong, but lacks
the specificity of this exception.

The ProtectedError class inherits from both TypeError and AttributeError,
ensuring that it is caught in exception clauses pertaining to either.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import _Attribute
from ..text import monoSpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class ProtectedError(TypeError):
  """ProtectedError is raised to indicate an attempt to delete a protected
  object. For example, a descriptor class could implement the '__delete__'
  method to always raise this exception. This provides a more detailed
  error. Particularly because both TypeError and AttributeError are being
  suggested by large language models. Neither of which is wrong, but lacks
  the specificity of this exception."""

  owningInstance = _Attribute()
  descriptorObject = _Attribute()
  existingValue = _Attribute()

  def __init__(self, instance: Any, desc: Any, oldValue: Any = None) -> None:
    """Initialize the ReadOnlyError."""
    self.owningInstance = instance
    self.descriptorObject = desc
    self.existingValue = oldValue
    TypeError.__init__(self, )

  def __str__(self, ) -> str:
    """
    Return the string representation of the ProtectedError.
    """
    oldValue = self.existingValue
    desc = self.descriptorObject
    fieldOwner = getattr(self.owningInstance, '__field_owner__', None)
    fieldName = getattr(desc, '__field_name__', None)
    infoSpec = """Attempted to delete protected attribute '%s.%s' 
      with value: '%s'"""
    info = infoSpec % (fieldOwner, fieldName, str(oldValue))
    return monoSpace(info)

  __repr__ = __str__
