"""HashMismatch is raised by the dispatcher system to indicate a hash
based mismatch between a type signature and a tuple of arguments. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.static import TypeSig

  from typing import Self


class HashMismatch(Exception):
  """HashMismatch is raised by the dispatcher system to indicate a hash
  based mismatch between a type signature and a tuple of arguments. """

  typeSig = _Attribute()
  posArgs = _Attribute()
  types = _Attribute()

  def __init__(self, typeSig_: TypeSig, *args) -> None:
    """HashMismatch is raised by the dispatcher system to indicate a hash
    based mismatch between a type signature and a tuple of arguments. """
    self.types = typeSig_
    self.posArgs = args

    Exception.__init__(self, )

  def __str__(self) -> str:
    """Get the string representation of the HashMismatch."""
    sigStr = str(self.typeSig)
    argTypes = [type(arg).__name__ for arg in self.posArgs]
    argStr = """(%s)""" % ', '.join(argTypes)
    sigHash = hash(self.typeSig)
    try:
      argHash = hash(self.posArgs)
    except TypeError:
      argHash = '<unhashable>'

    infoSpec = """Unable to match type signature: <br><tab>%s<br>with
    signature of arguments:<br><tab>%s<br>Received hashes: %d != %s"""
    info = infoSpec % (sigStr, argStr, sigHash, argHash)
    return monoSpace(info)

  __repr__ = __str__
