"""SigMismatch exception is raised when a TypeSig object fails to
recognize a tuple of arguments."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

try:
  from typing import Any
except ImportError:
  Any = object

if TYPE_CHECKING:
  from worktoy.static import TypeSig


class _TypeSig:
  """Descriptor for the TypeSig object passed to the exception."""

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the TypeSig object."""
    if instance is None:
      return self
    typeSig = getattr(instance, '__type_sig__', None)
    if typeSig is None:
      info = """'__type_sig__' attribute is not set!"""
      raise RuntimeError(info)
    return typeSig


class _PosArgs:
  """Descriptor for the positional arguments passed to the exception."""

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the positional arguments."""
    if instance is None:
      return self
    posArgs = getattr(instance, '__pos_args__', None)
    if posArgs is None:
      info = """'__pos_args__' attribute is not set!"""
      raise RuntimeError(info)
    return posArgs


class SigMismatch(TypeError):
  """SigMismatch exception is raised when a TypeSig object fails to
  recognize a tuple of arguments."""

  __type_sig__ = None
  __pos_args__ = None

  typeSig = _TypeSig()
  posArgs = _PosArgs()

  def __init__(self, typeSig: TypeSig, *args) -> None:
    self.__type_sig__ = typeSig
    self.__pos_args__ = args
    typeInfo = str(typeSig)
    fmt = lambda arg: '  %s of type: %s' % (str(arg), type(arg).__name__)
    listArgs = '\n'.join([fmt(arg) for arg in args])
    head = """Type signature: '%s' does not match received arguments:\n%s"""
    TypeError.__init__(self, head % (typeInfo, listArgs))
