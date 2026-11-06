"""
Suspicious is a class whose '__eq__' answers 'True' to anything and
counts how often it was asked.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class Suspicious:
  """
  'typeCast' to 'bool' compares a number with 0 and 1 and nothing else,
  since the '__eq__' of an arbitrary object may answer 'True' to anything.
  'Suspicious' is that object: equal to everything, and counting in
  'asked' how many times its '__eq__' ran, so a test can see that the
  cast never asked. Its '__cast_as__' hook builds a fresh instance, so
  a test can also see that the result of a hook is checked against
  'NotImplemented' by identity rather than through its '__eq__'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  asked: int = 0

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __cast_as__(cls, value: Any) -> Self:
    return cls()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __eq__(self, other: Any) -> bool:
    self.asked += 1
    return True
