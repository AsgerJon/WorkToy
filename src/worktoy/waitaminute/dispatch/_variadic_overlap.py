"""
VariadicOverlap is raised when two variadic declarations under one name
both accept the same call and nothing says which function receives it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt
from . import DuplicateSignature

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeAlias

  from worktoy.dispatch import TypeSig

  Method: TypeAlias = Callable[..., Any]


class VariadicOverlap(DuplicateSignature):
  """
  VariadicOverlap is raised as a class is created when two variadic
  declarations under one name, of different functions, both accept the
  same call by exact type, and no explicit declaration says which
  function receives it. Two declarations sharing a prefix both accept the
  call of the prefix alone: 'f(1)' matches '@overload(int, ARGS[str])'
  and '@overload(int, ARGS[int])' alike, and two without a prefix both
  accept the empty call. It subclasses 'DuplicateSignature', whose 'sig'
  is that shared signature, 'existing' the function of the declaration
  registered first and 'duplicate' that of the second. The message names
  the two declarations as written, since neither wrote the shared
  signature, and the way to settle the call: the shared signature
  declared explicitly on the function meant to receive it. Two
  declarations of one inner type, such as '@overload(ARGS[int])' beside
  '@overload(int, ARGS[int])', share every longer call as well, which no
  explicit declaration settles, and the message says so instead.

  Attributes
  ----------
  overloadName : str
    The overloaded name both declarations belong to.
  firstSig : TypeSig
    The variadic declaration registered first, as written.
  secondSig : TypeSig
    The variadic declaration registered second, as written.
  """

  __slots__ = ('overloadName', 'firstSig', 'secondSig')

  def __init__(
      self,
      overloadName: str,
      firstSig: TypeSig,
      secondSig: TypeSig,
      sig: TypeSig,
      existing: Method,
      duplicate: Method,
  ) -> None:
    self.overloadName = overloadName
    self.firstSig = firstSig
    self.secondSig = secondSig
    DuplicateSignature.__init__(self, sig, existing, duplicate)

  def _sameInner(self) -> bool:
    """
    The '_sameInner' method reports whether the two declarations take the
    same inner type, and so share every call longer than the shared one
    as well.
    """
    firstInner = self.firstSig.getRawTypes()[-1].__inner_type__
    secondInner = self.secondSig.getRawTypes()[-1].__inner_type__
    return True if firstInner is secondInner else False

  def __str__(self) -> str:
    infoSpec = """The variadic declarations %s and %s of '%s' both accept
    a call of %s, and no explicit declaration says which function
    receives it:<br>first declared on:<br><tab>%s<br>then on:<br><tab>%s
    <br>%s"""
    first, second, shared = self.firstSig, self.secondSig, self.sig
    if self._sameInner():
      advice = """The two take the same type after their prefixes, so
      they share every longer call as well, which no explicit
      declaration settles."""
    else:
      advice = """Declare %s explicitly on the function meant to receive
      such a call.""" % (shared,)
    info = infoSpec % (
        first, second, self.overloadName, shared, self.existing,
        self.duplicate, advice,
    )
    return textFmt(info)

  __repr__ = __str__
