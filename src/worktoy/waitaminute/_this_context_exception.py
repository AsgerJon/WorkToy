"""THISContextException is a custom exception raised to indicate a disallowed
use of the 'THIS' token object. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..text import joinWords, monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any, Callable

  from ..attr import AbstractDescriptor as Desc


class THISContextException(ValueError):
  """THISContextException is a custom exception raised to indicate a
  disallowed use of the 'THIS' token object. """

  context = _Attribute()

  def __init__(self, context: Callable) -> None:
    """Initialize the THISContextException object."""
    self.context = context
    infoSpec = """In the context of '%s', the THIS token object is not 
    supported!"""
    if hasattr(context, '__qualname__'):
      info = monoSpace(infoSpec % (context.__qualname__,))
    else:
      info = monoSpace(infoSpec % (context.__name__,))
    ValueError.__init__(self, info)

  def __eq__(self, other: Any) -> bool:
    """Compare the THISContextException object with another object."""
    cls = type(self)
    if not isinstance(other, cls):
      return False
    if other is self:
      return True
    if other.context != self.context:
      return False
    return True
