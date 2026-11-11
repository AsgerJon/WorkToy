"""KeeFlagsMeta provides the metaclass for KeeFlags."""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from ..desc import AttriBox
from ..mcls import BaseMeta
from ..utilities import textFmt, joinWords
from ..waitaminute.keenum import KeeResolveError, KeeWriteOnceError
from ..waitaminute.keenum import KeeMemberNameError, KeeTypeException
from . import Kee
from . import KeeFlagsSpace as KFSpace

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Self, Any, Iterator, Union

  from . import KeeFlags, KeeFlagsMeta

  Bases: TypeAlias = tuple[type, ...]
  KFMeta: TypeAlias = Union[KeeFlagsMeta, BaseMeta]

#  The tables of a class before '__new__' gives it its own.
_EMPTY: MappingProxyType = MappingProxyType({})

#  One member for each set of flags, in the whole process: the set of the
#  flag members a member combines, to that member. Every class holding
#  those flags holds that member. The strong references are deliberate.
_COMBINATIONS: dict = {}


class KeeFlagsMeta(BaseMeta):
  """
  KeeFlagsMeta is the metaclass driving every 'KeeFlags' bitmask-flag
  enumeration. Every member of a flags class is a combination of its
  flags: a flag is the combination of itself, and 'NULL', the member of
  the root 'KeeFlags', combines none.

  During '__new__' it gives the class its flags: those of its bases
  first, in the order of the bases, a flag reached through two bases
  once, then one flag member for each declaration of the body, built by
  'type.__call__', the declaration placed on the class first. Then it
  gives the class one member per combination of those flags, 2 ** N for
  N flags, in the order of their bit masks over the flags of the class.
  One member stands for each set of flags in the whole process: a
  combination some class built already, 'NULL' and the members of every
  base among them, is that very member, and only a combination no class
  built yet is built by this one, through 'type.__call__'. Each member is
  bound at the name that joins its flags in the order of this class,
  and records the class among its owners. 'memberList' holds the members
  by mask, 'memberDict' by the names of their flags, and 'flags' the
  flags of the class.

  The value of a member comes from the '_getValue' of the class that
  built it, read once, after the class has its flags. A flag declared
  with a 'Kee' is valued as the 'Kee' is; every other member by its
  name. 'valueType' is the type of the value of the first flag, and no
  combination may contain a member whose value is not an instance of
  it, which a class breaking it is refused for with 'KeeTypeException'.
  Every flag is the combination of itself, so the rule holds every
  flag, inherited ones included, to the type; the value of a
  combination itself is free, and 'NULL', containing no member, cannot
  break it.

  'cls(...)' and 'cls[...]' route through '_resolveMember': nothing
  gives 'NULL'; a member the class holds, or one of a subclass, is
  itself; several identifiers, or a tuple, list or set of them, give the
  member having every flag any of them has; an 'int' other than a
  'bool' is a bit mask of the class; a 'str' is a name in any case and
  flag order; anything else is a value, compared only with values of a
  type it is an instance of. A miss raises 'KeeResolveError', as a miss
  on a 'KeeNum' does. 'in' and 'isinstance' answer by identity: an
  object belongs to the class when it is one of its members, or a member
  of a subclass of it. Calling, length, iteration, membership, the
  instance check, subscripting and attribute assignment and deletion
  are the metaclass's own, so a flags class body binding the class hook
  for one of them, such as '__class_len__', is refused with
  'ShadowedClassHook'; the hooks for the other operations, such as
  '__class_str__', '__class_hash__' or '__class_subclasscheck__', work
  as on any class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __kee_class__ = None

  #  Private Variables
  __allow_instantiation__ = None
  __flag_order__: tuple = ()
  __member_list__: list = []
  __member_dict__ = _EMPTY
  __member_ids__ = _EMPTY
  __valued_members__ = _EMPTY
  __value_scan__: bool = False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getFlags(cls) -> list[KeeFlags]:
    """
    The 'flags' getter gives the flags of the class, the flag members
    themselves, in a new list: those of the bases first, then those the
    body declared.
    """
    return [*cls.__flag_order__]

  def _getValueType(cls) -> type:
    """
    The 'valueType' getter gives the type of the value of the first flag
    of the class. A class without flags has no value type and raises
    'TypeError', as an enumeration without members does.
    """
    flags = cls.__flag_order__
    if not flags:
      infoSpec = """Flags class '%s' has no flags, so it has no
      'valueType'."""
      raise TypeError(textFmt(infoSpec % cls.__name__))
    return type(flags[0].value)

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
    The '__new__' method builds the class, records it as the root when
    declared with the class keyword '_root', then gives it its flags,
    its members and its table of values.
    """
    #  The root is marked by the '_root' keyword, never by its name.
    isRoot = True if kw.get('_root', False) else False
    cls: KFMeta = BaseMeta.__new__(mcls, name, bases, space, **kw)
    if isRoot:
      setattr(mcls, '__kee_class__', cls)
    type.__setattr__(cls, '__allow_instantiation__', True)
    cls._createFlags()
    cls._createMembers()
    cls._createValued()
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
    by '_createFlags' and '_createMembers'.
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
    The '__contains__' method reports membership by identity, as the
    instance check does: 'x in cls' is True when 'x' is one of the
    members of the class, or a member of a subclass of it. It is False
    for a name, a mask or a value, however it would resolve, and the
    '__eq__' of 'x' is never asked.
    """
    return cls._holds(identifier)

  def __instancecheck__(cls, instance: Any) -> bool:
    """
    The '__instancecheck__' method treats 'instance' as a member when it
    is one of the members of the class, or a member of a subclass of it;
    a member the class shares with a base is an instance of both.
    """
    return cls._holds(instance)

  def __getitem__(cls, identifier: Any) -> KeeFlags:
    return cls._resolveMember(identifier)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _findCombination(flags: frozenset) -> Any:
    """
    The '_findCombination' method gives the member combining exactly the
    flags of the set, or 'NotImplemented' when no class built one, so an
    operator on members of classes that no class combines refuses.
    """
    try:
      return _COMBINATIONS[flags]
    except KeyError:
      return NotImplemented

  def _createFlags(cls) -> None:
    """
    The flags of the bases come first, as the namespace gathered them.
    Each declaration of the body is then placed on the class, as a box
    is placed on its class, which refuses a 'Kee' declared without
    parentheses or placed on another class already, and becomes a flag
    member of its own, the next bit. The flags are recorded before any
    value is read, since a '_getValue' may read the low flags. Every
    flag, inherited or new, is then held to the value type of the first
    flag, and only then are the new flags entered among the members of
    the process, so a refused class leaves none behind.

    Raises
    ------

    KeeTypeException
      A flag is valued by something other than an instance of the type
      of the value of the first flag.
    """
    space = type.__getattribute__(cls, '__namespace__')
    order = [*space.getBaseFlags().values()]
    built = []
    for name, declaration in space.getDeclaredFlags().items():
      if isinstance(declaration, Kee):
        AttriBox.__set_name__(declaration, cls, name)
      else:
        #  This branch is reached by the following:
        #  - A flag declared with the deprecated 'KeeFlag'
        declaration.__field_owner__ = cls
        declaration.__member_index__ = len(order)
      flag = type.__call__(cls, (), 1 << len(order), declaration)
      order.append(flag)
      built.append(flag)
    type.__setattr__(cls, '__flag_order__', (*order,))
    for flag in built:
      flag._settleValue()
    for flag in order[1:]:
      if not isinstance(flag.value, type(order[0].value)):
        raise KeeTypeException(flag.name, flag.value, cls.valueType)
    for flag in built:
      _COMBINATIONS[frozenset((flag,))] = flag

  def _createMembers(cls) -> None:
    """
    One member per bit mask over the flags of the class, in mask order,
    each bound at the name joining its flags in the order of the class. A
    name the class body binds itself is refused before any member is
    bound, since the member would replace it without a word. The names
    of the body are those the namespace kept; the namespace argument of
    '__new__' is a plain dictionary with the flag names still in it when
    the class is built by calling the metaclass with one.

    Raises
    ------

    KeeMemberNameError
      The class body binds the name of a member.
    """
    flags = cls.__flag_order__
    namespace = type.__getattribute__(cls, '__namespace__')
    members, names, byNames, ids = [], [], dict(), dict()
    for mask in range(2 ** len(flags)):
      highs = (*(f for bit, f in enumerate(flags) if mask & (1 << bit)),)
      name = str.join('_', [flag.name for flag in highs]) or 'NULL'
      if dict.__contains__(namespace, name):
        raise KeeMemberNameError(cls.__name__, name)
      key = frozenset(highs)
      try:
        member = _COMBINATIONS[key]
      except KeyError:
        member = type.__call__(cls, highs, mask)
        member._settleValue()
        _COMBINATIONS[key] = member
      members.append(member)
      names.append(name)
      byNames[member.names] = member
      ids[id(member)] = member
    for name, member in zip(names, members):
      member._addOwner(cls)
      type.__setattr__(cls, name, member)
    type.__setattr__(cls, '__member_list__', members)
    type.__setattr__(cls, '__member_dict__', byNames)
    type.__setattr__(cls, '__member_ids__', ids)

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

  def _holds(cls, obj: Any) -> bool:
    """
    The members of a class are its own and those it shares with its
    bases, and a member of a subclass belongs to it as well. Only an
    object whose class a 'KeeFlagsMeta' built can be either, so anything
    else is refused before a table is read. The class holds every member
    its table of ids maps, so an id found there is taken by that member
    alone.
    """
    if not isinstance(type(obj), KeeFlagsMeta):
      return False
    if id(obj) in cls.__member_ids__:
      return True
    return True if type.__subclasscheck__(cls, type(obj)) else False

  def _resolveIndex(cls, index: int) -> KeeFlags:
    """
    The '_resolveIndex' method resolves a member from its bit mask over
    the flags of the class, its position in 'memberList'. A mask outside
    the range, a negative one included, raises 'KeeResolveError'.
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
    order, a combined name, or a mask all work, and the miss of any one
    raises 'KeeResolveError' for it. Flags beyond those of the class, as
    a member of a subclass brings, combine into no member of the class,
    and raise 'KeeResolveError' for the identifiers.
    """
    names = set()
    for identifier in identifiers:
      names.update(cls._resolveMember(identifier).names)
    key = frozenset(names)
    if key in cls.__member_dict__:
      return cls.__member_dict__[key]
    raise KeeResolveError(cls, identifiers)

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

  def _resolveMember(cls, *identifier: Any) -> KeeFlags:
    if not identifier:
      return cls.__member_list__[0]
    if len(identifier) > 1:
      return cls._resolveNames(*identifier)
    identifier = identifier[0]
    if cls._holds(identifier):
      return identifier
    if isinstance(type(identifier), KeeFlagsMeta):
      #  This branch is reached by the following:
      #  - A member of a flags class this class does not hold
      raise KeeResolveError(cls, identifier)
    if isinstance(identifier, (tuple, list, frozenset, set)):
      return cls._resolveNames(*identifier)
    #  A 'bool' is an 'int', but no mask.
    if isinstance(identifier, int) and not isinstance(identifier, bool):
      return cls._resolveIndex(identifier)
    if isinstance(identifier, str):
      return cls._resolveName(identifier)
    return cls._resolveValue(identifier)
