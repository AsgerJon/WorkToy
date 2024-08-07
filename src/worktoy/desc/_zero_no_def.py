"""NODEF indicates that each instance owning an AttriBox must receive a
call to its __set__ to explicitly set a value, before it is allowed to
receive __get__ calls. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import Zeroton


class NODEF(Zeroton):
  """NODEF indicates that each instance owning an AttriBox must receive a
  call to its __set__ to explicitly set a value, before it is allowed to
  receive __get__ calls. """
