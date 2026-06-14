"""
KeeFlags enumerates every combination of a set of single-bit flags.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..desc import Field
from ..utilities import textFmt
from ..waitaminute import MissingVariable, TypeException
from ..waitaminute.keenum import KeeWriteOnceError
from . import KeeFlag, KeeFlagsMeta

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator, Never, Self


class KeeFlags(metaclass=KeeFlagsMeta):
  """
  Base class for bitmask-flag enumerations. Each KeeFlags subclass
  declares 'KeeFlag()' fields in its body, one per single-bit flag;
  the metaclass then materializes every combination of those flags as
  a concrete member at class-creation time.

  Cost (read before declaring a large enum)
  -----------------------------------------
  A KeeFlags class with N single-bit flags materializes 2 ** N
  members eagerly during class definition:

      N =  4   -> 16 members
      N =  8   -> 256 members
      N = 12   -> 4096 members
      N = 16   -> 65,536 members
      N = 20   -> 1,048,576 members

  The cost is paid once, at import. For typical use (file
  permissions, keyboard modifiers, etc.) where N <= 8, this is
  negligible. For N up to 12, expect a small but real import-time
  delay and memory footprint. For N >= 16, expect a noticeable
  delay and several MB of memory just for the class. For N > 20 you
  almost certainly want a plain 'int' bitmask with helper functions,
  not a KeeFlags enum.

  Member attributes
  -----------------
  - 'flags': all single-bit flags declared on the class (mirrors the
    class-level 'flags'; not member-specific).
  - 'highs': the flags that are HIGH for the member.
  - 'lows': the flags that are LOW for the member.
  - 'names': a frozenset of the names of the HIGH flags.
  - 'index' / 'value': the member's bitmask integer (value defaults
    to the index).
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
  collapses, and an unknown name raises 'KeyError'.

  Entries must be integer valued.

  Like 'KeeNum' members, the members are write-once constants: once
  'KeeFlagsMeta.__new__' has stamped a member, any attempt to set or
  delete an attribute on it raises 'KeeWriteOnceError', as does
  rebinding or deleting the member name on the owning class. A member
  needing extra attributes should come from a subclass declaring them.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables (type hints)
  __member_list__: list[Self]
  __member_dict__: dict[frozenset[str], Self]

  #  Private Variables
  #  '__field_owner__' and '__field_name__' are set on each instance
  #  by 'KeeFlagsMeta.__new__' at class creation time. Declared here
  #  with None defaults so fresh instances do not raise AttributeError
  #  before the metaclass setattr runs.
  __field_owner__ = None
  __field_name__ = None
  __member_index__ = None
  __member_value__ = None
  __frozen_state__ = None

  #  Public Variables
  index: Field[int] = Field()

  #  Virtual Variables
  flags: Field[list[KeeFlag]] = Field()
  lows: Field[Iterator[KeeFlag]] = Field()
  highs: Field[Iterator[KeeFlag]] = Field()
  value: Field[Any] = Field()
  name: Field[str] = Field()
  names: Field[frozenset[str]] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @flags.GET
  def _getFlagsFromType(self, ) -> Any:
    """
    The 'KeeFlagsMeta' metaclass provides the helpful 'flags' descriptor
    allowing inspection of all the flags available. The descriptor is then
    available on the derived 'KeeFlags' classes, but *not* on the
    instances themselves. For example:

    class KeyboardModifier(KeeFlags):
      ALT = KeeFlag()
      SHIFT = KeeFlag()
      CTRL = KeeFlag()
      META = KeeFlag()

    Then: 'KeyboardModifier.flags' is understood as:
    KeeFlagsMeta.flags.__get__(KeyboardModifier, KeeFlagsMeta)

    But instances of 'KeyboardModifier' are not able to access the
    metaclass defined descriptor. Therefore, the 'KeeFlags' class must
    explicitly mirror it. A potential future feature of 'worktoy' will
    provide deep metaclass descriptors.
    """
    cls = type(self)
    mcls = type(cls)
    desc = getattr(mcls, 'flags')
    return desc.__get__(cls, mcls)

  @value.GET
  def _getValue(self) -> Any:
    """
    Returns the object at the 'value' attribute of the member. The base
    implementation provides for retrieving a member from the class from a
    given value. Other than this, the attribute provides no further
    functionality. Subclasses may override this method to provide any
    object from any member. While not enforced, it is recommended that
    that member values should be of the same type and that the type should
    be immutable. Subclasses are free to grant multiple members the same
    value. In this case, the 'fromValue' method returns the first member
    having the given value.

    By default, the value is the index of the member.
    """
    return self.index

  @lows.GET
  def _getLows(self) -> Iterator[KeeFlag]:
    if self.__member_index__:
      for flag in type(self).flags:
        if self.index & (1 << flag.index):
          continue
        yield flag
    else:
      yield from type(self).flags

  @highs.GET
  def _getHighs(self) -> Iterator[KeeFlag]:
    if self.__member_index__:
      for flag in type(self).flags:
        if self.index & (1 << flag.index):
          yield flag
    else:
      yield from ()

  @index.GET
  def _getIndex(self) -> int:
    if self.__member_index__ is None:
      raise MissingVariable(self, '__member_index__', int)
    if isinstance(self.__member_index__, int):
      return self.__member_index__
    raise TypeException('__member_index__', self.__member_index__, int)

  @name.GET
  def _getName(self) -> str:
    return '_'.join(f.name for f in self.highs) or 'NULL'

  @names.GET
  def _getNames(self, ) -> frozenset:
    return frozenset(f.name for f in self.highs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __setattr__(self, name: str, value: Any) -> None:
    """
    A member is frozen once 'KeeFlagsMeta.__new__' has stamped it, so
    '__setattr__' raises 'KeeWriteOnceError' once the freeze flag is
    set; assignments during construction pass through.
    """
    if object.__getattribute__(self, '__frozen_state__'):
      raise KeeWriteOnceError(self, name)
    object.__setattr__(self, name, value)

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

  def __bool__(self) -> bool:
    """The NULL member (no flags HIGH) is falsy. Any member with at
    least one flag HIGH is truthy, mirroring the truthiness of the
    underlying bitmask."""
    return True if self.__member_index__ else False

  def __iter__(self) -> Iterator[Self]:
    yield from self.highs

  def __str__(self, ) -> str:
    infoSpec = """%s.%s [%d]"""
    clsName = type(self).__name__
    info = infoSpec % (clsName, self.name, self.index)
    return textFmt(info)

  __repr__ = __str__

  def __eq__(self, other: Any) -> bool:
    if not isinstance(type(other), KeeFlagsMeta):
      return NotImplemented
    if self.__field_owner__ is not other.__field_owner__:
      return False
    return True if self.index == other.index else False

  def __hash__(self, ) -> int:
    return hash((hash(type(self)), *self.highs))

  def __or__(self, other: Self) -> Self:
    cls = type(self)
    if not isinstance(other, cls):
      return NotImplemented
    highs = (*self.highs, *other.highs,)
    names = frozenset((f.name for f in highs), )
    return cls.memberDict[names]

  def __and__(self, other: Self) -> Self:
    cls = type(self)
    if not isinstance(other, cls):
      return NotImplemented
    highs = (f for f in self.highs if f in other.highs)
    names = frozenset((f.name for f in highs), )
    return cls.memberDict[names]

  def __xor__(self, other: Self) -> Self:
    cls = type(self)
    if not isinstance(other, cls):
      return NotImplemented
    ors = self | other
    ands = self & other
    highs = (f for f in ors.highs if f not in ands.highs)
    names = frozenset((*(f.name for f in highs),), )
    return cls.memberDict[names]

  def __invert__(self, ) -> Self:
    cls = type(self)
    lows = self.lows
    names = frozenset((f.name for f in lows), )
    return cls.memberDict[names]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, index: int) -> None:
    self.__member_index__ = index
