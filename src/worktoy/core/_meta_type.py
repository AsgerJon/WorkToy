"""
MetaType provides the meta-metaclass for the 'worktoy' library. All
metaclasses used across the library both derive from and base on this
class. This is necessary to prevent metaclass conflicts.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type, TypeVar, TypeAlias, Union, Self

  Bases: TypeAlias = tuple[type, ...]
  Namespace: TypeAlias = dict[str, Any]
  NamespaceClass: TypeAlias = Union[Self, Type[Namespace]]

  Meta: TypeAlias = Type[type]
  MetaMeta: TypeAlias = Type[Meta]


class _Space:
  """
  Private descriptor class providing the namespace for the namespace
  object class used by the metaclass.
  """

  def __get__(self, mcls: Meta, mmcls: MetaMeta, ) -> Any:
    if mcls is None:
      return self
    if not hasattr(mcls, '__prepare__'):
      return None
    testSpace = mcls.__prepare__('test', (), )
    return type(testSpace)


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
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(cls, ) -> str:
    """Returns the name of the class. """
    return """%s[metaclass=%s]""" % (cls.__name__, cls.__class__.__name__)

  __repr__ = __str__
