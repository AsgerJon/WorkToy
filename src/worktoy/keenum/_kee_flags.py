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
from ..waitaminute.keenum import KeeWriteOnceError, KeeResolveError
from . import KeeFlag, KeeFlagsMeta

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Iterator, Never, Self


class KeeFlags(metaclass=KeeFlagsMeta, _root=True):
  """
  Base class for bitmask-flag enumerations. Each KeeFlags subclass
  declares 'KeeFlag()' fields in its body, one per single-bit flag;
  the metaclass then materializes every combination of those flags as
  a concrete member at class-creation time.

  Cost (read before declaring a large enum)
  -----------------------------------------
  A KeeFlags class with N single-bit flags materializes 2 ** N
  members eagerly during class definition, each a Python object built
  by a call. Measured on one desktop machine under Python 3.14, the
  class statement took:

      N =  4   -> 16 members          less than a millisecond
      N =  8   -> 256 members         0.1 seconds
      N = 12   -> 4096 members        2 seconds
      N = 14   -> 16,384 members      9 seconds
      N = 16   -> 65,536 members      50 seconds

  The cost is paid once, at import, and grows four times for every two
  flags added. For typical use (file permissions, keyboard modifiers,
  etc.) where N <= 8, this is negligible. Past 12 the class statement
  takes seconds and the members several MB of memory. For N >= 16 you
  almost certainly want a plain 'int' bitmask with helper functions,
  not a KeeFlags enum. A lookup by index or through the operators is
  one step whatever N is; a lookup by name compares the name with each
  member's in turn.

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
    available on the subclasses of 'KeeFlags', but *not* on the
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
    desc = type.__getattribute__(mcls, 'flags')
    return desc.__get__(cls, mcls)

  @value.GET
  def _getValue(self) -> Any:
    """
    The value of a member is what a project reads off it, and what the
    class resolves a member from. The base gives every member its index
    as its value; a subclass reimplements this getter to give any object
    from any member, as 'FileAccess' in the tests gives bytes. Values of
    one immutable type are recommended, not required, and several
    members may share one value, in which case the lowest-indexed member
    answers for it.
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

  def __reduce__(self) -> tuple:
    """
    A member pickles as a lookup of its canonical name on its class, so
    it unpickles as the member itself. The default protocol rebuilt a
    fresh instance from the member's state, a phantom that was not the
    member, so an 'is' check against it failed.
    """
    return getattr, (type(self), self.name)

  def __bool__(self) -> bool:
    """The NULL member (no flags HIGH) is falsy. Any member with at
    least one flag HIGH is truthy, mirroring the truthiness of the
    underlying bitmask."""
    return True if self.__member_index__ else False

  def __iter__(self) -> Iterator[KeeFlag]:
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
    cls, otherCls = type(self), type(other)
    if otherCls is cls:
      return True if self.index == other.index else False
    if issubclass(otherCls, cls) or issubclass(cls, otherCls):
      return True if self.names == other.names else False
    return NotImplemented

  def __hash__(self, ) -> int:
    return hash(self.names)

  def _asOwn(self, other: Any) -> Any:
    """
    An operator takes a member of this class or of a related one, and
    works on the member of this class with the other's flags; anything
    else, a member of an unrelated class or a member with a flag this
    class lacks, gives 'None', so the operator answers 'NotImplemented'
    and Python asks the other operand.
    """
    if not isinstance(type(other), KeeFlagsMeta):
      return None
    return type(self)._fromMember(other)

  def __or__(self, other: Any) -> Any:
    other = self._asOwn(other)
    if other is None:
      return NotImplemented
    cls = type(self)
    highs = (*self.highs, *other.highs,)
    names = frozenset((f.name for f in highs), )
    return cls.memberDict[names]

  def __and__(self, other: Any) -> Any:
    other = self._asOwn(other)
    if other is None:
      return NotImplemented
    cls = type(self)
    highs = (f for f in self.highs if f in other.highs)
    names = frozenset((f.name for f in highs), )
    return cls.memberDict[names]

  def __xor__(self, other: Any) -> Any:
    other = self._asOwn(other)
    if other is None:
      return NotImplemented
    cls = type(self)
    ors = self | other
    ands = self & other
    highs = (f for f in ors.highs if f not in ands.highs)
    names = frozenset((*(f.name for f in highs),), )
    return cls.memberDict[names]

  #  The three operators commute, so the reflected forms are the same.
  __ror__ = __or__
  __rand__ = __and__
  __rxor__ = __xor__

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
