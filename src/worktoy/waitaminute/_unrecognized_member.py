"""UnrecognizedMember is raised when a KeeNum class is unabled to
recognize a given identifier."""
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
  from typing import Any


class UnrecognizedMember(Exception):
  """UnrecognizedMember is raised when a KeeNum class is unable to
  recognize a given identifier."""

  __keenum_cls__ = None
  __unrecognized_identifier__ = None

  def __init__(self, keenumCls: type, unrecognizedIdentifier: Any) -> None:
    """Initialize the UnrecognizedMember object."""
    self.__keenum_cls__ = keenumCls
    self.__unrecognized_identifier__ = unrecognizedIdentifier
    info = "Unrecognized identifier '%s' in KeeNum class '%s'"
    Exception.__init__(self, info % (unrecognizedIdentifier, keenumCls))
