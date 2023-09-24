"""WorkToy - Core - Header
Code writing assistant"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.texttools import TextBox


class Header(TextBox):
  """Class providing a header"""

  def __init__(self, *args, **kwargs) -> None:
    TextBox.__init__(self, *args, **kwargs)
    self.leftMargin = '  #%s|' % (10 * ' ')
    self.rightMargin = '|%s#  ' % (10 * ' ')
