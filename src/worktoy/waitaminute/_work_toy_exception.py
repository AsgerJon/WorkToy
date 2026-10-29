"""
WorkToyException is the common base of every exception in the
'worktoy.waitaminute' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations


class WorkToyException(Exception):
  """
  WorkToyException is the common base of every exception in the
  'worktoy.waitaminute' package, the control-flow signals aside. Each
  exception keeps the builtin it is based on, 'TypeError',
  'AttributeError', 'SyntaxError' and so on, by listing this class first
  and the builtin after it, so 'except TypeError' catches a
  'TypeException' as ever, and 'except WorkToyException' catches every
  exception of the library at once.

  The class declares empty slots so that it adds no layout of its own and
  may stand beside 'SyntaxError', whose layout is wider than that of
  'Exception'.
  """

  __slots__ = ()
