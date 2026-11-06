"""
Quiet is a descriptor whose '__instance_set__' reports nothing back.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Quiet(Object):
  """
  A '__instance_set__' returning 'None' tells 'Object.__set__' that the
  value was stored as assigned, and 'hookOnSet' then receives the value
  assigned. 'Quiet' stores the value under the private name of its field
  and returns nothing, recording in the 'log' list of the instance what
  'hookOnSet' received and the frame it ran in.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kw) -> Any:
    return instance.__dict__.get(self.getPrivateName(), None)

  def __instance_set__(self, instance: Any, value: Any, **kw) -> None:
    instance.__dict__[self.getPrivateName()] = value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def hookOnSet(self, instance: Any, value: Any, **kw) -> None:
    sameInstance = self.instance is instance
    instance.log.append(('onSet', value, sameInstance, self.owner))
