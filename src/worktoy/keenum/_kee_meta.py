"""
KeeMeta is the metaclass for the 'worktoy.keenum' enumerations.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Any
from collections.abc import Callable

from ..desc import Field
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
  of typed members.

  Class construction
  ------------------
  During '__new__', the namespace collected by KeeSpaceHook is handed
  off in '__init__', which then runs the lazy creators
  ('_createSpace', '_createBase', '_createMembers',
  '_createNamedMembers', '_createValuedMembers',
  '_validateClassResolve'). Each populates a private slot consulted
  by a public Field with a '_recursion=True' guard to detect
  population failure. After this, '__allow_instantiation__' is False
  and direct construction routes through '_resolveMember' instead.
  Last, '__init__' hands over to the inherited '__init__', which runs a
  '__class_init__' hook, now able to see the members, and notifies each
  base through '__subclasshook__'.

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
  'ShadowedClassHook', since the hook would never be called. The hooks
  for the operations left to 'AbstractMetaclass', such as
  '__class_hash__', work as on any class, and so do '__class_init__' and
  '__class_resolve__'.

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
  __registered_members__: Optional[tuple[Any, ...]] = None
  __named_members__: Optional[dict[str, Any]] = None
  __valued_members__: Optional[dict[Any, Any]] = None

  base: Field[KeeMeta] = Field()
  space: Field[KSpace] = Field()
  mroNum: Field[tuple[KeeMeta, ...]] = Field()
  members: Field[tuple[KeeNum, ...]] = Field()
  valueType: Field[type] = Field()
  namedMembers: Field[dict[str, KeeNum]] = Field()
  valuedMembers: Field[dict[Any, KeeNum]] = Field()
  if TYPE_CHECKING:  # pragma: no cover, no mutate
    #  'KeeMetaMeta' provides 'keeNum' on the metaclass; this hint only
    #  lets a type checker see it, and a 'Field' here, with no getter,
    #  would answer every enumeration with 'AccessError'.
    keeNum: Field[KeeMeta] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createSpace(cls) -> None:
    if isinstance(cls.__namespace__, KSpace):
      cls.__name_space__ = cls.__namespace__
    else:
      raise TypeException('__namespace__', cls.__namespace__, KSpace)

  @space.GET
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
    directly. Any other enumeration has the enumeration it subclasses as
    its base. The root is recognised by identity, never by name, since
    each subclass of 'KeeMeta' builds a root of its own name.
    """
    mcls = type(cls)
    root = mcls.keeNum
    if cls is root:
      cls.__base_class__ = cls
    else:
      bases = [b for b in cls.space.__base_classes__ if isinstance(b, mcls)]
      if len(bases) != 1:
        if bases:
          infoSpec = """Enumerating classes that are instances of '%s'
          may not have multiple bases, but received %d:<br><tab>%s"""
          mclsName = mcls.__name__
          bases = cls.space.__base_classes__
          baseStr = '<br><tab>'.join(b.__name__ for b in bases)
          info = infoSpec % (mclsName, len(bases), baseStr)
        else:
          infoSpec = """An enumeration of '%s' must be based on '%s.keeNum',
          its root, or on an enumeration based on it, but '%s' has the
          bases: (%s)."""
          given = ', '.join(b.__name__ for b in cls.space.__base_classes__)
          mclsName = mcls.__name__
          info = infoSpec % (mclsName, mclsName, cls.__name__, given)
        raise ValueError(textFmt(info))
      base = bases[0]
      cls.__base_class__ = cls if base is root else base

  @base.GET
  def _getBase(cls, **kwargs) -> KeeMeta:
    if cls.__base_class__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls._createBase()
      return cls._getBase(_recursion=True)  # pragma: no mutate
    return cls.__base_class__

  @mroNum.GET
  def _getMroNum(cls, ) -> tuple[KeeMeta, ...]:
    return () if cls.base is cls else (cls.base, *cls.base.mroNum,)

  def _createMembers(cls, ) -> None:
    """
    The '_createMembers' method builds the members, in the order the
    namespace registered them. A member the base enumeration already has
    under the name is the same member here, with the 'Kee' and the index
    it has there; anything else the base holds under the name, such as a
    plain class attribute or a member of some other enumeration, gives
    way to a new member. The 'Kee' of a new member is placed on the
    enumeration first, as a box is placed on its class, which refuses a
    'Kee' declared without parentheses or declared in another
    enumeration already, and then receives its index, the position of
    the member.
    """
    type.__setattr__(cls, '__allow_instantiation__', True)
    registry = []
    members = cls.space.__enumeration_members__.items()
    for index, (key, kee) in enumerate(members):
      member = cls._getInheritedMember(key)
      if member is None:
        kee.__set_name__(cls, key)
        kee.index = index
        member = cls(kee, )
      setattr(cls, key, member)
      registry.append(member)
    cls.__registered_members__ = (*registry,)
    type.__setattr__(cls, '__allow_instantiation__', False)

  def _getInheritedMember(cls, key: str) -> Any:
    """
    The '_getInheritedMember' method returns the member of the base
    enumeration named 'key', or None when the base holds no member of
    that name.
    """
    base = cls.base
    try:
      member = type.__getattribute__(base, key)
    except AttributeError:
      return None
    return member if isinstance(member, base) else None

  @members.GET
  def _getMembers(cls, **kwargs) -> tuple[Any, ...]:
    if cls.__registered_members__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls.__registered_members__ = ()
      return cls._getMembers(_recursion=True)  # pragma: no mutate
    return cls.__registered_members__

  @valueType.GET
  def _getValueType(cls, ) -> type:
    """
    The 'valueType' getter returns the type the members were declared
    with, 'T' in 'Kee[T]', which 'KeeSpace' pins for every member of the
    enumeration as the body runs, refusing a second type. The values may
    be instances of subclasses of it, as a 'bool' among 'int' values,
    and each is checked against it by its own 'Kee' at every read, so
    this getter reads no member. An enumeration without members has no
    declared type and raises 'TypeError'.
    """
    type_ = cls.space.__member_type__
    if type_ is None:
      infoSpec = """KeeNum class '%s' has no members, so it has no
      'valueType'."""
      info = infoSpec % (cls.__name__,)
      raise TypeError(textFmt(info))
    return type_

  def _createNamedMembers(cls) -> None:
    """
    The '_createNamedMembers' method populates the '__named_members__'
    cache, mapping each member's lowercased name to the member.
    """
    cache = {}
    for member in cls.members:
      cache[member.name.lower()] = member
    cls.__named_members__ = cache

  @namedMembers.GET
  def _getNamedMembers(cls, **kwargs) -> dict[str, Any]:
    if cls.__named_members__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls._createNamedMembers()
      return cls._getNamedMembers(_recursion=True)  # pragma: no mutate
    return cls.__named_members__

  def _createValuedMembers(cls) -> None:
    """
    The '_createValuedMembers' method populates the '__valued_members__'
    cache, mapping each hashable value to the first member carrying it. A
    single unhashable value collapses the cache to an '__unhashable__'
    marker, so value resolution falls back to a linear scan.
    """
    cache = {}
    for member in cls:
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
      cls.__valued_members__ = cache
      return
    cls.__valued_members__ = dict(__unhashable__=member.value, )

  @valuedMembers.GET
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
      cls.__custom_resolve__ = False
      return
    if classResolve is None:
      cls.__custom_resolve__ = False
      return
    if not callable(classResolve):
      raise TypeException('__class_resolve__', classResolve, Callable)
    cls.__custom_resolve__ = True

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
    Calling the class resolves a member from the identifier, except during
    class creation, when '__allow_instantiation__' is set and the call
    instantiates a member instead. A call resolves one member from one
    identifier, so any other arguments raise Python's 'TypeError'; see
    '_refuseCallArguments'.
    """
    if cls.__allow_instantiation__:
      return super().__call__(*args, **kwargs)
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
    value = cls._resolveFromName(name)
    if value is NotImplemented:
      return type.__getattribute__(cls, name)
    return value

  def __setattr__(cls, name: str, value: Any) -> None:
    """
    Rebinding a name that currently holds an enumeration member raises
    'KeeWriteOnceError': the members of an enumeration are write-once
    constants, and the resolution caches would keep serving the original
    member anyway. While '__allow_instantiation__' is high the guard
    stands down, which is the window '_createMembers' uses to bind the
    members in the first place.
    """
    if not cls.__allow_instantiation__:
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
    yield from cls.members

  def __len__(cls) -> int:
    return len(cls.members)

  def __contains__(cls, identifier: Any) -> bool:
    """
    The '__contains__' method reports membership by identity: 'x in cls'
    is True only when 'x' is an instance of 'cls', that is, one of its
    members.
    """
    if not cls:
      return False
    if isinstance(identifier, cls):
      return True
    return False

  def __instancecheck__(cls, instance: Any) -> bool:
    """
    The '__instancecheck__' method treats 'instance' as a member when it
    is one of the members of the enumeration, or a member of a
    subclass of it. A member is recognised by identity:
    comparing with '==' would hand the decision to the '__eq__' of
    'instance', which may raise on a member or answer 'True' to anything.
    """
    for member in cls:
      if member is instance:
        return True
    if issubclass(type(instance), cls):
      return True
    return False

  def __subclasscheck__(cls, subclass: type) -> bool:
    """
    The '__subclasscheck__' method reports whether 'cls' appears in the
    MRO of 'subclass'.
    """
    _ = issubclass(subclass, object)
    for item in subclass.__mro__:
      if item is cls:
        return True
    return False

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
    return True if cls.members else False

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
    The '__init__' method builds the members of the enumeration and then
    hands over to the inherited '__init__', which runs '__class_init__'
    and notifies each base through '__subclasshook__'. Coming last, the
    hook sees the finished members.
    """
    cls._createSpace()
    cls._createBase()
    cls._createMembers()
    cls._createNamedMembers()
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
    argument, the identifier the call resolves a member from.
    """
    if kwargs:
      keys = joinWords(*["""'%s'""" % key for key in kwargs])
      infoSpec = """%s() takes no keyword arguments, but received %s."""
      raise TypeError(textFmt(infoSpec % (cls.__name__, keys)))
    if len(args) != 1:
      infoSpec = """%s() takes exactly one argument, the identifier of a
      member, but received %d."""
      raise TypeError(textFmt(infoSpec % (cls.__name__, len(args))))

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
    try:
      member = cls.namedMembers[identifier.lower()]
    except KeyError:
      return NotImplemented
    else:
      return member

  def _resolveFromValue(cls, identifier: Any, valueType: type) -> Any:
    """
    The '_resolveFromValue' method gives the first member whose 'value'
    equals 'identifier', or 'NotImplemented' when none does. The caller
    hands over the value type it has read, since reading 'valueType'
    checks every member's value.

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
    if '__unhashable__' in cls.valuedMembers:
      return cls._scanValues(identifier)
    try:
      hash(identifier)
    except TypeError:
      #  The cache is keyed by hash, so an unhashable identifier is
      #  compared with each value instead, as an unhashable value is.
      return cls._scanValues(identifier)
    try:
      member = cls.valuedMembers[identifier]
    except KeyError:
      return NotImplemented
    else:
      return member

  def _scanValues(cls, identifier: Any) -> Any:
    """
    The '_scanValues' method returns the first member whose 'value'
    equals 'identifier', compared one by one, or 'NotImplemented' when
    none does. Value resolution falls back to it where hashing fails, for
    a member value or for the identifier.
    """
    for member in cls:
      if member.value == identifier:
        return member
    return NotImplemented

  def _resolveMember(cls, identifier: Any, **kwargs) -> Any:
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

    Returns
    -------
    KeeNum
      The resolved enumeration member.
    """
    if isinstance(identifier, cls):
      return identifier
    if isinstance(identifier, str):
      resolved = cls._resolveFromName(identifier)
      if resolved is not NotImplemented:
        return resolved
    if cls.__custom_resolve__:
      resolved = cls.__class_resolve__(identifier)
      if resolved is not NotImplemented:
        return resolved
    if kwargs.get('allowIndex', False):
      if isinstance(identifier, int):
        if identifier is not True and identifier is not False:
          try:
            return cls.members[identifier]
          except IndexError:
            pass
    #  An enumeration without members has no value type to ask for.
    if cls.members:
      valueType = cls.valueType
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
    if not cls.members:
      raise KeeResolveError(cls, value)
    valueType = cls.valueType
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
