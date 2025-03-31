"""FastCastMismatch should be raised to indicate that the fast static
system of the TypeSig class did not match."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

try:
  from typing import TYPE_CHECKING, Any
except ImportError:
  TYPE_CHECKING = False
  Any = object

if TYPE_CHECKING:
  from worktoy.static import TypeSig


class _Sig:
  """Descriptor for the TypeSig object passed to the exception."""

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the TypeSig object."""
    if instance is None:
      return self
    sig = getattr(instance, '__type_sig__', None)
    if sig is None:
      info = """'__type_sig__' attribute is not set!"""
      raise RuntimeError(info)
    return sig


class _PosArgs:
  """Descriptor for the positional arguments passed to the exception."""

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the positional arguments."""
    if instance is None:
      return self
    args = getattr(instance, '__pos_args__', None)
    if args is None:
      info = """'__pos_args__' attribute is not set!"""
      raise RuntimeError(info)
    return args


class CastMismatch(TypeError):
  """FastCastMismatch should be raised to indicate that the fast static
  system of the TypeSig class did not match."""

  __type_sig__ = None
  __pos_args__ = None

  typeSig = _Sig()
  posArgs = _PosArgs()

  def __init__(self, sig: TypeSig, *args) -> None:
    """Initialize the FastCastMismatch object."""
    self.__type_sig__ = sig
    self.__pos_args__ = args
    sigInfo = str(sig)
    argTypes = [type(arg).__name__ for arg in args]
    argInfo = ', '.join(argTypes)
    info = """TypeSig object:  '%s' does not match received argument 
    signature: '(%s)'!"""
    TypeError.__init__(self, monoSpace(info % (sigInfo, argInfo)))
