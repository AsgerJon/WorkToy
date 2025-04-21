"""CastMismatch should be raised to indicate that the fast static
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


class _ExpectedType:
  """Descriptor for the expected type passed to the exception."""

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the expected type."""
    if instance is None:
      return self
    expectedType = getattr(instance, '__expected_type__', None)
    if expectedType is None:
      info = """'__expected_type__' attribute is not set!"""
      raise RuntimeError(info)
    return expectedType


class _ActualObject:
  """Descriptor for the actual object passed to the exception."""

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the actual object."""
    if instance is None:
      return self
    obj = getattr(instance, '__actual_object__', None)
    if obj is None:
      info = """'__actual_object__' attribute is not set!"""
      raise RuntimeError(info)
    return obj


class CastMismatch(TypeError):
  """FastCastMismatch should be raised to indicate that the fast static
  system of the TypeSig class did not match."""

  __expected_type__ = None
  __actual_object__ = None

  expType = _ExpectedType()
  actObj = _ActualObject()

  def __init__(self, type_: type, obj: object) -> None:
    """Initialize the FastCastMismatch object."""
    self.__expected_type__ = type_
    self.__actual_object__ = obj
    typeName = type_.__name__
    objDescription = str(obj)
    info = """Expected type: '%s' does not match received argument 
    signature: '(%s)'!"""
    TypeError.__init__(self, monoSpace(info) % (typeName, objDescription))
