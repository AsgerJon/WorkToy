"""
Count is an 'int' subclass declaring a '__cast_as__' hook.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import typeCast

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class Count(int):
  """
  A subclass of a family builtin converts only through a classmethod
  '__cast_as__' of its own, which may lean on the families. 'Count' is
  the example of the 'typeCast' docstring: an 'int' subclass whose hook
  casts the value to 'int' and builds 'cls' from it, so a subclass of
  'Count' inheriting the hook builds itself.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __cast_as__(cls, value: Any) -> Self:
    return cls(typeCast(int, value))
