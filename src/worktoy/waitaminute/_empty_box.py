"""EmptyBox provides a custom exception raised when an instance of
AbstractBox is unable to find an existing value. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

if TYPE_CHECKING:
  from worktoy.attr import AbstractBox


class _Box:
  """Simple descriptor"""

  def __get__(self, instance: object, owner: type) -> object:
    return getattr(instance, '__box_instance__', None)


class _Instance:
  """Simple descriptor"""

  def __get__(self, instance: object, owner: type) -> object:
    return getattr(instance, '__owning_instance__', None)


class EmptyBox(Exception):
  """EmptyBox provides a custom exception raised when an instance of
  AbstractBox is unable to find an existing value. """

  __empty_box__ = None
  __owning_instance__ = None
  box = _Box()
  instance = _Instance()

  def __init__(self, box: object, instance: object) -> None:
    self.__empty_box__ = box
    self.__owning_instance__ = instance
    Exception.__init__(self, )
