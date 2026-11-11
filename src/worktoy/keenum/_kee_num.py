"""
KeeBase provides the base for 'worktoy.keenum' enumerations.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, overload

from ..core import MetaType
from ..utilities import textFmt
from ..waitaminute import DeprecatedPromise
from ..waitaminute.keenum import KeeResolveError, KeeWriteOnceError
from . import Kee

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Never, Self, Optional

#  The description of the deprecation of the position of a member.
_POSITION = """The position belongs to the enumeration, not to the member:
'Day[x]' gives the member at position 'x', and iterating 'Day' gives its
members in order."""


class KeeBase(metaclass=MetaType):
  """
  An enumeration member is one object, built once as its class is
  created, that a project passes around, compares and keys by: the days
  of a week, the status codes of a protocol. It must know its name, its
  position and its value, be equal to itself alone, hash wherever its
  value hashes, read back as the very object after copying and
  pickling, and refuse every change once built. Reading any of that, or
  hashing the member, happens in loops and at every dictionary lookup,
  so none of it may be worked out again after the member is built.

  Implementation
  --------------

  'KeeBase' is the base of every enumeration; 'KeeNum', the root an
  enumeration subclasses, is built from it by 'KeeMeta'. The constructor
  reads the name, the index, the value and the value type off the 'Kee'
  of the declaration and stores them as plain attributes of the member,
  together with the 'Kee' itself and the hash. A member is a plain
  object, not a worktoy 'Object': no box tags it, and reading it off its
  class runs no descriptor. Setting or deleting an attribute raises
  'KeeWriteOnceError'; the constructor writes past that with
  'object.__setattr__'.

  Equality is identity: 'MyEnum.A == MyEnum.A' is True; comparison to
  a member of a different KeeNum subclass returns NotImplemented (and
  '==' therefore yields False).

  Hashability tracks the member's value. The hash is computed once, from
  the name of the class and the name of the member joined by '::' and
  read as a big-endian integer, so distinct members of a class hash
  apart. A member whose value is unhashable (a list, a dict, a mutable
  instance) is unhashable as well: hashing it raises 'TypeError', so a
  hashed lookup on the member side stays consistent with one on the
  value side. Members with unhashable values still work everywhere
  hashability is not required: iteration, attribute access, name and
  index resolution, equality, '__str__', and '__repr__'.

  A copy of a member is the member itself, and a member pickles as a
  lookup of its name on its class.

  A member is shared by every enumeration based on the one that
  declared it, and 'owners' gives those classes, in the order they were
  created, held by strong references. The text of a member is no
  promise: it currently names its one owner, '<Color>.RED', or the root
  of its family once several classes hold it, '<KeeNum>.RED'.

  Attributes
  ----------

  name : str
    The name the class body bound the member to.

  index : int
    Deprecated: the position of the member among those of the class that
    declared it. Reading it, 'int(member)' and using the member as an
    index give a 'DeprecatedPromise', since the position belongs to the
    enumeration: 'Day[x]' gives the member at a position.

  value : Any
    The value the 'Kee' built.

  valueType : type
    The type the 'Kee' declared.

  kee : Kee
    The declaration of the member.

  owners : tuple[type, ...]
    The enumerations holding the member, in the order they were created.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __member_hash__: Optional[int] = None
  __member_index__: Optional[int] = None
  __member_owners__: Optional[list] = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # @formatter:off
  @overload
  def __init__(self, identifier: Any) -> None: ...
  @overload
  def __init__(self, member: Kee) -> None: ...
  # @formatter:on

  def __init__(self, member: Kee) -> None:
    value = member.getValue()
    object.__setattr__(self, 'kee', member)
    object.__setattr__(self, 'name', member.name)
    object.__setattr__(self, '__member_index__', member._getIndex())
    object.__setattr__(self, 'value', value)
    object.__setattr__(self, 'valueType', member.getFieldType())
    object.__setattr__(self, '__member_hash__', self._computeHash(value))
    object.__setattr__(self, '__member_owners__', [])

  def _computeHash(self, value: Any) -> Optional[int]:
    try:
      hash(value)
    except TypeError:
      return None
    base = str.join('::', (type(self).__name__, self.name,))
    return hash(int.from_bytes(base.encode(), 'big'))

  def _readIndex(self) -> int:
    """
    The 'index' of a member is deprecated: the position belongs to the
    enumeration, which answers 'Day[x]', not to the member. A read still
    gives the position in the class that declared the member, with a
    'DeprecatedPromise' at the line that read it.
    """
    info = textFmt(_POSITION)
    DeprecatedPromise('worktoy.keenum.KeeBase.index', info).warn()
    return self.__member_index__

  index = property(_readIndex)

  def _getOwners(self) -> tuple[type, ...]:
    return (*self.__member_owners__,)

  owners = property(_getOwners)

  def _addOwner(self, cls: type) -> None:
    """
    'KeeMeta._createMembers' records each enumeration holding the member
    as it binds it. The list is changed in place, which the frozen member
    allows, since nothing is assigned.
    """
    self.__member_owners__.append(cls)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __cast_as__(cls, value: Any) -> Any:
    """
    The '__cast_as__' hook lets 'typeCast' resolve a value to the member
    holding it, as calling the enumeration does: a member passes, a name
    resolves, '__class_resolve__' is consulted, and a value of the value
    type resolves to the first member holding it. An identifier no step
    resolves is refused with 'NotImplemented', so 'typeCast' raises its
    own refusal and an 'AttriBox' over the enumeration, or an overload
    naming it, moves on. While the class statement still instantiates
    members, nothing is resolved.
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
    """A member is a singleton, so a copy is the member itself. Returning
    a fresh instance would compare unequal to every canonical member,
    since equality is identity."""
    return self

  def __deepcopy__(self, memo: Any) -> Self:
    """A member is a singleton, so a deep copy is the member itself. This
    keeps a member stored as an 'AttriBox' default, or carried inside a
    structure that gets deep-copied, equal to the canonical member rather
    than a clone that matches nothing."""
    return self

  def __reduce__(self) -> tuple:
    """
    A member pickles as a lookup of its name on its class, so it
    unpickles as the member itself.
    """
    return getattr, (type(self), self.name)

  def __int__(self) -> int:
    """
    'int(member)' gives the deprecated position, with a
    'DeprecatedPromise'; see '_readIndex'.
    """
    info = textFmt(_POSITION)
    DeprecatedPromise('worktoy.keenum.KeeBase.__int__', info).warn()
    return self.__member_index__

  def __index__(self) -> int:
    """
    A member used as an index, as in 'items[member]', gives the
    deprecated position, with a 'DeprecatedPromise'; see '_readIndex'.
    """
    info = textFmt(_POSITION)
    DeprecatedPromise('worktoy.keenum.KeeBase.__index__', info).warn()
    return self.__member_index__

  def __hash__(self) -> int:
    """
    The hash computed as the member was built, or a 'TypeError' raised
    from the refusal of the value, when the value is unhashable.
    """
    memberHash = self.__member_hash__
    if memberHash is None:
      try:
        hash(self.value)
      except TypeError as typeError:
        infoSpec = """Enumeration member '%s' is unhashable because its
        value of type '%s' is unhashable!"""
        info = infoSpec % (self, type(self.value).__name__)
        raise TypeError(textFmt(info)) from typeError
    return memberHash

  def __eq__(self, other: Any) -> bool:
    if type(self) is not type(other):
      return NotImplemented
    return True if self is other else False

  def __str__(self) -> str:
    """
    The text names the one enumeration holding the member, or the root
    of its family once several do. It is no promise.
    """
    owners = self.__member_owners__
    if len(owners) == 1:
      return '<%s>.%s' % (owners[0].__name__, self.name)
    root = type(type(self)).keeNum
    return '<%s>.%s' % (root.__name__, self.name)

  __repr__ = __str__

  if TYPE_CHECKING:  # pragma: no cover, no mutate
    # @formatter:off
    def __call__(self, identifier: Any) -> Self: ...
    # @formatter:on
