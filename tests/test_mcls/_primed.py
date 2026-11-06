"""
Primed is a worktoy class that records what '__class_init__' receives.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class Primed(BaseObject):
  """
  A class may finish itself once it exists through '__class_init__',
  which receives the name, the bases, the namespace object and the
  class keywords, for the class and for every subclass inheriting the
  hook. 'Primed' appends each call to 'inits'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  inits: list = []

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CLASS HOOKS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_init__(cls, name: str, bases: tuple, space: Any, **kw) -> None:
    cls.inits.append((cls, name, bases, space, kw))
