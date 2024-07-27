"""MetaClass is a sus version of type"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any


class MetaClass(type):
  """MetaClass is a sus version of type"""

  @classmethod
  def __prepare__(mcls,
                  name: str,
                  bases: tuple[type, ...],
                  **kwargs) -> dict:
    return dict()

  def __new__(mcls,
              name: str,
              bases: tuple,
              namespace: dict,
              **kwargs) -> Any:
    """Create a new instance of the class."""
    cls = type.__new__(mcls, name, bases, namespace, **kwargs)
    return cls

  def __call__(cls, *args, **kwargs) -> Any:
    """Call the class."""
    self = cls.__new__(cls, *args, **kwargs)
    self.__init__(*args, **kwargs)
    return self


class Test(metaclass=MetaClass):
  """Test is a test class for the MetaClass metaclass."""

  def __init__(self, *args, **kwargs) -> None:
    pass

  def __str__(self) -> str:
    return 'Test'
