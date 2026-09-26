"""
Minimal reproduction of a PyCharm false positive.

A Generic class whose subscript returns a configured INSTANCE via
'__class_getitem__', which is then called to capture deferred args.
Pyright reports no problems. PyCharm flags the marked line with:

  Expected type Box[int] (matched generic type Self@Box),
  got type[Box[int]] instead
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen

from __future__ import annotations

from typing import Any, Generic, Self, TypeVar, Optional

T = TypeVar('T')


class SomeType:  pass


class Box(SomeType, Generic[T]):
  __field_type__: Optional[type] = None

  def __init__(self, *args, **kwargs) -> None:  ...

  @classmethod
  def __class_getitem__(cls, item: type) -> Self:
    self = object.__new__(cls)
    self.__field_type__ = item
    return self  # noqa

  def __call__(self, *args: Any, **kwargs: Any) -> Self:
    return self  # noqa
  #
  # def __get__(self, instance: Any, owner: Any) -> T:
  #   ...
