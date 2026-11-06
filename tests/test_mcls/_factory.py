"""
Factory is a worktoy class that builds, recognizes and admits in its own
way.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Factory(BaseObject):
  """
  A class may take over its own call, its 'isinstance' and its
  'issubclass' through '__class_call__', '__class_instancecheck__' and
  '__class_subclasscheck__'. 'Factory' returns a tagged tuple of the
  arguments from a call, counts every 'int' as an instance and every
  subclass of 'int' as a subclass.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CLASS HOOKS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_call__(cls, *args, **kwargs) -> tuple:
    return 'made', args, kwargs

  @classmethod
  def __class_instancecheck__(cls, obj: Any) -> bool:
    return True if isinstance(obj, int) else False

  @classmethod
  def __class_subclasscheck__(cls, subclass: type) -> bool:
    return True if issubclass(subclass, int) else False
