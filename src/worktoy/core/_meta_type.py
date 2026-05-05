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
  from typing import Any, Type, TypeAlias, Union, Self

  Bases: TypeAlias = tuple[type, ...]
  Space: TypeAlias = dict[str, Any]
  NamespaceClass: TypeAlias = Union[Self, Type[Space]]

  Meta: TypeAlias = Type[type]
  MetaMeta: TypeAlias = Type[Meta]


class _Space:
  """
  Private descriptor class providing the namespace for the namespace
  object class used by the metaclass.
  """

  __field_name__ = None
  __field_owner__ = None

  def __get__(self, mcls: type, mmcls: type, ) -> Any:
    if mcls is None:
      if mmcls is self.__field_owner__:
        return self
      return self.__get__(mmcls, mmcls)
    testSpace = mcls.__prepare__('test', (), )
    return type(testSpace)

  def __set_name__(self, owner: type, name: str) -> None:
    """
    Sets the name of the descriptor in the owner class.
    """
    self.__field_name__ = name
    self.__field_owner__ = owner


class MetaType(type):
  """
  MetaType provides the meta-metaclass for the 'worktoy' library. All
  metaclasses used across the library both derive from and base on this
  class. This is necessary to prevent metaclass conflicts.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __namespace_class__ = None

  #  Virtual Variables
  namespaceClass = _Space()

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
    validatedSpace: dict = mmcls._fromErrata(space)
    return super().__new__(mmcls, name, bases, validatedSpace, **kw)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _fromErrata(space: Space) -> dict[str, Any]:
    notations = space.get('__annotations__', dict())
    for key, value in space.items():
      if isinstance(value, type):
        if value.__name__ == '__Errata__':
          samizdat = getattr(value, '__annotations__', dict())
          break
    else:
      return space
    for name, truth in samizdat.items():
      notations[name] = truth
    space['__annotations__'] = notations
    del space[key]
    return space
