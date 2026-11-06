"""
DirOwner is a class whose 'here' attribute is a 'Directory'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import Directory


class DirOwner:
  """
  The tests of 'Directory' need a class defined in a file, so that the
  descriptor has a source directory to report. 'DirOwner' is that class,
  and this file is the directory it reports.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  here = Directory()
