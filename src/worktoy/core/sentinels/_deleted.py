"""
DELETED is the sentinel a descriptor stores in place of a value to mark
that value as deleted.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import Sentinel


class DELETED(Sentinel):
  """
  A box keeps the value of each instance in a slot, and builds its
  default into an empty slot at the first read. Deleting the attribute
  therefore cannot simply empty the slot: the next read would build the
  default again, and the deletion would leave no trace. The box needs a
  value to leave in the slot that means deleted, which no real value can
  be mistaken for and which the read recognizes. A descriptor a project
  writes on 'Object' needs the same.

  Implementation
  --------------

  'DELETED' is that value. When '__instance_get__' returns it,
  'Object.__get__' raises 'MissingVariable', an 'AttributeError', as for
  a deleted plain attribute, and 'Object.__delete__' raises it for a
  second deletion.
  """
  pass
