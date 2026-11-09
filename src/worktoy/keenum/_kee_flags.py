"""
KeeFlags enumerates every combination of a set of single-bit flags.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt
from ..waitaminute.keenum import KeeWriteOnceError, KeeResolveError
from . import KeeFlag, KeeFlagsMeta

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Iterator, Never, Optional, Self


class KeeFlags(metaclass=KeeFlagsMeta, _root=True):
  """
  Base class for bitmask-flag enumerations. Each KeeFlags subclass
  declares 'KeeFlag()' fields in its body, one per single-bit flag;
  the metaclass then materializes every combination of those flags as
  a concrete member at class-creation time.

  Cost (read before declaring a large enum)
  -----------------------------------------

  A KeeFlags class with N single-bit flags materializes 2 ** N
  members eagerly during class definition, each with its name, the
  names of its flags and its hash worked out once. Measured on one
  desktop machine under Python 3.15, the class statement took:

      N =  8   -> 256 members         about a millisecond
      N = 12   -> 4096 members        about 15 milliseconds
      N = 16   -> 65,536 members      about 0.3 seconds, and 72 MB

  The cost is paid once, at import, and grows four times for every two
  flags added. Every lookup is one step whatever N is: by index, by
  name in any case and order, by value when every value hashes, and
  through the operators.

  Member attributes
  -----------------

  - 'flags': all single-bit flags declared on the class (mirrors the
    class-level 'flags'; not member-specific).
  - 'highs': the flags that are HIGH for the member.
  - 'lows': the flags that are LOW for the member.
  - 'names': a frozenset of the names of the HIGH flags.
  - 'index' / 'value': the member's bitmask integer (value defaults
    to the index). A subclass reimplements '_getValue' to give its
    members other values; it is read once per member, as the class is
    created.
  - 'name': the canonical name, the HIGH flag names joined by '_', or
    'NULL' when no flag is HIGH.

  Naming and lookup
  -----------------

  A combined member's canonical name joins its HIGH flag names in
  declaration order ('FileAccess.READ_EXECUTE', never
  'FileAccess.EXECUTE_READ'), and attribute access resolves only that
  canonical name. Subscripting and calling are order- and
  case-insensitive: 'cls["EXECUTE_READ"]', 'cls["execute_read"]', and
  'cls["READ", "EXECUTE"]' all resolve to the same member, a repeated name
  collapses, and an unknown name raises 'KeeResolveError', as an unknown
  index or value does and as a 'KeeNum' miss does. Since '_' joins the
  flag names in a canonical name, a flag name may not contain '_' itself;
  declaring one raises 'KeeFlagNameError' in the class body.

  Members across a lineage
  ------------------------

  A flags class based on another holds the flags of its base first and
  members of its own, so no member object is shared between the two.
  Across the lineage a member is identified by the names of its high
  flags: a member of the base or of the subclass is equal to the member
  here with the same flags and hashes alike, resolves through a call, a
  subscript or 'typeCast' to this class's own member when this class
  holds every one of its flags, and is refused with 'KeeResolveError'
  otherwise, is in the class exactly when such a member exists, and
  takes part in the operators, where the class of the left operand
  answers when it holds every flag and the class of the right one
  answers through the reflected operator otherwise. Members of
  unrelated flags classes are strangers to each other.

  Like 'KeeNum' members, the members are write-once constants: any
  attempt to set or delete an attribute on a member raises
  'KeeWriteOnceError', as does rebinding or deleting the member name on
  the owning class. The constructor writes past that with
  'object.__setattr__'. A member needing extra attributes should come
  from a subclass declaring them.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables (type hints)
  __member_list__: list[Self]
  __member_dict__: dict[frozenset[str], Self]

  #  Private Variables
  __field_owner__ = None
  __field_name__ = None
  __member_hash__: Optional[int] = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getFlagsFromType(self, ) -> Any:
    """
    The 'KeeFlagsMeta' metaclass provides the helpful 'flags' descriptor
    allowing inspection of all the flags available. The descriptor is then
    available on the subclasses of 'KeeFlags', but *not* on the
    instances themselves. Therefore, the 'KeeFlags' class mirrors it.
    """
    return type(self).flags

  def _getValue(self) -> Any:
    """
    The value of a member is what a project reads off it, and what the
    class resolves a member from. The base gives every member its index
    as its value; a subclass reimplements this method to give any object
    from any member, as 'FileAccess' in the tests gives bytes. It is read
    once per member, as the class is created. Values of one immutable
    type are recommended, not required, and several members may share
    one value, in which case the lowest-indexed member answers for it.
    """
    return self.index

  def _getLows(self) -> Iterator[KeeFlag]:
    index = self.index
    for flag in type(self).__flag_clones__:
      if not index & (1 << flag.index):
        yield flag

  def _getHighs(self) -> Iterator[KeeFlag]:
    index = self.index
    for flag in type(self).__flag_clones__:
      if index & (1 << flag.index):
        yield flag

  flags = property(_getFlagsFromType)
  lows = property(_getLows)
  highs = property(_getHighs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __cast_as__(cls, value: Any) -> Any:
    """
    The '__cast_as__' hook lets 'typeCast' resolve a value to the member
    it identifies, as calling the class does: a member passes, a name in
    any case and order, a tuple of names, an index or a value resolves,
    and one the class cannot resolve is declined with 'NotImplemented',
    so 'typeCast' raises its own refusal and an 'AttriBox' over the
    class, or an overload naming it, refuses it as any value it cannot
    convert. While the metaclass still builds the members, nothing is
    resolved.
    """
    if cls.__allow_instantiation__:
      return NotImplemented
    try:
      return cls(value)
    except KeeResolveError:
      return NotImplemented

  def __setattr__(self, name: str, value: Any) -> Never:
    """
    A member is frozen once built, so every assignment raises
    'KeeWriteOnceError'; the constructor writes with
    'object.__setattr__'.
    """
    raise KeeWriteOnceError(self, name)

  def __delattr__(self, name: str) -> Never:
    """
    No stage of member construction deletes an attribute, so deletion
    raises 'KeeWriteOnceError' unconditionally.
    """
    raise KeeWriteOnceError(self, name)

  def __copy__(self) -> Self:
    """A member is a singleton, so a copy is the member itself. A fresh
    instance would break identity checks such as 'member is cls.NULL'."""
    return self

  def __deepcopy__(self, memo: Any) -> Self:
    """A member is a singleton, so a deep copy is the member itself,
    keeping a member carried inside a deep-copied structure identical to
    the canonical member."""
    return self

  def __reduce__(self) -> tuple:
    """
    A member pickles as a lookup of its canonical name on its class, so
    it unpickles as the member itself.
    """
    return getattr, (type(self), self.name)

  def __bool__(self) -> bool:
    """The NULL member (no flags HIGH) is falsy. Any member with at
    least one flag HIGH is truthy, mirroring the truthiness of the
    underlying bitmask."""
    return True if self.index else False

  def __iter__(self) -> Iterator[KeeFlag]:
    yield from self.highs

  def __str__(self, ) -> str:
    infoSpec = """%s.%s [%d]"""
    clsName = type(self).__name__
    info = infoSpec % (clsName, self.name, self.index)
    return textFmt(info)

  __repr__ = __str__

  def __eq__(self, other: Any) -> bool:
    cls, otherCls = type(self), type(other)
    if otherCls is cls:
      return True if self is other else False
    if not isinstance(otherCls, KeeFlagsMeta):
      return NotImplemented
    if issubclass(otherCls, cls) or issubclass(cls, otherCls):
      return True if self.names == other.names else False
    return NotImplemented

  def __hash__(self, ) -> int:
    return self.__member_hash__

  def _asOwn(self, other: Any) -> Any:
    """
    An operator takes a member of this class or of a related one, and
    works on the member of this class with the other's flags; anything
    else, a member of an unrelated class or a member with a flag this
    class lacks, gives 'None', so the operator answers 'NotImplemented'
    and Python asks the other operand.
    """
    cls = type(self)
    if type(other) is cls:
      return other
    if not isinstance(type(other), KeeFlagsMeta):
      return None
    return cls._fromMember(other)

  def __or__(self, other: Any) -> Any:
    own = self._asOwn(other)
    if own is None:
      return NotImplemented
    return type(self).__member_list__[self.index | own.index]

  def __and__(self, other: Any) -> Any:
    own = self._asOwn(other)
    if own is None:
      return NotImplemented
    return type(self).__member_list__[self.index & own.index]

  def __xor__(self, other: Any) -> Any:
    own = self._asOwn(other)
    if own is None:
      return NotImplemented
    return type(self).__member_list__[self.index ^ own.index]

  #  The three operators commute, so the reflected forms are the same.
  __ror__ = __or__
  __rand__ = __and__
  __rxor__ = __xor__

  def __invert__(self, ) -> Self:
    members = type(self).__member_list__
    return members[(len(members) - 1) ^ self.index]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, index: int) -> None:
    """
    The member of the bit mask 'index' stores its index, the names of its
    high flags, its canonical name, its hash and its value as plain
    attributes, with its class and name as '__field_owner__' and
    '__field_name__'.
    """
    object.__setattr__(self, 'index', index)
    highNames = [flag.name for flag in self.highs]
    names = frozenset(highNames)
    name = '_'.join(highNames) or 'NULL'
    object.__setattr__(self, 'names', names)
    object.__setattr__(self, 'name', name)
    object.__setattr__(self, '__member_hash__', hash(names))
    object.__setattr__(self, '__field_owner__', type(self))
    object.__setattr__(self, '__field_name__', name)
    object.__setattr__(self, 'value', self._getValue())
