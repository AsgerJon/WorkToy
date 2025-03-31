"""DispatchException provides a custom exception raised when an instance
of OverloadDispatcher fails to resolve the correct function from the
given arguments. Because the overload protocol relies on type matching,
this exception subclasses TypeError such that it can be caught by external
error handlers. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.static import Dispatch


class DispatchException(TypeError):
  """DispatchException provides a custom exception raised when an instance
  of OverloadDispatcher fails to resolve the correct function from the
  given arguments. """

  def __init__(self, dispatch: Dispatch, *args) -> None:
    dispatchStr = str(dispatch)
    argStr = ', '.join([type(arg).__name__ for arg in args])
    e = """The dispatcher \n'%s' \nreceived: \n'%s'!"""
    TypeError(e % (dispatchStr, argStr))
