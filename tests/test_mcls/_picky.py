"""
Picky is a worktoy class that sees every subclass and refuses some.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseObject


class Picky(BaseObject):
  """
  The metaclass calls '__subclasshook__' on each base with the new class
  and ignores the answer, so a base may only refuse a subclass by
  raising. 'Picky' records the name of every subclass in 'seen' and
  raises 'TypeError' for one whose name starts with 'Bad'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  seen: list = []

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __subclasshook__(cls, subclass: type) -> bool:
    Picky.seen.append(subclass.__name__)
    if subclass.__name__.startswith('Bad'):
      names = (subclass.__name__, cls.__name__)
      raise TypeError('%s is refused by %s' % names)
    return NotImplemented
