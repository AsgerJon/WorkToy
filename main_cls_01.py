"""
LOL
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import Self


class Meta(type):
  """
  Trolololo
  """

  def __instancecheck__(cls, other: object) -> bool:
    """
    This method is consulted only if type(other) is not cls. Let's fix that!
    """
    for base in cls.__bases__:
      if base is type(other):
        return True
    return False

  @classmethod
  def __prepare__(mcls, name, bases, **kwargs) -> dict:
    return dict()

  def __new__(mcls, name, bases, namespace, **kwargs) -> Self:
    shadow = super().__new__(mcls, name, bases, namespace)
    space = dict(__shadow_class__=shadow)
    return super().__new__(mcls, name, (shadow, *bases), space)

  def __call__(cls, *args, **kwargs) -> None:
    try:
      shadow = getattr(cls, '__shadow_class__')
    except AttributeError:
      return super().__call__(*args, **kwargs)
    else:
      return shadow(*args, **kwargs)


class Foo(metaclass=Meta):

  def __init__(self, *args, **kwargs) -> None:
    self.__is_trolling__ = kwargs.get('_trolling', False)


def main() -> int:
  foo = Foo()
  print(isinstance(foo, Foo))
  return 0
