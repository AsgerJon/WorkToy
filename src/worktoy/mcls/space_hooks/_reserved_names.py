"""
ReservedNames lists the names the interpreter sets automatically.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, TypeAlias, Union

  Names: TypeAlias = tuple[str, ...]


class ReservedNames:
  """
  ReservedNames provides a list of reserved names that are set
  automatically by the interpreter.
  """

  # @formatter:off
  @overload
  def __get__(self, instance: None, owner: type) -> Self: ...
  @overload
  def __get__(self, instance: Any, owner: type) -> Names: ...
  # @formatter:on

  def __get__(self, instance: Any, owner: type) -> Union[Self, Names]:
    if instance is None:
      return self
    return (
      '__dict__',
      '__weakref__',
      '__module__',
      '__annotations__',
      '__match_args__',
      '__doc__',
      '__name__',
      '__qualname__',
      '__firstlineno__',
      '__static_attributes__',
    )
