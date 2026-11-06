"""
KeyBind is a worktoy class with three 'KeeBox' fields.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeBox
from worktoy.mcls import BaseObject

from . import WeekDay, Permission, Shade


class KeyBind(BaseObject):
  """
  A 'KeeBox' declares a field over an enumeration with the member it
  starts as, written the way a project thinks of it. 'KeyBind' names a
  day in the wrong case, lists two flags, and gives a shade by its
  value.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  day = KeeBox[WeekDay]('tuesday')
  access = KeeBox[Permission]('read', 'exec')
  level = KeeBox[Shade](5)
