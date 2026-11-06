"""
Agreeable is a value whose '__eq__' answers 'True' to anything.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Agreeable:
  """
  Several checks of 'core' compare by identity on purpose: whether an
  argument is a placeholder, whether a value is 'DELETED', whether a
  read hook runs for the same instance, whether a body bound the very
  clone. A value equal to everything tells identity from equality in
  each of them. 'Agreeable' is that value, hashable so it may be looked
  up, and 'Object' owners may be based on it.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __eq__(self, other: Any) -> bool:
    return True

  def __hash__(self) -> int:
    return 0
