"""
Noisy is a descriptor that records every hook call and reports the value
it stored.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object
from worktoy.core.sentinels import DELETED

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Noisy(Object):
  """
  The tests of the 'Object' protocol need to see which hooks ran, in
  what order, with what, and what '__instance_set__' can report back.
  'Noisy' appends one entry per hook to the 'log' list of the instance,
  stores the text of every value written and returns that text, so
  'hookOnSet' is seen to receive the value as stored rather than as
  assigned. A read of a slot never written raises 'AttributeError', so a
  deletion of such a slot is seen to receive 'None' as the old value.
  Placement is recorded on the class in 'placements'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  placements: list = []

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kw) -> Any:
    instance.log.append(('get', dict(kw)))
    try:
      return instance.__dict__[self.getPrivateName()]
    except KeyError as keyError:
      raise AttributeError(self.getFieldName()) from keyError

  def __instance_set__(self, instance: Any, value: Any, **kw) -> Any:
    stored = str(value)
    instance.__dict__[self.getPrivateName()] = stored
    instance.log.append(('set', stored))
    return stored

  def __instance_delete__(
      self, instance: Any, old: Any = None, **kw) -> None:
    instance.__dict__[self.getPrivateName()] = DELETED
    instance.log.append(('delete', old))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def hookPreGet(self, instance: Any, **kw) -> None:
    instance.log.append(('preGet', self.instance is instance))

  def hookOnGet(self, instance: Any, value: Any, **kw) -> None:
    instance.log.append(('onGet', value))

  def hookPreSet(self, instance: Any, value: Any, **kw) -> None:
    instance.log.append(('preSet', value))

  def hookOnSet(self, instance: Any, value: Any, **kw) -> None:
    instance.log.append(('onSet', value))

  def hookPreDelete(self, instance: Any, **kw) -> None:
    instance.log.append(('preDelete', self.owner))

  def hookOnDelete(self, instance: Any, **kw) -> None:
    instance.log.append(('onDelete', None))

  def hookSetName(self, owner: type, name: str, **kw) -> None:
    Noisy.placements.append((owner.__name__, name))
