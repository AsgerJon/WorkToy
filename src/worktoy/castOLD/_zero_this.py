"""THIS represents the not yet created class. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

try:
  from typing import Any
except ImportError:
  Any = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

try:
  from typing import Self
except ImportError:
  Self = object

try:
  from typing import Callable
except ImportError:
  Callable = object

try:
  from typing import Never
except ImportError:
  try:
    from typing import NoReturn as Never
  except ImportError:
    Never = object


class ZeroMeta(type):
  """ZeroMeta is the metaclass for the Zero class. """

  def __new__(cls,
              name: str,
              bases: tuple[type, ...],
              namespace: dict[str, object]) -> type:
    return super().__new__(cls, name, bases, namespace)

  def __init__(cls, *__, **_) -> None:
    def _badNew(*_, **__) -> Never:
      raise TypeError('This class cannot be instantiated.')

    setattr(cls, '__new__', _badNew)

  def __call__(cls, *__, **_) -> Any:
    """Prevents instantiation of the class"""
    return cls


class THIS(metaclass=ZeroMeta):
  """THIS represents the not yet created class. """

  __ZERO_THIS__ = True


def thisFilterFactory(instance: object) -> Callable:
  """Getter-function for the 'THIS' filter."""

  def thisFilter(*args, **kwargs) -> Any:
    """Filter for the 'THIS' placeholder."""
    if args and kwargs:
      e = """The 'thisFilter' does not support combined positional and 
      keyword arguments!"""
      raise ValueError(monoSpace(e))
    if not args and not kwargs:
      return []
    if args:
      if len(args) == 1:
        if args[0] is THIS:
          return instance
        return args[0]
      out = []
      for arg in args:
        if arg is THIS:
          out.append(instance)
        else:
          out.append(arg)
      return out
    out = {}
    for key, value in kwargs.items():
      if value is THIS:
        out[key] = instance
      else:
        out[key] = value
    return out

  return thisFilter
