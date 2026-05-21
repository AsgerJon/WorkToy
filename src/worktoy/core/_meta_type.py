"""
MetaType provides the meta-metaclass for the 'worktoy' library. All
metaclasses used across the library both derive from and base on this
class. This is necessary to prevent metaclass conflicts.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias

  Bases: TypeAlias = tuple[type, ...]
  Space: TypeAlias = dict[str, Any]


class MetaType(type):
  """
  MetaType provides the meta-metaclass for the 'worktoy' library. All
  metaclasses used across the library both derive from and base on this
  class. This is necessary to prevent metaclass conflicts.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(cls, ) -> str:
    """Returns the name of the class. """
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
    validatedSpace = mmcls._mergeErrata(space)
    return super().__new__(mmcls, name, bases, validatedSpace, **kw)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _mergeErrata(space: Space) -> Space:
    """If the class body declared a nested '__Errata__' class, merge its
    annotations into the outer class's '__annotations__' and remove the
    nested class from the namespace.

    See 'keenum._kee_meta.KeeMeta.__Errata__' for the canonical use:
    declaring phantom annotations a type-checker can see without putting
    them in the real class body."""
    errata = space.pop('__Errata__', None)
    if errata is None:
      return space
    notations = space.get('__annotations__', dict())
    notations.update(getattr(errata, '__annotations__', dict()))
    space['__annotations__'] = notations
    return space
