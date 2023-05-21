"""CallMeMaybe"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations


class CallMeMaybeMeta(type):
  def __instancecheck__(cls, instance: object) -> bool:
    """Check if an object is a member of CallMeMaybe."""
    if hasattr(instance, '__call__'):
      return not getattr(instance, 'is_excluded', False)
    return False


class CallMeMaybe(metaclass=CallMeMaybeMeta):
  """Base class that considers callable objects as its members, unless
  exempted."""

  @classmethod
  def secret(cls, func: callable) -> callable:
    """Decorator to mark a function as exempt from CallMeMaybe membership."""
    func.is_excluded = True
    return func

  def __init__(self):
    """Prevent direct instantiation of CallMeMaybe."""
    raise InstantiationError("CallMeMaybe cannot be instantiated.")
