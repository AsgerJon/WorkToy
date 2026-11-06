"""
OWNER provides a sentinel object used together with THIS by the descriptor
flow where OWNER provides a placeholder for the owning class, while THIS
refers to an instance of the class (self typically).
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import Sentinel


class OWNER(Sentinel):
  """
  The arguments of an 'AttriBox' are written in the class body, before
  the class exists, and used at the first read to build the value. One of
  them may need to be the class the attribute is read through, which the
  class body cannot name yet.

  Implementation
  --------------

  At the first read, an argument that is 'OWNER' itself is replaced by
  the owner passed to '__get__'. 'THIS' does the same for the instance
  and 'DESC' for the box. Unlike 'THIS', 'OWNER' has no meaning in an
  overload signature.
  """
