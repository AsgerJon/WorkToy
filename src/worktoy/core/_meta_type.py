"""
MetaType is the meta-metaclass for the 'worktoy' library.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias

  Bases: TypeAlias = tuple[type, ...]
  Space: TypeAlias = dict[str, Any]


class MetaType(type):
  """
  MetaType provides the meta-metaclass for the 'worktoy' library. Every
  metaclass in 'worktoy' both subclasses 'MetaType' and has 'MetaType'
  as its own metaclass, so combining worktoy metaclasses does not raise
  a metaclass conflict.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(cls, ) -> str:
    return """%s[metaclass=%s]""" % (cls.__name__, cls.__class__.__name__)

  __repr__ = __str__

  #  The 'mmcls' parameter refers this being a meta-metaclass
  #  noinspection PyMethodParameters
  def __new__(mmcls, name: str, bases: Bases, space: Space, **kw) -> type:
    """
    Creates a new class with the given name, bases and namespace.
    """
    if '__namespace__' not in space:
      space['__namespace__'] = space
    return super().__new__(mmcls, name, bases, space, **kw)
