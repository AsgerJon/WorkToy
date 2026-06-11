"""
TypeSig encapsulates type signatures for overloads
"""
#  Apache-2.0 license
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
  is shared across every class body that uses it. Hashing such a
  'TypeSig' by its raw types alone would therefore collide between
  unrelated overloads, while the signature must still serve as a
  dict key during registration.

  The metaclass machinery provides a stand-in value instead.
  'AbstractNamespace.__init__' computes
  'hash((name, *baseNames, mcls.__name__))' (the same name tuple
  'AbstractMetaclass.__hash__' hashes once the class exists) and
  stores it on the namespace instance as '__hash_value__'.

  When 'TypeSig.__hash__' encounters 'THIS' or 'OWNER' in its raw
  types, it walks the call stack via '_findActiveNamespace' and
  picks up the '__hash_value__' and '__metaclass__' of the
  innermost class-body frame. It then substitutes 'THIS' with the
  stand-in value and 'OWNER' with the metaclass via
  'self(this=..., owner=...)' (see '__call__'), and hashes the
  substituted raw types. The resulting hash is stable for the whole
  class body and distinct between class bodies, which is all the
  registration dicts require.

  The stand-in hash is not required to equal the hash of the
  finished class, and nothing depends on such equality. Dicts keyed
  by sentinel-bearing signatures are filled and queried only while
  the class body executes. Once the class exists, 'swapTHIS'
  replaces the sentinel with the concrete class in place; from then
  on those dicts are only ever iterated, and the dispatcher compiles
  fresh lookup tables from the swapped signatures, which hash
  through the class itself.

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

  def getRawTypes(self) -> RawTypes:
    return self.__raw_types__

  @classmethod
  def _findActiveNamespace(cls) -> MaybeCtx:
    """
    The '_findActiveNamespace' method walks up the call stack looking
    for a class-body frame whose locals expose '__hash_value__' and
    '__metaclass__'. It returns the '(hashValue, metaclass)' pair of the
    innermost such frame, or None if no active class-body context is
    found.

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
    The 'fromArgs' constructor builds a 'TypeSig' from concrete values by
    taking the type of each argument in order. This is how the dispatcher
    derives the lookup key for an incoming call.

    Parameters
    ----------
    *args : Any
        The concrete call arguments whose types form the signature.

    Returns
    -------
    Self
        A 'TypeSig' of the argument types, in order.
    """
    return cls(*[type(arg) for arg in args], )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self, ) -> Iterator[type]:
    yield from self.getRawTypes()

  def __hash__(self, ) -> int:
    raw = self.getRawTypes()
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
      return hash(substituted.getRawTypes())
    return hash(raw)

  def __len__(self, ) -> int:
    return len(self.getRawTypes())

  def __contains__(self, type_: HASHABLE) -> bool:
    for rawType in self.getRawTypes():
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
    infoSpec = """<%s: %s>"""
    typeStr = '[%s]' % ', '.join(t.__name__ for t in self)
    clsName = type(self).__name__
    return textFmt(infoSpec % (clsName, typeStr))

  def __repr__(self) -> str:
    infoSpec = """%s(%s)"""
    typeStr = ', '.join(t.__name__ for t in self)
    return textFmt(infoSpec % (type(self).__name__, typeStr))

  def __call__(self, this: object = None, owner: type = None) -> Self:
    """
    Calling a 'TypeSig' returns a new 'TypeSig' with 'THIS' replaced by
    'this' and 'OWNER' replaced by 'owner'. Either argument can be
    omitted to leave the corresponding sentinel in place. '__hash__' uses
    this to substitute predicted-hash and metaclass values while a class
    is still under construction, and it is available externally as a
    primitive for any caller that needs a hashable copy without waiting
    for 'swapTHIS' to fire.

    Parameters
    ----------
    this : object, optional
        The value to substitute for the THIS sentinel.
    owner : type, optional
        The value to substitute for the OWNER sentinel.

    Returns
    -------
    Self
        A new 'TypeSig' with the requested substitutions applied and the
        same '__allow_flex__' flag.
    """
    newTypes = []
    for rawType in self.getRawTypes():
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
    """
    The 'swapTHIS' method replaces the THIS sentinel in the raw types
    with 'thisType' in place, called once the enclosing class exists so
    that '@overload(THIS)' resolves to the finished class.

    Parameters
    ----------
    thisType : type
        The class to substitute for the THIS sentinel.
    """
    newTypes = []
    for rawType in self.getRawTypes():
      if rawType is THIS:
        newTypes.append(thisType)
      else:
        newTypes.append(rawType)
    self.__raw_types__ = (*newTypes,)
