"""HashMismatch is raised by the dispatcher system to indicate a hash
based mismatch between a type signature and a tuple of arguments. """
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
  from worktoy.static import TypeSig


class HashMismatch(Exception):
  """HashMismatch is raised by the dispatcher system to indicate a hash
  based mismatch between a type signature and a tuple of arguments. """

  __type_sig__ = None
  __pos_args__ = None

  def __init__(self, typeSig: TypeSig, *args) -> None:
    """HashMismatch is raised by the dispatcher system to indicate a hash
    based mismatch between a type signature and a tuple of arguments. """

    self.__type_sig__ = typeSig
    self.__pos_args__ = args

    info = """Expected arguments to be of type:<br><tab>%s<br>but 
    received:<br><tab>%s"""
    argStr = """(%s)""" % ', '.join([type(arg).__name__ for arg in args])
    info = info % (str(typeSig), argStr)
    Exception.__init__(self, info)
