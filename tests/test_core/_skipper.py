"""
Skipper is a descriptor that ends a redundant write with 'SkipSet'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object
from worktoy.core.control_flow import SkipSet

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Skipper(Object):
  """
  A write of the value a descriptor already holds has nothing to do, and
  'hookPreSet' may end it silently with 'SkipSet', after which neither
  '__instance_set__' nor 'hookOnSet' runs. 'Skipper' does exactly that,
  and records every write that went through in the 'log' list of the
  instance.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kw) -> Any:
    return instance.__dict__.get(self.getPrivateName(), None)

  def __instance_set__(self, instance: Any, value: Any, **kw) -> None:
    instance.__dict__[self.getPrivateName()] = value
    instance.log.append(('set', value))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def hookPreSet(self, instance: Any, value: Any, **kw) -> None:
    if instance.__dict__.get(self.getPrivateName(), None) == value:
      raise SkipSet

  def hookOnSet(self, instance: Any, value: Any, **kw) -> None:
    instance.log.append(('onSet', value))
