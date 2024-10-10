"""DoubleDollarException is raised when trying to find environment
variable names in a string containing two consecutive dollar signs. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace


class DoubleDollarException(SyntaxError):
  """DoubleDollarException is raised when trying to find environment
  variable names in a string containing two consecutive dollar signs. """

  def __init__(self, *args) -> None:
    if args:
      e = """The string: '%s' contains instances of consecutive dollar 
      signs which is not supported!""" % args[0]
      SyntaxError.__init__(self, monoSpace(e))
    else:
      SyntaxError.__init__(self, )
