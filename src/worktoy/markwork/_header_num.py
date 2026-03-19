"""
HeaderNum subclasses 'KeeNum' and enumerates the header levels.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Iterable, Type


class HeaderNum(KeeNum):
  """
  HeaderNum subclasses 'KeeNum' and enumerates the header levels.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Enumerations
  TITLE = Kee[str]('h1')
  CHAPTER = Kee[str]('h2')
  SECTION = Kee[str]('h3')
  SUBSECTION = Kee[str]('h4')
  PARAGRAPH = Kee[str]('p')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __int__(self, ) -> int:
    cls = type(self)
    return sum((*(i if (m is self) else 0 for i, m in enumerate(cls)),))
