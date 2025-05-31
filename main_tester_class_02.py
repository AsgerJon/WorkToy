"""
lol
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Self, TypeAlias


class Foo:
  """
  L
  """

  @classmethod
  def __call__(cls, *args, **kwargs) -> Self:
    """
    L
    """
    infoSpec = """'__call__ received: cls: '%s', args: '%s', kwargs: '%s'"""
    clsStr = getattr(cls, '__name__', type(cls).__name__)
    argStr = ', '.join(map(str, args))
    kwargStr = ', '.join(f"{k}={v}" for k, v in kwargs.items())
    info = infoSpec % (clsStr, argStr, kwargStr)
    print(info)
    return cls
