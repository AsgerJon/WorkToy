"""
WorkToyException is the common base of every exception in the
'worktoy.waitaminute' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


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

  A message that shows a value shows it through '_reprOf', so that every
  exception of the library shows a value the same way.
  """

  __slots__ = ()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _reprOf(value: Any) -> str:
    """
    The '_reprOf' method gives the text a message shows for a value: its
    'repr', which tells the string '12' from the number 12 and shows an
    empty string, cut to 50 characters so that a large object does not
    flood the message. The 'repr' of a string brings its quotes, so a
    message puts none around a value.
    """
    text = repr(value)
    if len(text) > 50:
      return """%s...""" % text[:47]
    return text
