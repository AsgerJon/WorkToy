"""SigMismatch exception is raised when a TypeSig object fails to
recognize a tuple of arguments."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False


class SigMismatch(TypeError):
  """SigMismatch exception is raised when a TypeSig object fails to
  recognize a tuple of arguments."""

  __type_tuple__ = None
  __pos_args__ = None

  def __init__(self, typeTuple: tuple[type, ...], posArgs: tuple) -> None:
    """Initialize the SigMismatch object."""
    self.__type_tuple__ = typeTuple
    self.__pos_args__ = posArgs
    if len(typeTuple) != len(posArgs):
      info = """Length mismatch between supported type signature and 
      positional arguments!"""
    else:
      info = """Received positional arguments of types: <br><tab>%s<br>, 
      but expected types: <br><tab>(%s)"""
      argTypes = [type(arg).__name__ for arg in posArgs]
      argStr = ', '.join(argTypes)
      typeNames = [type(arg).__name__ for arg in typeTuple]
      typeStr = ', '.join(typeNames)
      TypeError.__init__(self, monoSpace(info % (argStr, typeStr)))
