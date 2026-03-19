"""
ChapterStyle subclasses 'Style' and provides the styling for the 'Chapter'
class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..desc import AttriBox
from ..keenum import KeeBox
from . import Style, HeaderNum

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union

  BoolBox: TypeAlias = Union[bool, AttriBox]
  HeaderBox: TypeAlias = Union[HeaderNum, KeeBox]


class ChapterStyle(Style):
  """
  ChapterStyle subclasses 'Style' and provides the styling for the
  'Chapter' class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  italic: BoolBox = AttriBox[bool](False)
  bold: BoolBox = AttriBox[bool](True)
  underline: BoolBox = AttriBox[bool](False)
  strikethrough: BoolBox = AttriBox[bool](False)
