"""
KeeFlags enumerates every combination of a set of single-bit flags.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt
from ..waitaminute import DeprecatedPromise
from ..waitaminute.keenum import KeeWriteOnceError, KeeResolveError
from . import Kee, KeeFlagsMeta

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Callable, Iterator, Never, Optional, Self

#  The description of the deprecation of the bit mask of a member.
_MASK = """The bit mask belongs to the class, not to the member: 'Flags[x]'
gives the member of mask 'x', and iterating 'Flags' gives its members in
the order of their masks."""


class KeeFlags(metaclass=KeeFlagsMeta, _root=True):
  """
  Base class for bitmask-flag enumerations. A subclass declares its
  flags in its body with 'Kee', as 'READ = Kee[str]()', and the
  metaclass gives the class one member per combination of its flags.

    class UserPermission(KeeFlags):
      READ = Kee[str]()
      EXEC = Kee[str]()

    class AdminPermission(KeeFlags):
      WRITE = Kee[str]()
      DEL = Kee[str]()

    class Permission(UserPermission, AdminPermission):
      pass

  Every member is a combination of flags. A flag is the combination of
  itself, and 'NULL', which this root builds, is the one member that
  combines none, inherited by every flags class.

  Cost (read before declaring a large enum)
  -----------------------------------------

  A flags class with N flags holds 2 ** N members and builds those no
  other class built for the same flags, each with its name, the names of
  its flags and its hash worked out once. Measured on one desktop
  machine under Python 3.15, the class statement of a class of fresh
  flags took:

      N =  8   -> 256 members         about a millisecond
      N = 12   -> 4096 members        about 15 milliseconds
      N = 16   -> 65,536 members      about 0.3 seconds, and 72 MB

  The cost is paid once, at import, and grows four times for every two
  flags added. Every lookup is one step whatever N is: by mask, by name
  in any case and order, by value when every value hashes, and through
  the operators.

  Members shared along the lineage
  --------------------------------

  A flags class holds the flags of its bases first, in the order of the
  bases, and its own after them. One member stands for each set of flags
  in the whole process, so a class holds the very members of its bases,
  'Extended.READ is Permission.READ', and a combination of flags of two
  bases is built by the first class combining them and bound by every
  later one. A member belongs to the class that built it: its 'flags'
  are those of that class, its 'lows' the flags of that class that are
  low in it, and its value comes from the '_getValue' of that class.

  Member attributes
  -----------------

  - 'name': the flag names joined by '_' in the order of the class that
    built it, or 'NULL'. A class binds each member at the name joining
    its flags in its own order.
  - 'names': a frozenset of the names of the high flags.
  - 'highs': the flags that are high in the member, the flag members
    themselves; iterating a member gives them.
  - 'lows': the flags of the class that built the member that are low.
  - 'flags': the flags of the class that built the member.
  - 'value': the value of a flag declared with a 'Kee' is that of the
    'Kee', so 'Kee[str]()' gives the name; every other member is valued
    by its name. A subclass reimplements '_getValue' to give the members
    it builds other values; it is read once per member, after the class
    has its flags. 'valueType' is the type of the value of the first
    flag of the class, and no combination may contain a member whose
    value is not an instance of it: every flag of a class shares the
    type, while the value of a combination is free, and 'NULL' is
    exempt, since it contains no member.
  - 'kee': the declaration of a flag, or None for any other member.
  - 'owners': the flags classes holding the member, in order of
    creation.
  - 'index': deprecated, the bit mask of the member in the class that
    built it.

  Equality is identity, and a member hashes by the names of its flags.
  '|', '&' and '^' give the member of the resulting set of flags, and
  refuse with 'TypeError' when no class holds that set. '~member' is the
  member whose flags are the lows of 'member'; '~NULL' raises
  'ZeroDivisionError', since there is no universal combination to invert
  to. 'NULL' is falsy and every other member truthy.

  Like 'KeeNum' members, the members are write-once constants: any
  attempt to set or delete an attribute on a member raises
  'KeeWriteOnceError', as does rebinding or deleting the member name on
  the owning class. The constructor writes past that with
  'object.__setattr__'. A copy of a member is the member, and a member
  pickles as a lookup of its name on the class that built it. The text
  of a member is no promise: it currently names its one owner,
  '<Permission>.READ', or the root once several classes hold it,
  '<KeeFlags>.READ'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables (type hints)
  __member_list__: list[Self]
  __member_dict__: dict[frozenset[str], Self]
  __flag_order__: tuple[Self, ...]

  #  Private Variables
  __field_owner__ = None
  __field_name__ = None
  __member_hash__: Optional[int] = None
  __member_flags__: tuple = ()
  __member_index__: Optional[int] = None
  __member_owners__: Optional[list] = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getFlagsFromType(self, ) -> list[Self]:
    """
    The 'flags' of a member are those of the class that built it, which
    the metaclass gives the class as 'flags'.
    """
    return type(self).flags

  def _getValue(self) -> Any:
    """
    The value of a member is what a project reads off it, and what the
    class resolves a member from. A flag declared with a 'Kee' is valued
    as the 'Kee' is, so 'Kee[str]()' gives the name, and every other
    member is valued by its name. A subclass reimplements this method to
    give the members it builds any other object; it is read once per
    member, after the class has its flags. Several members may share one
    value, in which case the lowest-indexed member answers for it.
    """
    if isinstance(self.kee, Kee):
      return self.kee.getValue()
    return self.name

  def _getHighs(self) -> Iterator[Self]:
    yield from self.__member_flags__

  def _getLows(self) -> Iterator[Self]:
    highs = self.__member_flags__
    for flag in type(self).__flag_order__:
      if not any(flag is high for high in highs):
        yield flag

  def _readIndex(self) -> int:
    """
    The 'index' of a member is deprecated: the bit mask belongs to the
    class, which answers 'Flags[x]', not to the member. A read still
    gives the mask in the class that built the member, with a
    'DeprecatedPromise' at the line that read it.
    """
    DeprecatedPromise('worktoy.keenum.KeeFlags.index', textFmt(_MASK)).warn()
    return self.__member_index__

  def _getOwners(self) -> tuple[type, ...]:
    return (*self.__member_owners__,)

  flags = property(_getFlagsFromType)
  lows = property(_getLows)
  highs = property(_getHighs)
  index = property(_readIndex)
  owners = property(_getOwners)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __cast_as__(cls, value: Any) -> Any:
    """
    The '__cast_as__' hook lets 'typeCast' resolve a value to the member
    it identifies, as calling the class does: a member passes, a name in
    any case and order, a tuple of names, a mask or a value resolves,
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
    A member pickles as a lookup of its name on the class that built it,
    so it unpickles as the member itself.
    """
    return getattr, (type(self), self.name)

  def __bool__(self) -> bool:
    """'NULL', which combines no flags, is falsy. Every other member is
    truthy, mirroring the truthiness of the underlying bitmask."""
    return True if self.__member_flags__ else False

  def __iter__(self) -> Iterator[Self]:
    yield from self.highs

  def __str__(self, ) -> str:
    """
    The text names the one class holding the member, or the root once
    several do. It is no promise.
    """
    owners = self.__member_owners__
    if len(owners) == 1:
      return '<%s>.%s' % (owners[0].__name__, self.name)
    root = type(type(self)).__kee_class__
    return '<%s>.%s' % (root.__name__, self.name)

  __repr__ = __str__

  def __hash__(self, ) -> int:
    return self.__member_hash__

  def _combine(self, other: Any, merge: Callable) -> Any:
    """
    The operators work on the flags of the two members alone, so neither
    class has a say: the result is the member of the resulting set of
    flags, whichever class built it, or 'NotImplemented' when 'other' is
    no flags member or no class holds that set.
    """
    if not isinstance(type(other), KeeFlagsMeta):
      return NotImplemented
    mine = frozenset(self.__member_flags__)
    theirs = frozenset(other.__member_flags__)
    return KeeFlagsMeta._findCombination(merge(mine, theirs))

  def __or__(self, other: Any) -> Any:
    return self._combine(other, frozenset.union)

  def __and__(self, other: Any) -> Any:
    return self._combine(other, frozenset.intersection)

  def __xor__(self, other: Any) -> Any:
    return self._combine(other, frozenset.symmetric_difference)

  #  The three operators commute, so the reflected forms are the same.
  __ror__ = __or__
  __rand__ = __and__
  __rxor__ = __xor__

  def __invert__(self, ) -> Self:
    """
    The inverse of a member is the member whose flags are its lows, the
    flags of the class that built it that are low in it. 'NULL' combines
    no flags and belongs to no class with flags, so it has no inverse.
    """
    if not self.__member_flags__:
      info = """'NULL' combines no flags, and there is no universal
      combination for it to invert to."""
      raise ZeroDivisionError(textFmt(info))
    return KeeFlagsMeta._findCombination(frozenset(self.lows))

  def __int__(self) -> int:
    """
    'int(member)' gives the deprecated bit mask, with a
    'DeprecatedPromise'; see '_readIndex'.
    """
    info = textFmt(_MASK)
    DeprecatedPromise('worktoy.keenum.KeeFlags.__int__', info).warn()
    return self.__member_index__

  def __index__(self) -> int:
    """
    A member used as an index gives the deprecated bit mask, with a
    'DeprecatedPromise'; see '_readIndex'.
    """
    info = textFmt(_MASK)
    DeprecatedPromise('worktoy.keenum.KeeFlags.__index__', info).warn()
    return self.__member_index__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, highs: tuple, mask: int, kee: Any = None) -> None:
    """
    A member stores its high flags, its bit mask in the class building
    it, its canonical name, the names of its flags, its hash and its
    declaration as plain attributes. A flag, given its declaration, is
    the combination of itself and takes the name of the declaration. The
    value is settled by the metaclass through '_settleValue' once the
    class has its flags.
    """
    if kee is None:
      name = str.join('_', [flag.name for flag in highs]) or 'NULL'
    else:
      name = kee.name
      highs = (self,)
    object.__setattr__(self, 'name', name)
    object.__setattr__(self, 'kee', kee)
    object.__setattr__(self, '__member_flags__', highs)
    object.__setattr__(self, '__member_index__', mask)
    object.__setattr__(self, '__member_owners__', [])
    names = frozenset(flag.name for flag in highs)
    object.__setattr__(self, 'names', names)
    object.__setattr__(self, '__member_hash__', hash(names))
    object.__setattr__(self, '__field_owner__', type(self))
    object.__setattr__(self, '__field_name__', name)

  def _settleValue(self) -> None:
    """
    The metaclass reads the value once, after the class building the
    member has all its flags, since a '_getValue' may read the lows.
    """
    object.__setattr__(self, 'value', self._getValue())

  def _addOwner(self, cls: type) -> None:
    """
    The metaclass records each flags class holding the member as it binds
    it. The list is changed in place, which the frozen member allows,
    since nothing is assigned.
    """
    self.__member_owners__.append(cls)
