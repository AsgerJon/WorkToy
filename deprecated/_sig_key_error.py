"""SigKeyError is raised if multiple callables are attempted to be signed
to the same TypeSig object. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Callable
  from worktoy.static import TypeSig


class SigKeyError(KeyError):
  """SigKeyError is raised if multiple callables are attempted to be signed
  to the same TypeSig object. """

  __type_sig__ = None
  __call_me_maybe__ = None

  def __init__(self, typeSig: TypeSig, callMeMaybe: Callable) -> None:
    """Initialize the SigKeyError object."""
    self.__type_sig__ = typeSig
    self.__call_me_maybe__ = callMeMaybe
    funcName = callMeMaybe.__name__
    info = "Callable '%s' is already signed to '%s'"
    Exception.__init__(self, info % (funcName, typeSig))
