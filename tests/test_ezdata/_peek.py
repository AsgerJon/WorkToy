"""
Peek is a descriptor built on 'Object' the documented way.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Peek(Object):
  """
  Every 'Object' defines the descriptor protocol, so an 'Object' in a
  dataclass body is a descriptor only when its class overrides one of
  the six methods of that protocol. 'Peek' overrides '__instance_get__'
  and answers every read with the word 'peeked', so it stays a class
  attribute where a plain 'Object' would become a field.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> str:
    return 'peeked'
