"""
Loose is a class declaring '__cast_as__' as a plain function.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Loose:
  """
  A '__cast_as__' that is no classmethod would run with the value bound
  as 'self', so 'typeCast' refuses it with 'UnboundCastHook' before
  calling it. 'Loose' declares the hook as a plain function.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __cast_as__(self, value: Any) -> Any:
    return value
