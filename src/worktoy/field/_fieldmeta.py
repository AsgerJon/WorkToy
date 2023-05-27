"""_FieldMeta is a metaclass forcing a new attribute __cls__ onto the
decorated class and in particular its functions"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations


class _FieldMethod:
  """_FieldMethod decorates methods in classes with _FieldMeta as
  metaclass"""


class _FieldMeta(type):
  """_FieldMeta is a metaclass forcing a new attribute __cls__ onto the
  decorated class and in particular its functions"""

  @staticmethod
  def _should_update_attr(attr_name: str, attr_value: str) -> bool:
    """This static method checks if the attribute should be updated to
    refer to the owning class by adding a new attribute called __cls__
    pointing to it."""
    if attr_name.startswith("__"):
      return False
    if isinstance(attr_value, (int, float, str, tuple, frozenset)):
      return False
    return True

  def __init__(cls, clsname, bases, attrs) -> None:
    """Creates a new class whose methods are aware of it directly through
    the __cls__ attribute."""
    super().__init__(clsname, bases, attrs)
    for attr_name, attr_value in attrs.items():
      if _FieldMeta._should_update_attr(attr_name, attr_value):
        setattr(attr_value, "__cls__", cls)
        setattr(cls, attr_name, attr_value)


class FieldMeta(metaclass=_FieldMeta):
  """Intermediary class"""

  __clc__: type
