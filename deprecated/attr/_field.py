"""Field subclasses AbstractField and implements decorators for setting
the accessor methods. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.attr import AbstractField

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Callable


class Field(AbstractField):
  """Field subclasses AbstractField and implements decorators for setting
  the accessor methods. """

  def GET(self, callMeMaybe: Callable) -> Callable:
    """The GET decorator sets the getter method for the field."""
    self.setGetterKey(callMeMaybe.__name__)
    return callMeMaybe

  def SET(self, callMeMaybe: Callable) -> Callable:
    """The SET decorator sets the setter method for the field."""
    self.appendSetterKey(callMeMaybe.__name__)
    return callMeMaybe

  def DELETE(self, callMeMaybe: Callable) -> Callable:
    """The DELETE decorator sets the deleter method for the field."""
    self.appendDeleterKey(callMeMaybe.__name__)
    return callMeMaybe
