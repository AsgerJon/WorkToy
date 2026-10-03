"""
DuplicateSignature is raised when a second function is registered under
a 'TypeSig' that a 'Dispatcher' already holds.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt, NoPickle

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeAlias, Union

  from worktoy.dispatch import TypeSig

  Method: TypeAlias = Callable[..., Any]


class DuplicateSignature(NoPickle, TypeError):
  """
  DuplicateSignature is raised when a 'Dispatcher' receives a second
  function registration under a 'TypeSig' it already has on file. A
  second fallback or a second finalizer raises it too, whether a class
  body registers it under one name or it is set on a 'Dispatcher' by
  hand, with the role in place of the signature, since neither has one.

  Attributes
  ----------
  sig: TypeSig or str
    The signature that was registered twice, or the role, 'fallback' or
    'finalizer', registered twice.
  existing: Callable
    The function already registered under 'sig'.
  duplicate: Callable
    The function whose registration was rejected.
  """

  __slots__ = ('sig', 'existing', 'duplicate')

  def __init__(
      self, sig: Union[TypeSig, str], existing: Method, duplicate: Method,
  ) -> None:
    self.sig = sig
    self.existing = existing
    self.duplicate = duplicate
    TypeError.__init__(self, )

  def __str__(self) -> str:
    if isinstance(self.sig, str):
      infoSpec = """'Dispatcher' already has a %s function registered:
      <br>existing function: <br><tab>%s<br>rejected duplicate:
      <br><tab>%s"""
      existingStr = str(self.existing)
      duplicateStr = str(self.duplicate)
      info = infoSpec % (self.sig, existingStr, duplicateStr)
      return textFmt(info)
    infoSpec = """'Dispatcher' already has a function registered under
    type signature: <br><tab>%s<br>existing function: <br><tab>%s<br>
    rejected duplicate: <br><tab>%s"""
    sigStr = str(self.sig)
    existingStr = str(self.existing)
    duplicateStr = str(self.duplicate)
    info = infoSpec % (sigStr, existingStr, duplicateStr)
    return textFmt(info)

  __repr__ = __str__
