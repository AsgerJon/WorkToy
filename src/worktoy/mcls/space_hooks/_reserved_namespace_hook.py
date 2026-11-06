"""
ReservedNamespaceHook protects reserved names from being overridden.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...waitaminute.meta import ReservedName
from . import AbstractSpaceHook, ReservedNames

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class ReservedNamespaceHook(AbstractSpaceHook):
  """
  Python places names such as '__module__', '__qualname__' and '__doc__'
  in the namespace as the class body starts, and gives a class others,
  such as '__orig_bases__'. A class body binding one of them again, as
  "__module__ = 'other'", quietly breaks what relies on it, and must fail
  at that line instead.

  Implementation
  --------------

  'setItemPhase' raises 'ReservedName', a 'SyntaxError', when a name of
  'ReservedNames' is bound while the namespace holds it already, which
  lets the first binding, the interpreter's own, through.

  Attributes
  ----------

  reservedNames : tuple[str, ...]
    The protected names.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public variables
  reservedNames: ReservedNames = ReservedNames()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    if key in self.reservedNames and key in self.space:
      raise ReservedName(key)
    return False
