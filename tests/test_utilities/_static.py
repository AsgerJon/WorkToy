"""
Static is a class declaring '__cast_as__' as a staticmethod.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Static:
  """
  A staticmethod '__cast_as__' has no class to build an instance of, so
  'typeCast' refuses it with 'UnboundCastHook' like a plain function.
  'Static' declares the hook that way.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def __cast_as__(value: Any) -> Any:
    return value
