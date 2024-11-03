"""DispatchException provides a custom exception raised when an instance
of OverloadDispatcher fails to resolve the correct function from the
given arguments. Because the overload protocol relies on type matching,
this exception subclasses TypeError such that it can be caught by external
error handlers. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.meta import Dispatcher


class DispatchException(TypeError):
  """DispatchException provides a custom exception raised when an instance
  of OverloadDispatcher fails to resolve the correct function from the
  given arguments. """

  def __init__(self, dispatch: Dispatcher, *args) -> None:
    e = """Dispatch instance could not match signature of arguments to any 
    supported signature. Received: <br><tab>'%s'<br>Supported 
    signatures: %s"""
    argSig = ', '.join([type(arg).__name__ for arg in args])
    supported = []
    for sig in dispatch.getTypeSignatures():
      types = sig.getTypes()
      typeNames = [t.__name__ for t in types]
      supported.append("""(%s)""" % ', '.join(typeNames))
    supportedSig = '<br><tab>'.join(supported)
    e2 = monoSpace(e % (argSig, supportedSig))
    TypeError.__init__(self, e2)
