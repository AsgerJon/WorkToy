"""
Foreign is a class whose '__cast_as__' hook returns the value itself.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Foreign:
  """
  A '__cast_as__' hook returning anything but an instance of its class
  or 'NotImplemented' is refused by 'typeCast', so a field or an
  overload never receives a foreign object. 'Foreign' hands the value
  back unchanged.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __cast_as__(cls, value: Any) -> Any:
    return value
