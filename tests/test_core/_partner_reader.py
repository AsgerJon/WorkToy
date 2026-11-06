"""
PartnerReader is a descriptor whose 'hookOnGet' reads the same field on
the partner of the instance.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class PartnerReader(Object):
  """
  The lock on a read hook is per instance: a hook may read the same
  field of another instance, and only two instances reading each other
  run into the refusal. 'PartnerReader' reads the field of
  'instance.partner' from 'hookOnGet' when the instance has one, records
  every value it read in the 'seen' list of the instance, and then reads
  its own field as well when the instance is 'selfish', which the base
  must still refuse.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kw) -> Any:
    return instance.tag

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def hookOnGet(self, instance: Any, value: Any, **kw) -> None:
    if instance.partner is None:
      return
    instance.seen.append(getattr(instance.partner, self.getFieldName()))
    if instance.selfish:
      getattr(instance, self.getFieldName())
