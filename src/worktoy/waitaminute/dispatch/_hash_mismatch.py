"""HashMismatch is raised by the dispatcher system to indicate a hash
based mismatch between a type signature and a tuple of arguments. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from worktoy.dispatch import TypeSignature


class HashMismatch(Exception):
  """HashMismatch is raised by the dispatcher system to indicate a hash
  based mismatch between a type signature and a tuple of arguments. """

  __slots__ = ('sig', 'args')

  def __init__(self, sig: TypeSignature, *args) -> None:
    """HashMismatch is raised by the dispatcher system to indicate a hash
    based mismatch between a type signature and a tuple of arguments. """
    self.sig = sig
    self.args = args

    Exception.__init__(self, )

  def __str__(self) -> str:
    """Get the string representation of the HashMismatch."""
    sigStr = str(self.sig)
    argTypes = [type(arg).__name__ for arg in self.args]
    argStr = """(%s)""" % ', '.join(argTypes)
    sigHash = hash(self.sig)
    try:
      argHash = hash(self.args)
    except TypeError:
      argHash = '<unhashable>'

    infoSpec = """Unable to match type signature: <br><tab>%s<br>with
    signature of arguments:<br><tab>%s<br>Received hashes: %d != %s"""
    info = infoSpec % (sigStr, argStr, sigHash, argHash)
    return textFmt(info)

  __repr__ = __str__
