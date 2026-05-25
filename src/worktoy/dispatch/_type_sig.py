"""
TypeSig encapsulates type signatures for overloads
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from inspect import currentframe
from typing import TYPE_CHECKING

from ..core.sentinels import THIS, OWNER
from ..utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Self, Iterator, Union, Optional

  RawTypes: TypeAlias = tuple[type, ...]
  HASHABLE: TypeAlias = Union[type, int]
  ActiveCtx: TypeAlias = tuple[int, type]
  MaybeCtx: TypeAlias = Optional[ActiveCtx]


class TypeSig:
  """Hashable, ordered tuple of types used as a dispatch key.

  A 'TypeSig' represents the positional-argument type signature of a
  single overload. Equality and hashing are by type identity in the
  declared order, so 'TypeSig(int, str)' and 'TypeSig(str, int)' are
  distinct keys. The signature is iterable and supports 'len' and
  'in', the latter using identity comparison.

  The class-level flag '__allow_flex__' (default True) controls
  whether the SLOW path of the dispatcher is allowed to attempt
  'typeCast' conversions against this signature. 'overload.flex' and
  'Dispatcher.flex' set it to False on their generated signatures,
  since the permutation machinery already covers the flexibility
  they need.

  Use 'TypeSig.fromArgs(*args)' to derive a signature from concrete
  values (used by the dispatcher to look up a matching overload).
  Use 'swapTHIS(thisType)' to replace the 'THIS' sentinel with the
  enclosing class once the class is fully constructed; this is what
  lets '@overload(THIS)' work inside a class body.

  Hashing and the 'THIS' / 'OWNER' sentinels
  ------------------------------------------
  '@overload(THIS, ...)' registers a 'TypeSig' carrying the 'THIS'
  sentinel because the enclosing class does not yet exist at the
  moment the decorator runs. 'THIS' is a singleton, so its identity
  is shared across every class body that uses it; hashing such a
  'TypeSig' naively would either collide between unrelated overloads
  or corrupt downstream hash tables once 'swapTHIS' mutates the raw
  types after class construction.

  The metaclass machinery solves this by predicting the final class
  hash at namespace-creation time. 'AbstractNamespace.__init__'
  computes 'hash((name, *baseNames, mcls.__name__))' (the same
  formula 'AbstractMetaclass.__hash__' will produce once the class
  exists) and stores it on the namespace instance as
  '__hash_value__'.

  When 'TypeSig.__hash__' encounters 'THIS' or 'OWNER' in its raw
  types, it walks the call stack via '_findActiveNamespace' and
  picks up the '__hash_value__' and '__metaclass__' of the
  innermost class-body frame. It then substitutes 'THIS' with the
  predicted hash value and 'OWNER' with the metaclass via
  'self(this=..., owner=...)' (see '__call__'), and hashes the
  substituted raw types. Because tuple hashing combines
  'hash(element)' for each element, and CPython's
  'hash(int) == int' for the relevant range, the substituted hash
  matches the eventual concrete-class hash exactly. Dict invariants
  therefore survive the later in-place mutation by 'swapTHIS'.

  Using frame inspection rather than a global push/pop stack
  eliminates a real correctness problem: a class body that raises
  before reaching the metaclass's '__new__' would leak a stack
  entry (Python provides no hook between class-body failure and
  exception propagation). Frame walking has no global state to
  leak - a failed frame simply drops off the call stack on its own.

  Outside an active class-body context, '__hash__' raises
  'TypeError' - the same fail-loud guard, narrowed to actual
  misuse (code paths that bypass the metaclass and try to hash a
  sentinel-bearing 'TypeSig' on their own). Equality stays enabled
  unconditionally so that list-based dedup ('Dispatcher.addSigFunc'
  via '==') keeps working for sentinel-bearing signatures.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __raw_types__ = None
  __allow_flex__ = True

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getRawTypes(self) -> RawTypes:
    return self.__raw_types__

  @classmethod
  def _findActiveNamespace(cls) -> MaybeCtx:
    """Walk up the call stack looking for a class-body frame whose
    locals expose '__hash_value__' and '__metaclass__'. Returns the
    '(hashValue, metaclass)' pair of the innermost such frame, or
    'None' if no active class-body context is found.

    CPython treats class-body and module-body frames specially:
    'frame.f_locals' is the real namespace mapping that
    '__prepare__' returned, not a snapshot. For 'BaseSpace' (and
    any 'AbstractNamespace') instances, that means we can read
    '__hash_value__' and '__metaclass__' off the frame's locals
    directly.

    Using frame inspection rather than a class-level push/pop stack
    eliminates the leak-on-class-body-error problem: there is no
    global state to clean up, and any frame that errors out simply
    disappears from the call stack on its own."""
    curFrame = currentframe()
    if curFrame is None:
      return None
    frame = curFrame.f_back
    while frame is not None:
      ns = frame.f_locals
      hashValue = getattr(ns, '__hash_value__', None)
      metaclass = getattr(ns, '__metaclass__', None)
      if isinstance(hashValue, int) and isinstance(metaclass, type):
        return (hashValue, metaclass)
      frame = getattr(frame, 'f_back', None)
    return None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *rawTypes: type) -> None:
    self.__raw_types__ = rawTypes

  @classmethod
  def fromArgs(cls, *args, ) -> Self:
    """
    Create a TypeSig from the given arguments.
    """
    return cls(*[type(arg) for arg in args], )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self, ) -> Iterator[type]:
    yield from self._getRawTypes()

  def __hash__(self, ) -> int:
    raw = self._getRawTypes()
    if THIS in raw or OWNER in raw:
      ctx = type(self)._findActiveNamespace()
      if ctx is None:
        infoSpec = """'%s' containing 'THIS' or 'OWNER' is not
        hashable outside an active class-body context. The
        dispatcher only needs to hash such signatures during class
        construction; if this hash is being computed elsewhere,
        call 'swapTHIS' first to resolve the sentinel."""
        raise TypeError(textFmt(infoSpec % (type(self).__name__,)))
      hashValue, metaclass = ctx
      substituted = self(this=hashValue, owner=metaclass)
      return hash(substituted._getRawTypes())
    return hash(raw)

  def __len__(self, ) -> int:
    return len(self._getRawTypes())

  def __contains__(self, type_: HASHABLE) -> bool:
    for rawType in self._getRawTypes():
      if rawType is type_:
        return True
    return False

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, type(self)):
      return NotImplemented
    if len(self) != len(other):
      return False
    for this, that in zip(self, other):
      if this is not that:
        return False
    return True

  def __str__(self) -> str:
    """Returns a string representation of the type signature."""
    infoSpec = """<%s: %s>"""
    typeStr = '[%s]' % ', '.join(t.__name__ for t in self)
    clsName = type(self).__name__
    return textFmt(infoSpec % (clsName, typeStr))

  def __repr__(self) -> str:
    """Returns code that would recreate the type signature."""
    infoSpec = """%s(%s)"""
    typeStr = ', '.join(t.__name__ for t in self)
    return textFmt(infoSpec % (type(self).__name__, typeStr))

  def __call__(self, this: object = None, owner: type = None) -> Self:
    """Return a new 'TypeSig' with 'THIS' replaced by 'this' and
    'OWNER' replaced by 'owner'. Either kwarg can be omitted to
    leave the corresponding sentinel in place. Used by '__hash__'
    to substitute predicted-hash and metaclass values while a class
    is still under construction, and available externally as a
    primitive for any caller that needs a hashable copy without
    waiting for 'swapTHIS' to fire."""
    newTypes = []
    for rawType in self._getRawTypes():
      if rawType is THIS and this is not None:
        newTypes.append(this)
      elif rawType is OWNER and owner is not None:
        newTypes.append(owner)
      else:
        newTypes.append(rawType)
    new = type(self)(*newTypes)
    new.__allow_flex__ = self.__allow_flex__
    # noinspection PyTypeChecker
    return new

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def swapTHIS(self, thisType: type) -> None:
    newTypes = []
    for rawType in self._getRawTypes():
      if rawType is THIS:
        newTypes.append(thisType)
      else:
        newTypes.append(rawType)
    self.__raw_types__ = (*newTypes,)
