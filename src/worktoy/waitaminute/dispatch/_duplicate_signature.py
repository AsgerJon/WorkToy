"""
DuplicateSignature is raised when a second function is registered under
a 'TypeSig' that a 'Dispatcher' already holds.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeAlias

  from worktoy.dispatch import TypeSig

  Method: TypeAlias = Callable[..., Any]


class DuplicateSignature(TypeError):
  """
  DuplicateSignature is raised when a 'Dispatcher' receives a second
  function registration under a 'TypeSig' it already has on file.

  Attributes
  ----------
  sig: TypeSig
    The signature that was registered twice.
  existing: Callable
    The function already registered under 'sig'.
  duplicate: Callable
    The function whose registration was rejected.
  """

  __slots__ = ('sig', 'existing', 'duplicate')

  def __init__(
      self, sig: TypeSig, existing: Method, duplicate: Method,
  ) -> None:
    self.sig = sig
    self.existing = existing
    self.duplicate = duplicate
    TypeError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """'Dispatcher' already has a function registered under
    type signature: <br><tab>%s<br>existing function: <br><tab>%s<br>
    rejected duplicate: <br><tab>%s"""
    sigStr = str(self.sig)
    existingStr = str(self.existing)
    duplicateStr = str(self.duplicate)
    info = infoSpec % (sigStr, existingStr, duplicateStr)
    return textFmt(info)

  __repr__ = __str__
