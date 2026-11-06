"""
UnhashableMeta builds classes that cannot be hashed.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class UnhashableMeta(type):
  """
  The dispatch function looks a call up by the tuple of the classes of
  its arguments, which fails when one of those classes cannot be hashed,
  and the call must then go on to the 'isinstance' passes. A metaclass
  defining '__eq__' without '__hash__' makes its classes unhashable;
  'UnhashableMeta' is such a metaclass.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __eq__(cls, other: Any) -> bool:
    return cls is other
