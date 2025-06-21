"""
SpyHook is a diagnostic hook used to track namespace activity during
class construction. It logs all invocations of the four standard hook
methods defined by AbstractHook:

- setItemHook: triggered on assignment
- getItemHook: triggered on access
- preCompileHook: triggered before namespace compilation
- postCompileHook: triggered after namespace compilation

This hook is useful for verifying hook ordering, correctness, and
namespace behavior in unit tests.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func

from worktoy.attr import Field
from worktoy.mcls.hooks import AbstractHook
from worktoy.parse import maybe

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, TypeAlias, Never

  Event: TypeAlias = tuple[str, str, Any]
  Events: TypeAlias = list[Event]


class SpyHook(AbstractHook):
  """Diagnostic hook that logs all hook events."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __accessor_events__ = None

  #  Public Variables
  events = Field()

  #  Virtual Variables
  addEvent = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @events.GET
  def _getAccessorEvents(self) -> Events:
    """Get the list of events recorded by this hook."""
    return maybe(self.__accessor_events__, [])

  @addEvent.GET
  def _getAddEvent(self) -> Func:
    """
    This virtual field returns a callback function when 'accessed'.
    """

    def callMeMaybe(event: Event) -> Never:
      """
      Callback function returned from the 'addEvent' virtual field.
      """
      self._addAccessorEvent(event)

    return callMeMaybe  # NOQA! pycharm, please!

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  @addEvent.SET
  def _addAccessorEvent(self, event: Event) -> None:
    """Add an event to the list of recorded events."""
    existingEvents = self._getAccessorEvents()
    self.__accessor_events__ = [*existingEvents, event]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemHook(self, key: str, val: Any, old: Any) -> bool:
    self.addEvent(('set', key, val))
    return False

  def getItemHook(self, key: str, val: Any) -> bool:
    self.addEvent(('get', key, val))
    return False

  def preCompileHook(self, space: dict) -> dict:
    self.addEvent(('pre', dict(space), dict(space)))
    return space

  def postCompileHook(self, space: dict) -> dict:
    self.addEvent(('post', dict(space), dict(space)))
    return space
