"""
Hooked is a plain class with an '__init_subclass__' of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox


class Hooked:
  """
  The hook 'THIS' installs on a holder must call what the holder held
  under '__init_subclass__' before, with every class keyword, so the
  holder goes on reacting to its subclasses. 'Hooked' records the name
  and keywords of every subclass in 'records'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  records: list = []

  #  Public Variables
  x = AttriBox[int](0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init_subclass__(cls, **kwargs) -> None:
    Hooked.records.append((cls.__name__, dict(kwargs)))
