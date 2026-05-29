"""
THIS is a sentinel placeholder for the enclosing class, resolved
contextually by the descriptor flow.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import Sentinel

if TYPE_CHECKING:  # pragma: no cover
  pass


class THIS(Sentinel):
  """
  THIS is a sentinel placeholder for the enclosing class, used inside
  a class body before that class exists.

  In a deferred 'AttriBox' constructor argument, THIS is replaced at
  access time by the 'instance' passed to '__get__' (the object the
  attribute is read from). In an '@overload(...)' signature it stands
  for the enclosing class, so the overload matches instances of that
  class, analogous to 'typing.Self'.

  Use 'OWNER' for the 'owner' class passed to '__get__'; OWNER has no
  role in overload signatures.
  """
