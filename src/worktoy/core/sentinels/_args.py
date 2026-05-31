"""
ARGS uses a Sentinel metaclass and provides a placeholder for a starred
argument in an overload signature.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import SentinelMeta

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Iterator, Optional


class _MetaARGS(SentinelMeta):
  """
  Metaclass for the 'ARGS' sentinel.
  """

  __inner_type__: Optional[type] = None

  def __new__(mcls, *args, **kwargs) -> _MetaARGS:
    # noinspection PyTypeChecker
    return type.__new__(mcls, *args, **kwargs)

  def __call__(cls, type_: type) -> _MetaARGS:
    """
    Creates an instance covering the given type.
    """
    self = type.__call__(cls, )
    self.__inner_type__ = type_
    return self


class ARGS(metaclass=_MetaARGS):
  """
  ARGS uses a Sentinel metaclass and provides a placeholder for a starred
  argument in an overload signature.
  """

  def __iter__(self) -> Iterator[Self]:
    """
    ARGS is iterable and yields itself.
    """
    yield from (self,)

  @classmethod
  def __class_getitem__(cls, type_: type) -> Self:
    """
    ARGS is subscriptable and returns an instance covering the given type.
    """
    return cls(type_)
