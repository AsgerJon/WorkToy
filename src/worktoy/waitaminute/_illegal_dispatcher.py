"""
IllegalDispatcher is a custom exception raised to indicate that a subclass
of 'Dispatch' has failed to identify itself as a dispatcher. All
subclasses of 'Dispatch' must provide the '__overload_dispatcher__' key in
their namespace allowing 'TypeSig' to identify recursive constructor calls
that would otherwise cause hard-to-debug recursion errors. These errors
might even include infinite recursions not detectable by the Python
recursion limit.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class IllegalDispatcher(Exception):
  """IllegalDispatcher is a custom exception raised to indicate that a
  subclass of 'Dispatch' has failed to identify itself as a dispatcher. All
  subclasses of 'Dispatch' must provide the '__overload_dispatcher__' key in
  their namespace allowing 'TypeSig' to identify recursive constructor calls
  that would otherwise cause hard-to-debug recursion errors. These errors
  might even include infinite recursions not detectable by the Python
  recursion limit.
  """

  dispatcher = _Attribute()

  def __init__(self, cls: type) -> None:
    """Initialize the IllegalDispatcher exception."""
    Exception.__init__(self, )
    self.dispatcher = cls

  def __str__(self, ) -> str:
    """
    Return a string representation of the IllegalDispatcher exception.
    """
    infoSpec = """IllegalDispatcher: Class '%s' failed to set 
      '__overload_dispatcher__ = True'. This token is required for overload 
      dispatchers so that TypeSig can prevent infinite recursion during 
      __init__ overload resolution."""
    return monoSpace(infoSpec % self.dispatcher.__name__)

  __repr__ = __str__
