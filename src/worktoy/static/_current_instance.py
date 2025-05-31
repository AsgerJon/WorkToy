"""_CurrentInstance is a private method used by AbstractObject to expose
the current owning instance of the descriptor instance."""
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
  from typing import Any, Never

  from . import AbstractObject


class _CurrentInstance:
  """_CurrentInstance is a private method used by AbstractObject to
  expose
  the current owning instance of the descriptor instance."""

  def __get__(self, desc: Any, owner: type) -> Any:
    """Return the current owning instance of the descriptor instance."""
    if desc is None:
      return self
    if TYPE_CHECKING:
      assert isinstance(desc, AbstractObject)
    return desc.__current_instance__

  def __set__(self, *_) -> Never:
    """This should never happen."""
    raise RuntimeError

  def __delete__(self, *_) -> Never:
    """This should never happen."""
    raise RuntimeError
