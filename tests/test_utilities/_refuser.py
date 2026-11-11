"""
Refuser is a class whose '__cast_as__' hook answers 'NotImplemented'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Refuser:
  """
  A '__cast_as__' hook refuses a value by returning 'NotImplemented',
  which 'typeCast' turns into 'TypeCastException'. 'Refuser' refuses
  every value.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __cast_as__(cls, value: Any) -> Any:
    return NotImplemented
