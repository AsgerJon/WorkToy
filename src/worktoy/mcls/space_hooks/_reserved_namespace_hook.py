"""
ReservedNameHook protects reserved names from being overridden.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...waitaminute.meta import ReservedName
from . import AbstractSpaceHook, ReservedNames, SpaceDesc

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias
  from .. import AbstractNamespace

  Names: TypeAlias = tuple[str, ...]


class ReservedNamespaceHook(AbstractSpaceHook):
  """
  ReservedNamespaceHook prevents redefinition of names that are reserved
  for use by Python or the metaclass system. These names are typically
  populated automatically during class construction and must not be
  reassigned by user code.

  Protected names
  ---------------
  '__dict__'              Internal attribute dictionary
  '__weakref__'           Weak reference support slot
  '__module__'            Name of the module defining the class
  '__annotations__'       Type hint storage
  '__match_args__'        Structural pattern matching
  '__doc__'               Docstring
  '__name__'              Class name
  '__qualname__'          Fully qualified class name
  '__firstlineno__'       Source line for class definition
  '__static_attributes__' Internal metadata used by the metaclass

  Behavior
  --------
  During namespace population (when a class body assigns names), any
  attempt to override a name in the reserved list raises a
  'ReservedName' exception, but only if the name already exists in the
  namespace. This prevents accidental clobbering of values while still
  allowing deferred initialization.

  Usage
  -----
  To use 'ReservedNamespaceHook', declare it in your namespace class:

      class Space(AbstractNamespace):
        reservedNameHook = ReservedNamespaceHook()
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public variables
  space: SpaceDesc[AbstractNamespace] = SpaceDesc()
  reservedNames: ReservedNames = ReservedNames()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    Called before a name is set in the namespace. Raises
    'ReservedName' when 'key' is a reserved name that is already
    present in the namespace; otherwise returns False.
    """
    if key in self.reservedNames and key in self.space:
      raise ReservedName(key)
    return False
