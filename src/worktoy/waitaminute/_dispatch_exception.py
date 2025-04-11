"""DispatchException provides a custom exception raised when an instance
of OverloadDispatcher fails to resolve the correct function from the
given arguments. Because the overload protocol relies on type matching,
this exception subclasses TypeError such that it can be caught by external
error handlers. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.static import Dispatch


class DispatchException(TypeError):
  """DispatchException provides a custom exception raised when an instance
  of OverloadDispatcher fails to resolve the correct function from the
  given arguments. Because the overload protocol relies on type matching,
  this exception subclasses TypeError such that it can be caught by external
  error handlers. """

  def __init__(self, dispatch: Dispatch, *args) -> None:
    dispatchStr = str(dispatch)
    argTypes = [type(arg) for arg in args]
    argNames = [t.__name__ for t in argTypes]
    argStr = ', '.join(argNames)
    info = """%s\nbut received: (%s)""" % (dispatchStr, argStr)
    TypeError.__init__(self, info)
