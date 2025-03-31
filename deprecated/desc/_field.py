"""Field class subclasses the 'AbstractDescriptor' and provides the owning
class with decorators for explicitly specifying the accessor methods. This
means that the owning class are free to customize accessor method for each
of their attributes. The GET, SET, DELETE and RESET decorators allow the
owning class to designate the methods responsible for accessor operations.
Besides these decorators, the Field class also inherits the notification
related decorators from the AbstractDescriptor class. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from depr.desc import BaseField

try:
  from typing import Callable, Any, TYPE_CHECKING
except ImportError:
  Callable = object
  Any = object
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from depr.meta import CallMeMaybe


class Field(BaseField):
  """Field provides a flexible implementation of the descriptor
  protocol allowing owning classes to decorate methods as accessor
  methods. """

  def GET(self, callMeMaybe: CallMeMaybe) -> CallMeMaybe:
    """Decorator for the getter-method."""
    self.setGetterKey(callMeMaybe.__name__)
    return callMeMaybe

  def SET(self, callMeMaybe: CallMeMaybe) -> CallMeMaybe:
    """Decorator for the setter-method."""
    self.appendSetterKey(callMeMaybe.__name__)
    return callMeMaybe

  def DELETE(self, callMeMaybe: CallMeMaybe) -> CallMeMaybe:
    """Decorator for the deleter-method."""
    self.appendDeleterKey(callMeMaybe.__name__)
    return callMeMaybe
