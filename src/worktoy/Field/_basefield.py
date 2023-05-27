"""BaseField decorates classes with fields"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations
from typing import Any, NoReturn

from icecream import ic

ic.configureOutput(includeContext=True)


class BaseField:
  """Field decorates a class a with a field
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, name: str, value: Any) -> None:
    self._name = name
    self._value = value

  def __get__(self, *args) -> Any:
    """Implementation of getter"""
    for arg in args:
      ic(arg)
    return self._value

  def __set__(self, *args, ) -> NoReturn:
    """Implementation of setter"""
    for arg in args:
      ic(arg)
    self._value = args[1]

  def __call__(self, cls: type) -> type:
    """Decorates the class"""
    setattr(cls, self._name, self)
    return cls
