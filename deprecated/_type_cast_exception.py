"""TypeCastException is a custom exception class inheriting from
TypeError. It is raised to indicate that a type casting operation has
failed. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import typeMsg


class TypeCastException(TypeError):
  """TypeCastException is a custom exception class inheriting from
  TypeError. It is raised to indicate that a type casting operation has
  failed. """

  def __init__(self, obj: object, expType: type) -> None:
    e = typeMsg('object', obj, expType)
    TypeError.__init__(self, e)
