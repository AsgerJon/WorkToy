"""The 'worktoy.meta' module provides the implementation of 'overload'."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import OverloadEntry


def overload(*types) -> OverloadEntry:
  """Decorator function for overloading functions."""
  typeNames = [cls.__name__ for cls in types]
  info = """Overloading types: '%s'""" % ', '.join(typeNames)
  # print(info)
  return OverloadEntry(*types)
