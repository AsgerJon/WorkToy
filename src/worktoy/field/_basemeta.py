"""BaseMeta is an abstract meta base class adding common functionalities."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations
from icecream import ic

from typing import Any, NoReturn

ic.configureOutput(includeContext=True)

Bases = tuple[type]


class BaseMeta(type):
  """BaseMeta implementing some validation"""

  immutableTypes = {
    int, float, bool, str, tuple, bytes, complex, frozenset, type(None)}

  @staticmethod
  def isDunder(name: str) -> bool:
    """Checks if the name is a dunder name"""
    return True if name.startswith('__') and name.endswith('__') else False

  @staticmethod
  def isImmutable(obj: Any) -> bool:
    """Checks if obj is immutable"""
    test = any([isinstance(obj, type_) for type_ in BaseMeta.immutableTypes])
    return True if test else False

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple[type], **kwargs) -> dict:
    """Allows definition of a starting point for the class namespace"""
    return {}

  def __new__(mcls, name: str, bases: Bases, attrs: dict, **kwargs) -> type:
    """Marking attributes that are not dunder or immutable with the class."""
    cls = super().__new__(mcls, name, bases, attrs, )
    setattr(cls, '__meta__', mcls)
    for (key, val) in attrs.items():
      if not (mcls.isDunder(key) or mcls.isImmutable(val)):
        setattr(val, '__cls__', cls)
        setattr(cls, key, val)
    return cls

  def __init__(cls, name: str, bases: Bases, attrs: dict, **kwargs) -> None:
    """Class creation"""
    super().__init__(name, bases, attrs, **kwargs)

  def __call__(cls, *args, **kwargs) -> Any:
    """Creates a new instance of a class using as metaclass this."""
    instance = cls.__new__(cls)
    cls.__init__(instance, *args, **kwargs)
    return instance

  def __str__(cls) -> str:
    """String representation"""
    return """Hi there! I'm the basic meta class!"""
