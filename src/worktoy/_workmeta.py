"""The WorkMeta eliminates the weird behaviour of builtin  types when we
subclass them. """
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any


class _WorkMetaClass(type):

  def __call__(cls, *args, **kwargs) -> Any:
    instance = cls.__new__(cls)
    instance.__init__(*args, **kwargs)
    return instance


class WorkMeta(metaclass=_WorkMetaClass):
  """Subclass this class along with a builtin type to achieve normal
  behaviour."""
  pass
