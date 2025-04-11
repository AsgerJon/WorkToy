"""DELETED provides a value used to indicate that an attribute is to be
treated as having been deleted. For example, after a call to __delete__,
subsequent calls to __get__ should raise AttributeError until a call to
__set__ provides a new value. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations


class _MetaDeleted(type):
  """Metaclass for DELETED class object"""

  def __call__(cls, *args, **kwargs) -> None:
    """Call the DELETED class object"""
    raise TypeError(f"{cls.__name__} is not callable")


class DELETED(metaclass=_MetaDeleted):
  """DELETED is a singleton class that is used to indicate that an
  attribute"""
  pass
