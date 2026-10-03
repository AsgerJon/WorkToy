"""KeeFlagsMeta provides the metaclass for KeeFlags."""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..desc import Field
from ..mcls import BaseMeta
from ..utilities import textFmt, joinWords
from ..waitaminute.keenum import KeeResolveError, KeeWriteOnceError
from ..waitaminute.keenum import KeeMemberNameError
from . import KeeFlag
from . import KeeFlagsSpace as KFSpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Self, Any, Iterator, Union
  from . import KeeFlags, KeeFlagsMeta

  Bases: TypeAlias = tuple[type, ...]
  KFMeta: TypeAlias = Union[KeeFlagsMeta, BaseMeta]


class KeeFlagsMeta(BaseMeta):
  """
  KeeFlagsMeta is the metaclass driving every 'KeeFlags' bitmask-flag
  enumeration. During '__new__' it reads the 'KeeFlag' declarations
  collected by 'KeeFlagsHook', then materializes one member per
  combination of those flags, 2 ** N members for N flags, caching them in
  'memberList' and a names-keyed 'memberDict'. The value of a member comes
  from the '_getValue' the ordinary method resolution order finds, so the
  nearest override wins, and 'cls(...)' / 'cls[...]' route through
  '_resolveMember' once instantiation is locked. A miss, by name, index
  or value, raises 'KeeResolveError', as a miss on a 'KeeNum' does, and
  'in' reports it as absent. Calling, length,
  iteration, membership, hashing, the subclass check and attribute
  assignment and deletion are the metaclass's own, so a flags class body
  binding the class hook for one of them, such as '__class_len__', is
  refused with 'ShadowedClassHook'; the hooks for the other operations,
  such as '__class_str__', work as on any class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __kee_class__ = None
  __kee_bases__ = None

  #  Private Variables
  __kee_flags__ = None
  __allow_instantiation__ = None

  #  Public Variables
  flags: Field[list[KeeFlag]] = Field()
  memberList: Field[list[KeeFlags]] = Field()
  memberDict: Field[dict[frozenset[str], KeeFlags]] = Field()
  valueType: Field[type] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @flags.GET
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

  @valueType.GET
  def _getValueType(cls) -> type:
    nullMember = cls.NULL
    return type(nullMember.value)

  @memberList.GET
  def _getMemberList(cls) -> list[KeeFlags]:
    return cls.__member_list__

  @memberDict.GET
  def _getMemberDict(cls) -> dict[str, KeeFlags]:
    return cls.__member_dict__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __subclasscheck__(cls, other: type, **kwargs) -> bool:
    if cls is other:
      return True
    if other is type(cls).__kee_class__:
      return False
    if not isinstance(other, type):
      raise TypeError('issubclass() arg 1 must be a class')
    otherKeeBases = getattr(other, '__kee_bases__', None)
    if otherKeeBases is None:
      return False
    for base in otherKeeBases:
      if base is cls or cls.__subclasscheck__(base):
        return True
    return False

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
    class, then for every subclass past the 'KeeFlags' base materializes
    all 2 ** N flag combinations as members, populating 'memberList' and
    'memberDict'.
    """
    #  The root is marked by the '_root' keyword, never by its name, and
    #  the keyword goes no further than here.
    isRoot = True if kw.pop('_root', False) else False
    cls: KFMeta = BaseMeta.__new__(mcls, name, bases, space, **kw)
    if isRoot:
      setattr(cls, '__kee_bases__', bases)
      setattr(mcls, '__kee_class__', cls)
      return cls
    setattr(cls, '__kee_bases__', bases)
    cls.__allow_instantiation__ = True
    memberList = []
    memberDict = dict()
    n = 2 ** len(cls.flags)
    for i in range(n):
      member = cls(i, )
      #  The guard is down while the members are bound, so a class-body
      #  attribute of the name would be replaced without a word.
      if dict.__contains__(space, member.name):
        raise KeeMemberNameError(name, member.name)
      setattr(member, '__field_owner__', cls)
      setattr(member, '__field_name__', member.name)
      setattr(cls, member.name, member)
      memberList.append(member)
      memberDict[member.names] = member
      #  The stamping above must precede the freeze; from here on the
      #  member is a write-once constant.
      object.__setattr__(member, '__frozen_state__', True)
    cls.__member_list__ = memberList
    cls.__member_dict__ = memberDict
    cls.__allow_instantiation__ = False
    return cls

  def __setattr__(cls, name: str, value: Any) -> None:
    """
    Rebinding a name that currently holds an enumeration member raises
    'KeeWriteOnceError': the members of an enumeration are write-once
    constants, and 'memberList' and 'memberDict' would keep serving the
    original member anyway. While '__allow_instantiation__' is high the
    guard stands down, which is the window '__new__' uses to bind the
    members in the first place.
    """
    if not cls.__allow_instantiation__:
      existing = cls.__dict__.get(name, None)
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
    existing = cls.__dict__.get(name, None)
    keeClass = type(cls).__kee_class__
    if keeClass is not None and isinstance(existing, keeClass):
      raise KeeWriteOnceError(existing, name)
    BaseMeta.__delattr__(cls, name)

  def __call__(cls, *args, **kwargs) -> Any:
    """
    Calling the class resolves the member combining the flags of the
    positional identifiers, or the empty member for none, except while
    '__new__' builds the members. A keyword has no meaning here and raises
    Python's 'TypeError', as a function given an unexpected keyword does.
    """
    if getattr(cls, '__allow_instantiation__', False):
      return BaseMeta.__call__(cls, *args, **kwargs)
    if kwargs:
      keys = joinWords(*["""'%s'""" % key for key in kwargs])
      infoSpec = """%s() takes no keyword arguments, but received %s."""
      raise TypeError(textFmt(infoSpec % (cls.__name__, keys)))
    return cls._resolveMember(*args)

  def __len__(cls) -> int:
    return len(cls.memberList)

  def __iter__(cls, ) -> Iterator[KeeFlags]:
    yield from cls.memberList

  def __contains__(cls, identifier: Any) -> bool:
    """
    The '__contains__' method reports whether 'identifier' resolves to a
    member, by any of the lookups: a miss raises 'KeeResolveError', which
    reads as absent.
    """
    try:
      _ = cls._resolveMember(identifier)
    except KeeResolveError:
      return False
    else:
      return True

  def __getitem__(cls, identifier: Any) -> KeeFlags:
    return cls._resolveMember(identifier)

  def __hash__(cls, ) -> int:
    return hash((cls.__name__, cls.__module__,))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _resolveIndex(cls, index: int) -> KeeFlags:
    for member in cls:
      if member.index == index:
        return member
    raise KeeResolveError(cls, index)

  def _resolveName(cls, name: str) -> KeeFlags:
    """
    The '_resolveName' method resolves a member from a name that matches
    the canonical name of a member ignoring case, as 'null' matches
    'NULL', or that lists the flags of a member separated by '_', in any
    order and any case. A name matching no member raises
    'KeeResolveError'.
    """
    upperName = name.upper()
    identifier = frozenset(upperName.split('_'))
    for member in cls:
      if member.name.upper() == upperName or member.names == identifier:
        return member
    raise KeeResolveError(cls, name)

  def _resolveNames(cls, *identifiers: Any) -> KeeFlags:
    """
    The '_resolveNames' method resolves several identifiers to the member
    having every flag high that any of them has. Each is resolved as a
    single lookup would resolve it, so a member, a name in any case and
    order, a combined name, or an index all work, and the miss of any one
    raises 'KeeResolveError' for it.
    """
    names = set()
    for identifier in identifiers:
      names.update(cls._resolveMember(identifier).names)
    return cls.memberDict[frozenset(names)]

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
    for member in cls:
      memberValue = member.value
      if not isinstance(value, type(memberValue)):
        continue
      if isinstance(value, bool) and not isinstance(memberValue, bool):
        continue
      if memberValue == value:
        return member
    raise KeeResolveError(cls, value)

  def _resolveMember(cls, *identifier: Any, **kwargs) -> KeeFlags:
    if not identifier:
      return cls(0, )
    if len(identifier) > 1:
      return cls._resolveNames(*identifier)
    identifier = identifier[0]
    if isinstance(identifier, cls):
      return identifier
    if isinstance(identifier, (tuple, list, frozenset, set)):
      return cls._resolveNames(*identifier)
    #  A 'bool' is an 'int', but no index.
    if isinstance(identifier, int) and not isinstance(identifier, bool):
      return cls._resolveIndex(identifier)
    if isinstance(identifier, str):
      return cls._resolveName(identifier)
    return cls._resolveValue(identifier)
