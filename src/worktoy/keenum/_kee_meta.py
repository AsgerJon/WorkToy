"""
KeeMeta is the metaclass for the 'worktoy.keenum' enumerations.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, TypeVar, Any
from collections.abc import Callable

from ..mcls import BaseMeta
from ..utilities import textFmt, joinWords
from ..waitaminute import TypeException
from ..waitaminute.keenum import KeeResolveError, KeeWriteOnceError
from . import KeeSpace as KSpace
from . import KeeBase
from . import KeeMetaMeta

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Iterator, Optional

  from . import KeeNum

  Bases: TypeAlias = tuple[type, ...]

T = TypeVar('T')


class KeeMeta(BaseMeta, metaclass=KeeMetaMeta):
  """
  KeeMeta is the metaclass driving every KeeNum-style enumeration in
  'worktoy.keenum'. It pairs with KeeSpace (the class-body namespace)
  to turn 'Kee' descriptors in the class body into a frozen sequence
  of typed members. An enumeration is asked for its members far more
  often than it is built, in loops and in every call taking a member,
  and nothing about it changes once its class statement ends, so every
  question it answers costs a lookup in a table built then.

  Class construction
  ------------------

  '__init__' runs the creators in order: '_createSpace', '_createBase',
  '_createMembers', '_createNamedMembers', '_createMemberIds',
  '_createValuedMembers' and '_validateClassResolve'. An enumeration may
  be based on several enumerations. '_createMembers' binds the members
  of the base enumerations, the same objects, in the order of the bases,
  and
  builds one member per new 'Kee' through 'type.__call__', so a call of
  the class never instantiates. The other creators build the tables the
  lookups read: the members by lower-cased name, by 'id' and by value.
  Last, '__init__' hands over to the inherited '__init__', which runs a
  '__class_init__' hook, now able to see the members, and notifies each
  base through '__subclasshook__'. The accessors 'members',
  'namedMembers', 'valuedMembers', 'valueType', 'base', 'space' and
  'mroNum' are builtin properties.

  Member resolution
  -----------------

  'cls(identifier)' and 'cls[identifier]' resolve a member in this
  order:

    1. identity: if identifier is already a member, return it.
    2. name lookup, case-insensitive, when identifier is a 'str'.
    3. a class-defined '__class_resolve__' hook, if present. Identity
       and name lookup above bypass the hook; it is consulted before
       index and value resolution, and returns 'NotImplemented' to
       defer.
    4. positional index ('cls[identifier]' only): a non-bool 'int'
       indexes the member sequence (ordinary list indexing, so
       'cls[-1]' is the last member). An out-of-range index defers.
    5. value lookup, when identifier is an instance of the member
       value type.

  Failing every applicable step raises 'KeeResolveError'.

  Because the hook is consulted before index and value, an
  enumeration whose value type is 'int' is particularly encouraged to
  implement '__class_resolve__': it lets the class decide the
  index-versus-value question for 'int' identifiers. Without a hook,
  'cls[i]' uses index before value, so with members A=2, B=5, C=9,
  'cls[2]' is C (index 2) while 'cls(2)' is A (value 2).

  Iteration, length, and membership
  ---------------------------------

  Instances of KeeMeta are iterable ('for member in MyEnum'),
  length-typed ('len(MyEnum)'), and act as their own membership
  domain: 'x in MyEnum' and 'isinstance(x, MyEnum)' are True when 'x'
  is one of the members, or a member of a subclass of
  'MyEnum'. Members are recognised by identity, so the '__eq__' of 'x'
  is never asked. These operations, and calling, printing, attribute
  access and the instance and subclass checks, are the metaclass's own,
  so an enumeration body binding the class hook for one of them, such as
  '__class_len__' or '__class_call__', is refused with
  'ShadowedClassHook', since the hook would never be called. The subclass
  check of an enumeration is that of 'type'. The hooks for the
  operations left to 'AbstractMetaclass', such as '__class_hash__', work
  as on any class, and so do '__class_init__' and '__class_resolve__'.

  Subclassing through KeeMetaMeta
  -------------------------------

  Subclassing KeeMeta to extend behavior requires using the
  'metaclass.keeNum' attribute (provided by KeeMetaMeta) as the base
  for the actual enumeration class. See KeeMetaMeta's docstring for
  the recommended pattern.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Annotations
  __class_resolve__: Callable[[Any], Any]

  #  Private Variables
  __name_space__: Optional[KSpace] = None
  __base_class__: Optional[KeeMeta] = None
  __allow_instantiation__: bool = False
  __custom_resolve__: Optional[bool] = None
  __registered_members__: tuple[Any, ...] = ()
  __member_type__: Optional[type] = None
  __named_members__: Optional[dict[str, Any]] = None
  __member_ids__: MappingProxyType = MappingProxyType({})
  __valued_members__: Optional[dict[Any, Any]] = None
  __value_scan__: bool = False

  if TYPE_CHECKING:  # pragma: no cover, no mutate
    #  'KeeMetaMeta' provides 'keeNum' on the metaclass; this hint only
    #  lets a type checker see it.
    keeNum: KeeMeta

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createSpace(cls) -> None:
    if isinstance(cls.__namespace__, KSpace):
      type.__setattr__(cls, '__name_space__', cls.__namespace__)
    else:
      raise TypeException('__namespace__', cls.__namespace__, KSpace)

  def _getSpace(cls, **kwargs) -> KSpace:
    if cls.__name_space__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls._createSpace()
      return cls._getSpace(_recursion=True)  # pragma: no mutate
    return cls.__name_space__

  def _createBase(cls, ) -> None:
    """
    The '_createBase' method finds the base enumeration of 'cls'. The
    root of the metaclass, the class its 'keeNum' descriptor builds, is
    its own base, and so is every enumeration that subclasses that root
    alone. Any other enumeration has as its base the first enumeration
    it subclasses other than the root; it may subclass several. The
    root is recognised by identity, never by name, since each subclass
    of 'KeeMeta' builds a root of its own name.
    """
    mcls = type(cls)
    root = mcls.keeNum
    if cls is root:
      type.__setattr__(cls, '__base_class__', cls)
      return
    space = cls._getSpace()
    bases = [b for b in space.__base_classes__ if isinstance(b, mcls)]
    if not bases:
      infoSpec = """An enumeration of '%s' must be based on '%s.keeNum',
      its root, or on an enumeration based on it, but '%s' has the
      bases: (%s)."""
      given = ', '.join(b.__name__ for b in space.__base_classes__)
      mclsName = mcls.__name__
      info = infoSpec % (mclsName, mclsName, cls.__name__, given)
      raise ValueError(textFmt(info))
    for base in bases:
      if base is not root:
        type.__setattr__(cls, '__base_class__', base)
        return
    type.__setattr__(cls, '__base_class__', cls)

  def _getBase(cls, **kwargs) -> KeeMeta:
    if cls.__base_class__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls._createBase()
      return cls._getBase(_recursion=True)  # pragma: no mutate
    return cls.__base_class__

  def _getMroNum(cls, ) -> tuple[KeeMeta, ...]:
    """
    The 'mroNum' getter gives the enumerations 'cls' is based on, in its
    resolution order, the root of its metaclass left out.
    """
    mcls = type(cls)
    root = mcls.keeNum
    out = []
    for base in cls.__mro__[1:]:
      if isinstance(base, mcls) and base is not root:
        out.append(base)
    return (*out,)

  def _createMembers(cls, ) -> None:
    """
    The '_createMembers' method builds the members, in the order the
    namespace registered them. A member a base enumeration already has
    under the name is the same member here, with the 'Kee' and the index
    it has there; anything else a base holds under the name, such as a
    plain class attribute, gives way to a new member. The 'Kee' of a new
    member is placed on the enumeration first, as a box is placed on its
    class, which refuses a 'Kee' declared without parentheses or
    declared in another enumeration already, and then receives its
    index, the position of the member. Each member is built by
    'type.__call__', past the call of the class, which resolves, and
    each member, inherited or new, records the class among its owners.
    """
    type.__setattr__(cls, '__allow_instantiation__', True)
    registry = []
    members = cls._getSpace().__enumeration_members__.items()
    for index, (key, kee) in enumerate(members):
      member = cls._getInheritedMember(key)
      if member is None:
        kee.__set_name__(cls, key)
        kee._setIndex(index)
        member = type.__call__(cls, kee)
      member._addOwner(cls)
      type.__setattr__(cls, key, member)
      registry.append(member)
    type.__setattr__(cls, '__registered_members__', (*registry,))
    type.__setattr__(cls, '__allow_instantiation__', False)

  def _getInheritedMember(cls, key: str) -> Any:
    """
    The '_getInheritedMember' method returns the member named 'key' of
    the base enumerations, or None when no base holds a member of that
    name. The namespace gathered them from every base as it was made.
    """
    inherited = cls._getSpace().__inherited_members__
    try:
      return inherited[key]
    except KeyError:
      return None

  def _getMembers(cls, **kwargs) -> tuple[Any, ...]:
    if cls.__registered_members__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      type.__setattr__(cls, '__registered_members__', ())
      return cls._getMembers(_recursion=True)  # pragma: no mutate
    return cls.__registered_members__

  def _getValueType(cls, ) -> type:
    """
    The 'valueType' getter returns the type the members were declared
    with, 'T' in 'Kee[T]', which 'KeeSpace' pins for every member of the
    enumeration as the body runs, refusing a second type. The values may
    be instances of subclasses of it, as a 'bool' among 'int' values.
    An enumeration without members has no declared type and raises
    'TypeError'.
    """
    type_ = cls._getSpace().__member_type__
    if type_ is None:
      infoSpec = """KeeNum class '%s' has no members, so it has no
      'valueType'."""
      info = infoSpec % (cls.__name__,)
      raise TypeError(textFmt(info))
    return type_

  def _createNamedMembers(cls) -> None:
    """
    The '_createNamedMembers' method populates the '__named_members__'
    table, mapping each member's lowercased name to the member.
    """
    cache = {}
    for member in cls._getMembers():
      cache[member.name.lower()] = member
    type.__setattr__(cls, '__named_members__', cache)

  def _getNamedMembers(cls, **kwargs) -> dict[str, Any]:
    if cls.__named_members__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls._createNamedMembers()
      return cls._getNamedMembers(_recursion=True)  # pragma: no mutate
    return cls.__named_members__

  def _createMemberIds(cls) -> None:
    """
    The '_createMemberIds' method populates the '__member_ids__' table,
    mapping the 'id' of each member to the member, so the instance check
    finds an inherited member in one lookup. The class holds every member
    it maps, so no 'id' in the table can be reused while the class lives.
    """
    cache = {}
    for member in cls._getMembers():
      cache[id(member)] = member
    type.__setattr__(cls, '__member_ids__', cache)

  def _createValuedMembers(cls) -> None:
    """
    The '_createValuedMembers' method populates the '__valued_members__'
    table, mapping each hashable value to the first member carrying it. A
    single unhashable value collapses the table to an '__unhashable__'
    marker and raises the flag '__value_scan__', so value resolution
    compares with every member in turn.
    """
    cache = {}
    for member in cls._getMembers():
      try:
        _ = hash(member.value)
        key = member.value
      except TypeError:
        break
      else:
        if key in cache:
          continue
        cache[key] = member
    else:
      type.__setattr__(cls, '__valued_members__', cache)
      type.__setattr__(cls, '__value_scan__', False)
      return
    marker = dict(__unhashable__=member.value, )
    type.__setattr__(cls, '__valued_members__', marker)
    type.__setattr__(cls, '__value_scan__', True)

  def _getValuedMembers(cls, **kwargs) -> dict[Any, Any]:
    if cls.__valued_members__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls._createValuedMembers()
      return cls._getValuedMembers(_recursion=True)  # pragma: no mutate
    return cls.__valued_members__

  def _validateClassResolve(cls) -> None:
    """
    The lookups ask '__class_resolve__' only when the class has one, so
    the metaclass records once, as the class is created, whether a
    callable hook is found along the resolution order; 'None' at the
    name declares none, as a subclass may bind to drop an inherited
    hook.

    Raises
    ------

    TypeException
      '__class_resolve__' is bound to something that is not callable.
    """
    try:
      classResolve = type.__getattribute__(cls, '__class_resolve__')
    except AttributeError:
      type.__setattr__(cls, '__custom_resolve__', False)
      return
    if classResolve is None:
      type.__setattr__(cls, '__custom_resolve__', False)
      return
    if not callable(classResolve):
      raise TypeException('__class_resolve__', classResolve, Callable)
    type.__setattr__(cls, '__custom_resolve__', True)

  space = property(_getSpace)
  base = property(_getBase)
  mroNum = property(_getMroNum)
  members = property(_getMembers)
  valueType = property(_getValueType)
  namedMembers = property(_getNamedMembers)
  valuedMembers = property(_getValuedMembers)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __prepare__(
      mcls,
      name: str,
      bases: Bases,
      **kw: Any,
  ) -> KSpace:
    """
    The '__prepare__' method returns a 'KeeSpace' as the class-body
    namespace.
    """
    return KSpace(mcls, name, bases, **kw)

  def __call__(cls: KeeMeta, *args, **kwargs) -> T:
    """
    Calling the class resolves a member from one identifier; any other
    arguments raise Python's 'TypeError'; see '_refuseCallArguments'. The
    members are built past this method, by '_createMembers'.
    """
    if kwargs or len(args) != 1:
      cls._refuseCallArguments(args, kwargs)
    return cls._resolveMember(args[0])

  def __getitem__(cls, identifier: Any) -> Any:
    """
    The '__getitem__' method resolves a member by identifier with the
    positional-index step enabled, so an identifier that is already a
    member passes through, then a name, then '__class_resolve__', then a
    non-bool 'int' as a positional index, then value.
    """
    return cls._resolveMember(identifier, allowIndex=True)

  def __getattr__(cls, name: str) -> Any:
    """
    An attribute miss on an enumeration is a member name in another
    case, as 'Color.red' for 'Color.RED', since the members of the base
    are registered on the class as its own and ordinary lookup finds
    every member by its name. A name that is no member falls through to
    the ordinary attribute error.
    """
    named = cls._getNamedMembers()
    key = name.lower()
    if key in named:
      return named[key]
    return type.__getattribute__(cls, name)

  def __setattr__(cls, name: str, value: Any) -> None:
    """
    Rebinding a name that currently holds an enumeration member raises
    'KeeWriteOnceError': the members of an enumeration are write-once
    constants, and the resolution tables would keep serving the original
    member anyway.
    """
    try:
      existing = cls.__dict__[name]
    except KeyError:
      pass
    else:
      if isinstance(existing, KeeBase):
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
      if isinstance(existing, KeeBase):
        raise KeeWriteOnceError(existing, name)
    BaseMeta.__delattr__(cls, name)

  def __iter__(cls) -> Iterator[Any]:
    return iter(cls.__registered_members__)

  def __len__(cls) -> int:
    return len(cls.__registered_members__)

  def __contains__(cls, identifier: Any) -> bool:
    """
    The '__contains__' method reports membership by identity, as the
    instance check does: 'x in cls' is True when 'x' is one of the members
    of 'cls', or a member of a subclass of it, which holds for an
    enumeration without members of its own as well.
    """
    return cls._holds(identifier)

  def __instancecheck__(cls, instance: Any) -> bool:
    """
    The '__instancecheck__' method treats 'instance' as a member when it
    is one of the members of the enumeration, or a member of a
    subclass of it. A member is recognised by identity:
    comparing with '==' would hand the decision to the '__eq__' of
    'instance', which may raise on a member or answer 'True' to anything.
    """
    return cls._holds(instance)

  __subclasscheck__ = type.__subclasscheck__

  def __str__(cls) -> str:
    """
    The 'str()' of an enumeration names its kind, the root of its
    metaclass, which is 'KeeNum' for 'KeeMeta' itself, and counts the
    members.
    """
    infoSpec = """<%s '%s': %d %s>"""
    kind = type(cls).keeNum.__name__
    count = len(cls)
    members = 'member' if count == 1 else 'members'
    return infoSpec % (kind, cls.__name__, count, members)

  __repr__ = __str__

  def __bool__(cls, ) -> bool:
    """
    A KeeNum class is truthy when it has at least one member.
    """
    return True if cls.__registered_members__ else False

  @classmethod
  def __init_subclass__(mcls, **kwargs) -> None:
    setattr(mcls, '__kee_num__', None)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __new__(mcls, name: str, bases: Bases, space: KSpace, **kw) -> T:
    # noinspection PyTypeChecker
    return super().__new__(mcls, name, bases, space, **kw)

  def __init__(cls, name: str, bases: Bases, space: KSpace, **kw) -> None:
    """
    The '__init__' method builds the members of the enumeration and the
    tables the lookups read, and then hands over to the inherited
    '__init__', which runs '__class_init__' and notifies each base
    through '__subclasshook__'. Coming last, the hook sees the finished
    members.
    """
    cls._createSpace()
    cls._createBase()
    cls._createMembers()
    cls._createNamedMembers()
    cls._createMemberIds()
    cls._createValuedMembers()
    cls._validateClassResolve()
    BaseMeta.__init__(cls, name, bases, space, **kw)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _refuseCallArguments(cls, args: tuple, kwargs: dict) -> None:
    """
    The '_refuseCallArguments' method raises Python's 'TypeError', as a
    function given the wrong arguments does, for a call to the class that
    gives any keyword, or that gives other than exactly one positional
    argument, the identifier the call resolves a member from. '__call__'
    calls it only for such a call, so it always raises.
    """
    if kwargs:
      keys = joinWords(*["""'%s'""" % key for key in kwargs])
      infoSpec = """%s() takes no keyword arguments, but received %s."""
      raise TypeError(textFmt(infoSpec % (cls.__name__, keys)))
    infoSpec = """%s() takes exactly one argument, the identifier of a
    member, but received %d."""
    raise TypeError(textFmt(infoSpec % (cls.__name__, len(args))))

  def _holds(cls, obj: Any) -> bool:
    """
    The members of a class are its own and those it inherits, and a
    member of a subclass belongs to it as well. Only an object whose
    class a 'KeeMeta' built can be either, so anything else is refused
    before a table is read. The class holds every member its table of
    ids maps, so an id found there is taken by that member alone.
    """
    if not isinstance(type(obj), KeeMeta):
      return False
    if id(obj) in cls.__member_ids__:
      return True
    return True if type.__subclasscheck__(cls, type(obj)) else False

  def _resolveFromName(cls, identifier: str) -> Any:
    """
    The '_resolveFromName' method resolves a member by name
    (case-insensitive).

    Parameters
    ----------

    identifier : str
      The string identifier to resolve.

    Returns
    -------

    Any
      The resolved member, or 'NotImplemented' if resolution fails.
    """
    named = cls.__named_members__
    key = identifier.lower()
    if key in named:
      return named[key]
    return NotImplemented

  def _resolveFromValue(cls, identifier: Any, valueType: type) -> Any:
    """
    The '_resolveFromValue' method gives the first member whose 'value'
    equals 'identifier', or 'NotImplemented' when none does. The caller
    hands over the value type it has read.

    Parameters
    ----------

    identifier : Any
      The value identifier to resolve.

    valueType : type
      The value type of the enumeration, as 'valueType' gave it.

    Returns
    -------

    KeeNum or NotImplemented
      The resolved member, or 'NotImplemented' if resolution fails.
    """
    if valueType is int:
      if identifier is True or identifier is False:
        return NotImplemented
    if cls.__value_scan__:
      return cls._scanValues(identifier)
    try:
      hash(identifier)
    except TypeError:
      #  The table is keyed by hash, so an unhashable identifier is
      #  compared with each value instead, as an unhashable value is.
      return cls._scanValues(identifier)
    valued = cls.__valued_members__
    if identifier in valued:
      return valued[identifier]
    return NotImplemented

  def _scanValues(cls, identifier: Any) -> Any:
    """
    The '_scanValues' method returns the first member whose 'value'
    equals 'identifier', compared one by one, or 'NotImplemented' when
    none does. Value resolution falls back to it where hashing fails, for
    a member value or for the identifier.
    """
    for member in cls.__registered_members__:
      if member.value == identifier:
        return member
    return NotImplemented

  def _resolveMember(cls, identifier: Any, allowIndex: bool = False) -> Any:
    """
    The '_resolveMember' method is the one resolver behind a call and a
    subscript of the class, applying the steps below in order.

    Order
    -----

    1. Identity: if 'identifier' is already a member, return it.
    2. Name resolution (case-insensitive) when 'identifier' is a
       'str'.
    3. The class '__class_resolve__' hook, if present. Identity and
       name resolution above bypass it; it is consulted before index
       and value resolution.
    4. Positional index, only when 'allowIndex=True' (set by
       '__getitem__'): a non-bool 'int' indexes the member sequence.
    5. Value resolution when 'identifier' is of the 'valueType'.
    6. If all else fails, raise 'KeeResolveError'.

    Raises
    ------

    KeeResolveError
      If resolution fails at all levels, a 'KeeResolveError' is raised
      containing the 'KeeNum' class and the identifier that failed to
      resolve.

    Parameters
    ----------

    identifier : Any
      The identifier to resolve.

    allowIndex : bool, optional
      Whether a non-bool 'int' is tried as a position.

    Returns
    -------

    KeeNum
      The resolved enumeration member.
    """
    if cls._holds(identifier):
      return identifier
    if isinstance(identifier, str):
      resolved = cls._resolveFromName(identifier)
      if resolved is not NotImplemented:
        return resolved
    if cls.__custom_resolve__:
      resolved = cls.__class_resolve__(identifier)
      if resolved is not NotImplemented:
        return resolved
    members = cls.__registered_members__
    if allowIndex:
      if isinstance(identifier, int):
        if identifier is not True and identifier is not False:
          try:
            return members[identifier]
          except IndexError:
            pass
    #  An enumeration without members has no value type to ask for.
    if members:
      valueType = cls.__member_type__
      if isinstance(identifier, valueType):
        resolved = cls._resolveFromValue(identifier, valueType)
        if resolved is not NotImplemented:
          return resolved
    raise KeeResolveError(cls, identifier)

  def fromValue(cls, value: Any) -> Any:
    """
    A project holding a value may need the member carrying it, without
    the name and position steps a call or a subscript makes first.

    Implementation
    --------------

    The lowest-indexed member whose 'value' equals the argument answers.
    An enumeration without members has none, and raises
    'KeeResolveError' whatever the value.

    Raises
    ------

    TypeException
      The value is not of the value type.

    KeeResolveError
      No member carries the value.
    """
    if not cls._getMembers():
      raise KeeResolveError(cls, value)
    valueType = cls._getValueType()
    if not isinstance(value, valueType):
      raise TypeException('value', value, valueType)
    resolved = cls._resolveFromValue(value, valueType)
    if resolved is NotImplemented:
      raise KeeResolveError(cls, value)
    return resolved


# @formatter:off
if TYPE_CHECKING:  # pragma: no cover, no mutate
  class KeeNum(KeeBase, metaclass = KeeMeta):  # noqa
    """
    This is to PyCharm's typing what samizdat was to the USSR.

    See: https://www.britannica.com/technology/samizdat

    We grant you a seat on the 'if TYPE_CHECKING' block, but we do not
    grant you rank of "type hint".
    """
    def __call__(self: Any, *args, **kwargs) -> Any: ...
    def fromValue(self: Any, *args, **kwargs) -> Any: ...
    def __getattr__(self: Any, *args, **kwargs) -> Any: ...
    def __iter__(self: Any,) -> Any: ...
    def __len__(self: Any,) -> int: ...
    def __contains__(self: Any, *args, **kwargs) -> bool: ...
    def __instancecheck__(self: Any, *args, **kwargs) -> bool: ...
    def __subclasscheck__(self: Any, *args, **kwargs) -> bool: ...
# @formatter:on
else:
  KeeNum = KeeMeta.keeNum  # noqa

__all__ = ('KeeMeta', 'KeeNum',)
