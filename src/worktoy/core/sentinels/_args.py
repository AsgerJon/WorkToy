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
  from typing import Any, Self, Iterator, Optional


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

  Each subscript builds a new instance, so two signatures written the same
  way hold two distinct instances. Instances therefore compare and hash by
  their inner type, which lets a variadic signature in a subclass be
  recognized as equal to the one it overrides.
  """

  def __iter__(self) -> Iterator[Self]:
    """
    ARGS is iterable and yields itself.
    """
    yield from (self,)

  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, ARGS):
      return NotImplemented
    return True if self.__inner_type__ is other.__inner_type__ else False

  def __hash__(self) -> int:
    return hash((type(self).__name__, self.__inner_type__))

  def __str__(self) -> str:
    """
    The rendering follows the subscript that created the instance, for
    example 'ARGS[int]'.
    """
    innerType = self.__inner_type__
    innerName = getattr(innerType, '__name__', None) or str(innerType)
    return '%s[%s]' % (type(self).__name__, innerName)

  __repr__ = __str__

  @classmethod
  def __class_getitem__(cls, type_: type) -> Self:
    """
    ARGS is subscriptable and returns an instance covering the given type.
    """
    return cls(type_)
