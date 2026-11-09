"""KeeFlagsMeta provides the metaclass for KeeFlags."""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from ..mcls import BaseMeta
from ..utilities import textFmt, joinWords
from ..waitaminute.keenum import KeeResolveError, KeeWriteOnceError
from ..waitaminute.keenum import KeeMemberNameError
from . import KeeFlag
from . import KeeFlagsSpace as KFSpace

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Self, Any, Iterator, Union

  from . import KeeFlags, KeeFlagsMeta

  Bases: TypeAlias = tuple[type, ...]
  KFMeta: TypeAlias = Union[KeeFlagsMeta, BaseMeta]

#  The tables of a class before '__new__' gives it its own.
_EMPTY: MappingProxyType = MappingProxyType({})


class KeeFlagsMeta(BaseMeta):
  """
  KeeFlagsMeta is the metaclass driving every 'KeeFlags' bitmask-flag
  enumeration. During '__new__' it reads the 'KeeFlag' declarations
  collected by 'KeeFlagsHook', clones them onto the class with their bit
  indices, then materializes one member per combination of those flags,
  2 ** N members for N flags, in index order through 'type.__call__',
  caching them in 'memberList' and a names-keyed 'memberDict'. The index
  of a member is its bit mask, so 'memberList[index]' is the member of a
  mask, and the operators of the members are bit operations on indices.
  The value of a member comes from the '_getValue' the ordinary method
  resolution order finds, so the nearest override wins, and it is read
  once as the member is built. 'cls(...)' / 'cls[...]' route through
  '_resolveMember'. A miss, by name, index or value, raises
  'KeeResolveError', as a miss on a 'KeeNum' does, and 'in' answers by
  identity: an object is in the class when it is one of its members, or
  a member of a related flags class whose flags the class holds, which
  resolves to that member. A lookup by name, in any case and order, is
  one lookup in 'memberDict'; a lookup by value is one lookup when every
  value hashes. Calling, length, iteration, membership, subscripting and
  attribute assignment and deletion are the metaclass's own, so a flags
  class body binding the class hook for one of them, such as
  '__class_len__', is refused with 'ShadowedClassHook'; the hooks for the
  other operations, such as '__class_str__', '__class_hash__' or
  '__class_subclasscheck__', work as on any class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __kee_class__ = None

  #  Private Variables
  __kee_flags__ = None
  __allow_instantiation__ = None
  __flag_clones__: tuple = ()
  __member_list__: list = []
  __member_dict__ = _EMPTY
  __valued_members__ = _EMPTY
  __value_scan__: bool = False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getFlags(cls) -> list[KeeFlag]:
    """
    The 'flags' getter returns the flags of the class in a new list. The
    flags are cloned onto the class on the first read and kept, so every
    later read, and every member reporting its flags, sees the same flag
    objects. They are kept in the namespace of the class itself, since a
    subclass clones flags of its own.
    """
    if '__flag_clones__' not in cls.__dict__:
      clones = (*cls.getKeeFlags().values(),)
      type.__setattr__(cls, '__flag_clones__', clones)
    return [*cls.__dict__['__flag_clones__']]

  def _getValueType(cls) -> type:
    nullMember = cls.NULL
    return type(nullMember.value)

  def _getMemberList(cls) -> list[KeeFlags]:
    return cls.__member_list__

  def _getMemberDict(cls) -> dict[frozenset[str], KeeFlags]:
    return cls.__member_dict__

  flags = property(_getFlags)
  memberList = property(_getMemberList)
  memberDict = property(_getMemberDict)
  valueType = property(_getValueType)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kw) -> KFSpace:
    """
    The '__prepare__' method returns a 'KeeFlagsSpace' as the class-body
    namespace, in place of the plain 'BaseSpace'.
    """
    return KFSpace(mcls, name, bases, **kw)

  def __new__(mcls, name: str, bases: Bases, space: KFSpace, **kw) -> Self:
    """
    The '__new__' method builds the flag enumeration: it constructs the
    class, then for every subclass past the 'KeeFlags' base clones the
    flags and materializes all 2 ** N flag combinations as members,
    populating 'memberList', 'memberDict' and the table of values.
    """
    #  The root is marked by the '_root' keyword, never by its name.
    isRoot = True if kw.get('_root', False) else False
    cls: KFMeta = BaseMeta.__new__(mcls, name, bases, space, **kw)
    if isRoot:
      setattr(mcls, '__kee_class__', cls)
      return cls
    type.__setattr__(cls, '__allow_instantiation__', True)
    mcls._createMembers(cls, name)
    mcls._createValued(cls)
    type.__setattr__(cls, '__allow_instantiation__', False)
    return cls

  def __setattr__(cls, name: str, value: Any) -> None:
    """
    Rebinding a name that currently holds an enumeration member raises
    'KeeWriteOnceError': the members of an enumeration are write-once
    constants, and 'memberList' and 'memberDict' would keep serving the
    original member anyway.
    """
    try:
      existing = cls.__dict__[name]
    except KeyError:
      pass
    else:
      keeClass = type(cls).__kee_class__
      if keeClass is not None and isinstance(existing, keeClass):
        raise KeeWriteOnceError(existing, name)
    BaseMeta.__setattr__(cls, name, value)

  def __delattr__(cls, name: str) -> None:
    """
    Deleting a name that currently holds an enumeration member raises
    'KeeWriteOnceError' unconditionally: no stage of class construction
    deletes a member, so no window exists.
    """
    try:
      existing = cls.__dict__[name]
    except KeyError:
      pass
    else:
      keeClass = type(cls).__kee_class__
      if keeClass is not None and isinstance(existing, keeClass):
        raise KeeWriteOnceError(existing, name)
    BaseMeta.__delattr__(cls, name)

  def __call__(cls, *args, **kwargs) -> Any:
    """
    Calling the class resolves the member combining the flags of the
    positional identifiers, or the empty member for none. A keyword has
    no meaning here and raises Python's 'TypeError', as a function given
    an unexpected keyword does. The members are built past this method,
    by '_createMembers'.
    """
    if kwargs:
      keys = joinWords(*["""'%s'""" % key for key in kwargs])
      infoSpec = """%s() takes no keyword arguments, but received %s."""
      raise TypeError(textFmt(infoSpec % (cls.__name__, keys)))
    return cls._resolveMember(*args)

  def __len__(cls) -> int:
    return len(cls.__member_list__)

  def __iter__(cls, ) -> Iterator[KeeFlags]:
    return iter(cls.__member_list__)

  def __contains__(cls, identifier: Any) -> bool:
    """
    The '__contains__' method reports membership by identity: 'x in cls'
    is True when 'x' is one of the members of the class, or a member of a
    related flags class with flags the class holds, which is equal to
    one of its members; it is False for a name, an index or a value,
    however it would resolve. The '__eq__' of 'x' is never asked.
    """
    if isinstance(type(identifier), KeeFlagsMeta):
      return True if cls._fromMember(identifier) is not None else False
    return False

  def __getitem__(cls, identifier: Any) -> KeeFlags:
    return cls._resolveMember(identifier)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createMembers(cls, name: str) -> None:
    """
    One member per bit mask, in index order, each bound at its name. The
    flags are cloned onto the class first, since every member reads them.
    A name the class body binds itself is refused before any member is
    bound, since the member would replace it without a word. The names
    of the body are those the namespace kept; the namespace argument of
    '__new__' is a plain dictionary with the flag names still in it when
    the class is built by calling the metaclass with one.

    Raises
    ------

    KeeMemberNameError
      The class body binds the name of a member.
    """
    flags = cls._getFlags()
    namespace = type.__getattribute__(cls, '__namespace__')
    members, byNames = [], dict()
    for index in range(2 ** len(flags)):
      member = type.__call__(cls, index)
      if dict.__contains__(namespace, member.name):
        raise KeeMemberNameError(name, member.name)
      members.append(member)
      byNames[member.names] = member
    for member in members:
      type.__setattr__(cls, member.name, member)
    type.__setattr__(cls, '__member_list__', members)
    type.__setattr__(cls, '__member_dict__', byNames)

  def _createValued(cls) -> None:
    """
    Each hashable value maps to the lowest-indexed member holding it. A
    single unhashable value raises the flag '__value_scan__', and value
    lookups then go through the members in turn.
    """
    valued = dict()
    for member in cls.__member_list__:
      try:
        hash(member.value)
      except TypeError:
        type.__setattr__(cls, '__value_scan__', True)
        return
      if member.value in valued:
        continue
      valued[member.value] = member
    type.__setattr__(cls, '__valued_members__', valued)
    type.__setattr__(cls, '__value_scan__', False)

  def _fromMember(cls, member: KeeFlags) -> Any:
    """
    A member of another class in the same lineage, a flags class based
    on this one or that this one is based on, names flags this class may
    hold too, and the member of this class with exactly those flags
    stands for it here. The members of each class are its own, so the
    foreign member is never handed back.

    Parameters
    ----------

    member : KeeFlags
      A member of any flags class.

    Returns
    -------

    KeeFlags or None
      The member of this class with the flags of 'member', the member
      itself when it is this class's own, or 'None' when the classes are
      unrelated or this class lacks one of the flags.
    """
    other = type(member)
    if other is cls:
      return member
    if not (issubclass(other, cls) or issubclass(cls, other)):
      #  This branch is reached by the following:
      #  - The member belongs to a flags class of another lineage
      return None
    byNames = cls.__member_dict__
    if member.names in byNames:
      return byNames[member.names]
    #  The rest of the method is reached by the following:
    #  - The member has a flag high that this class lacks, as a member of
    #    a subclass combining the flag it added
    return None

  def _resolveIndex(cls, index: int) -> KeeFlags:
    """
    The '_resolveIndex' method resolves a member from its index, which is
    its position in 'memberList', since the metaclass builds the members
    in index order. An index outside the range, a negative one included,
    raises 'KeeResolveError'.
    """
    members = cls.__member_list__
    if 0 <= index < len(members):
      return members[index]
    raise KeeResolveError(cls, index)

  def _resolveName(cls, name: str) -> KeeFlags:
    """
    The '_resolveName' method resolves a member from a name that matches
    the canonical name of a member ignoring case, as 'null' matches
    'NULL', or that lists the flags of a member separated by '_', in any
    order and any case. The flags of a member are the parts of its
    canonical name, so one lookup by the set of the parts answers both.
    A name matching no member raises 'KeeResolveError'.
    """
    upperName = name.upper()
    if upperName == 'NULL':
      return cls.__member_list__[0]
    names = frozenset(upperName.split('_'))
    byNames = cls.__member_dict__
    if names in byNames:
      return byNames[names]
    raise KeeResolveError(cls, name)

  def _resolveNames(cls, *identifiers: Any) -> KeeFlags:
    """
    The '_resolveNames' method resolves several identifiers to the member
    having every flag high that any of them has. Each is resolved as a
    single lookup would resolve it, so a member, a name in any case and
    order, a combined name, or an index all work, and the miss of any one
    raises 'KeeResolveError' for it.
    """
    mask = 0
    for identifier in identifiers:
      mask |= cls._resolveMember(identifier).index
    return cls.__member_list__[mask]

  def _resolveValue(cls, value: Any) -> KeeFlags:
    """
    The '_resolveValue' method returns the first member whose value
    equals 'value', raising 'KeeResolveError' when none does. The value is
    compared only with member values of a type it is an instance of,
    since comparing it with any other would hand the decision to its own
    '__eq__', which may raise on a member value or answer 'True' to
    anything. A 'bool' is compared with 'bool' values alone, though it
    is an 'int', as a 'KeeNum' of 'int' values refuses one.
    """
    if not cls.__value_scan__:
      try:
        hash(value)
      except TypeError:
        pass
      else:
        valued = cls.__valued_members__
        if value not in valued:
          raise KeeResolveError(cls, value)
        member = valued[value]
        if cls._valueMatches(value, member.value):
          return member
    for member in cls.__member_list__:
      if cls._valueMatches(value, member.value):
        return member
    raise KeeResolveError(cls, value)

  def _valueMatches(cls, value: Any, memberValue: Any) -> bool:
    if not isinstance(value, type(memberValue)):
      return False
    if isinstance(value, bool) and not isinstance(memberValue, bool):
      return False
    return True if memberValue == value else False

  def _resolveMember(cls, *identifier: Any, **kwargs) -> KeeFlags:
    if not identifier:
      return cls.__member_list__[0]
    if len(identifier) > 1:
      return cls._resolveNames(*identifier)
    identifier = identifier[0]
    if isinstance(type(identifier), KeeFlagsMeta):
      member = cls._fromMember(identifier)
      if member is None:
        raise KeeResolveError(cls, identifier)
      return member
    if isinstance(identifier, (tuple, list, frozenset, set)):
      return cls._resolveNames(*identifier)
    #  A 'bool' is an 'int', but no index.
    if isinstance(identifier, int) and not isinstance(identifier, bool):
      return cls._resolveIndex(identifier)
    if isinstance(identifier, str):
      return cls._resolveName(identifier)
    return cls._resolveValue(identifier)
