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

from worktoy.parse import maybe

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Self


class ProtectedError(TypeError, AttributeError):
  """ProtectedError is raised to indicate an attempt to delete a protected
  object. For example, a descriptor class could implement the '__delete__'
  method to always raise this exception. This provides a more detailed
  error. Particularly because both TypeError and AttributeError are being
  suggested by large language models. Neither of which is wrong, but lacks
  the specificity of this exception."""

  def __init__(self, *args, **kwargs) -> None:
    descKwarg = kwargs.get('desc', None)
    insKwarg = kwargs.get('instance', None)
    valKwarg = kwargs.get('value', None)
    descArg, insArg, valArg = [*args, None, None, None][:3]
    desc = maybe(descKwarg, descArg)
    ins = maybe(insKwarg, insArg)
    val = maybe(valKwarg, valArg)
    if desc is None or ins is None:
      super().__init__(*args, **kwargs)
    elif val is None:
      infoSpec = """Attempted to delete '%s.%s' from instance: '%s'! This 
      descriptor is of type: '%s' and is protected from deletion!"""
      ownerName = type(ins).__name__
      fieldName = getattr(desc, '__field_name__', type(desc).__name__)
      descTypeName = type(desc).__name__
      insStr = repr(ins)
      info = infoSpec % (ownerName, fieldName, insStr, descTypeName)
      super().__init__(info)
    else:
      infoSpec = """Attempted to delete value: '%s' at '%s.%s' from
      instance: '%s'! This descriptor is of type: '%s' and is protected
      from deletion!"""
      valStr = repr(val)
      ownerName = type(ins).__name__
      fieldName = getattr(desc, '__field_name__', type(desc).__name__)
      descTypeName = type(desc).__name__
      insStr = repr(ins)
      info = infoSpec % (valStr, ownerName, fieldName, insStr, descTypeName)
      super().__init__(info)
