"""
FullName subclasses 'EZData' and provides an ordered encapsulation of a
person's full name, with family name first and given names second.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData, EZField

if TYPE_CHECKING:  # pragma: no cover
  pass


class FullName(EZData, ordered=True):
  """
  FullName subclasses 'EZData' and provides an ordered encapsulation of a
  person's full name, with family name first and given names second.
  """

  givenNames = EZField[str]()
  familyName = EZField[str]()

  def __str__(self, ) -> str:
    infoSpec = "%s, %s"
    return infoSpec % (self.familyName, self.givenNames)
