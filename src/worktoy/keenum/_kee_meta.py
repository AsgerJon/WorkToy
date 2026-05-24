"""
KeeMeta provides the metaclass for the 'worktoy.keenum' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Any
from collections.abc import Callable

from ..core import MetaType
from ..desc import Field
from ..mcls import BaseMeta
from ..utilities import textFmt
from ..waitaminute import TypeException
from ..waitaminute.keenum import KeeResolveError
from . import KeeSpace as KSpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Iterator, Optional

  from . import KeeNum

  Bases: TypeAlias = tuple[type, ...]

T = TypeVar('T')


class KeeMetaMeta(MetaType):
  """
  This is the meta-metaclass of the 'worktoy.keenum' package. It allows
  derived metaclasses to access their dedicated derived root class through
  the descriptor protocol. For the recommended 'KeeMeta' metaclass,
  the value retrieved from 'KeeMeta.keeNum' is identical to the 'KeeNum'
  class. When deriving a new class from a subclass of 'KeeMeta', set as
  base class of the new class the 'keeNum' attribute of the custom
  metaclass.
  For example, suppose 'FontMeta' was a subclass of 'KeeMeta' and
  'FontFamilyNum' was an enumerating class derived from 'FontMeta',
  the following would be the recommended syntax:

  class FontMeta(KeeMeta):
    pass

  class FontFamilyNum(FontMeta.keeNum):
    ARIAL = Kee[int](1)
    TIMES_NEW_ROMAN = Kee[int](2)
    CALIBRI = Kee[int](3)
    ... etc.

  The '__init_subclass__' implementation of 'KeeMeta' removes 'KeeNum'
  from being retrievable from the private attribute '__kee_num__'. Thus,
  calls to the getter function for 'keeNum' on subclasses of 'KeeMeta'
  will trigger the creation of a new 'KeeNum'-like class for that metaclass.
  """

  __kee_num__: Any = None
  keeNum: Field[KeeMeta] = Field()

  @keeNum.GET
  def _getKeeNum(mcls, **kwargs) -> KeeMeta:  # noqa N805
    from . import _KeeBase
    if mcls.__kee_num__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      num = """%sNum""" % (mcls.__name__,)
      name = 'KeeNum' if mcls.__name__ == 'KeeMeta' else num
      numSpace = KSpace(mcls, name, (_KeeBase,), _root=True)
      numSpace['__root_class__'] = True
      numSpace['__doc__'] = _KeeBase.__doc__
      # noinspection PyTypeChecker
      num = mcls.__new__(mcls, name, (_KeeBase,), numSpace, _root=True)
      mcls.__kee_num__ = num
      return mcls._getKeeNum(_recursion=True, )
    return mcls.__kee_num__


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

  Member resolution
  -----------------
  'cls(identifier)' and 'cls[identifier]' both call '_resolveMember',
  which tries in order:

    1. identity (if identifier is already a member, return it)
    2. case-insensitive name lookup
    3. a class-defined '__class_resolve__' hook (if present)
    4. value lookup via 'valueType' / 'fromValue'

  Failure at all four raises 'KeeResolveError'. Subclasses may
  declare '__class_resolve__' to intercept resolution before the
  value-based fallback.

  Iteration, length, and membership
  ---------------------------------
  Instances of KeeMeta are iterable ('for member in MyEnum'),
  length-typed ('len(MyEnum)'), and act as their own membership
  domain ('x in MyEnum' is True iff x is one of the members).
  'isinstance(x, MyEnum)' is True when 'x' equals any member or
  belongs to a subclass.

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
  __kee_num__: Optional[KeeMeta] = None

  base: Field[KeeMeta] = Field()
  space: Field[KSpace] = Field()
  mroNum: Field[tuple[KeeMeta, ...]] = Field()
  members: Field[tuple[KeeNum, ...]] = Field()
  valueType: Field[type] = Field()
  namedMembers: Field[dict[str, KeeNum]] = Field()
  valuedMembers: Field[dict[Any, KeeNum]] = Field()
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
    """Returns the namespace of 'keeNum'."""
    if cls.__name_space__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls._createSpace()
      return cls._getSpace(_recursion=True, )
    return cls.__name_space__

  def _createBase(cls, ) -> None:
    if cls.__name__ == 'KeeNum':
      cls.__base_class__ = cls
    else:
      mcls = type(cls)
      bases = [b for b in cls.space.__base_classes__ if isinstance(b, mcls)]
      if len(bases) != 1:
        if bases:
          infoSpec = """Enumerating classes derived from '%s', may not have 
          multiple bases, but received %d:<br>%s"""
          mclsName = mcls.__name__
          bases = cls.space.__base_classes__
          baseStr = '<tab><br>'.join(b.__name__ for b in bases)
          info = infoSpec % (mclsName, len(bases), baseStr)
        else:
          infoSpec = """Enumerating classes derived from '%s', must have 
          exactly one base, but received none!"""
          info = infoSpec % (mcls.__name__,)
        raise ValueError(textFmt(info))
      base = bases[0]
      cls.__base_class__ = cls if base.__name__ == 'KeeNum' else base

  @base.GET
  def _getBase(cls, **kwargs) -> KeeMeta:
    """Returns the nearest non-Object base of 'keeNum'."""
    if cls.__base_class__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls._createBase()
      return cls._getBase(_recursion=True, )
    return cls.__base_class__

  @mroNum.GET
  def _getMroNum(cls, ) -> tuple[KeeMeta, ...]:
    return () if cls.base is cls else (cls.base, *cls.base.mroNum,)

  def _createMembers(cls, ) -> None:
    type.__setattr__(cls, '__allow_instantiation__', True)
    registry = []
    for key, kee in cls.space.__enumeration_members__.items():
      try:
        member = getattr(cls.base, key, )
      except AttributeError:
        member = cls(kee, )
      setattr(cls, key, member)
      registry.append(member)
    cls.__registered_members__ = (*registry,)
    type.__setattr__(cls, '__allow_instantiation__', False)

  @members.GET
  def _getMembers(cls, **kwargs) -> tuple[Any, ...]:
    """Returns the registered enumeration members of 'keeNum'."""
    if cls.__registered_members__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls.__registered_members__ = ()
      return cls._getMembers(_recursion=True, )
    return cls.__registered_members__

  @valueType.GET
  def _getValueType(cls, ) -> type:
    """Returns the value type of the enumeration."""
    type_ = None
    for member in cls.members:
      if isinstance(type_, type):
        if isinstance(member.value, type_):
          continue
        raise TypeException('value', member.value, type_)
      else:
        type_ = type(member.value)
    if type_ is None:
      infoSpec = """KeeNum class '%s' has no members, so no 'valueType' 
      can be inferred. """
      info = infoSpec % (cls.__name__,)
      raise TypeError(textFmt(info))
    return type_

  def _createNamedMembers(cls) -> None:
    """
    Creator function for the '__named_members__' cache.
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
      return cls._getNamedMembers(_recursion=True, )
    return cls.__named_members__

  def _createValuedMembers(cls) -> None:
    """
    Creator function for the '__valued_members__' cache.
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
      return cls._getValuedMembers(_recursion=True, )
    return cls.__valued_members__

  def _validateClassResolve(cls) -> None:
    """
    Detects '__class_resolve__' anywhere in the class hierarchy and
    validates it. Sets 'cls.__custom_resolve__' to True when a
    callable hook is found, False otherwise.

    Raises
    ------
    TypeException
      If '__class_resolve__' is defined but not callable.
    """
    classResolve = getattr(cls, '__class_resolve__', None)
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
    """Prepares the namespace for the class."""
    return KSpace(mcls, name, bases, **kw)

  def __call__(cls: KeeMeta, *args: Any, **kwargs: Any) -> T:
    """
    Resolves a member, or instantiates one during class creation.
    """
    if cls.__allow_instantiation__:
      return super().__call__(*args, **kwargs)
    if not args:
      raise TypeException('identifier', None, object)
    return cls._resolveMember(args[0])

  def __getitem__(cls, identifier: Any) -> Any:
    """Gets a member of the enumeration by identifier."""
    if isinstance(identifier, int):
      if identifier is not True and identifier is not False:
        try:
          member = cls.members[identifier]
        except IndexError:
          pass
        else:
          return member
    return cls._resolveMember(identifier)

  def __getattr__(cls, name: str) -> Any:
    """Gets a member of the enumeration by name."""
    mcls = type(cls)
    bases: list[KeeMeta] = [cls, ]
    if cls.__base_class__ is not None:
      bases.append(cls.__base_class__)
    for num in bases:
      value = mcls._resolveFromName(num, name)
      if value is NotImplemented:
        continue
      break
    else:
      return type.__getattribute__(cls, name)
    return value

  def __iter__(cls) -> Iterator[Any]:
    """Iterates over the members of the enumeration."""
    yield from cls.members

  def __len__(cls) -> int:
    """Returns the number of members in the enumeration."""
    return len(cls.members)

  def __contains__(cls, identifier: Any) -> bool:
    """Checks if the enumeration contains a matching member."""
    if not cls:
      return False
    if isinstance(identifier, cls):
      return True
    return False

  def __instancecheck__(cls, instance: Any) -> bool:
    """Checks if 'instance' is a member of the enumeration."""
    for member in cls:
      if member == instance:
        return True
    if issubclass(type(instance), cls):
      return True
    return False

  def __subclasscheck__(cls, subclass: type) -> bool:
    """Checks if 'subclass' is a subclass of the enumeration."""
    _ = issubclass(subclass, object)
    for item in subclass.__mro__:
      if item is cls:
        return True
    return False

  def __str__(cls) -> str:
    """Returns a string representation of the enumeration."""
    infoSpec = """<KeeNum '%s': %d members>"""
    return infoSpec % (cls.__name__, len(cls))

  __repr__ = __str__

  def __bool__(cls, ) -> bool:
    """KeeNum classes are always truthy."""
    return True if cls.members else False

  @classmethod
  def __init_subclass__(mcls, **kwargs) -> None:
    setattr(mcls, '__kee_num__', None)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __new__(mcls, name: str, bases: Bases, space: KSpace, **kw) -> T:
    """Creates the 'KeeMeta' class."""
    if '_root' in kw:
      del kw['_root']
    # noinspection PyTypeChecker
    return super().__new__(mcls, name, bases, space, **kw)

  def __init__(cls, name: str, *__, **_) -> None:
    cls.__class_name__ = name
    cls._createSpace()
    cls._createBase()
    cls._createMembers()
    cls._createNamedMembers()
    cls._createValuedMembers()
    cls._validateClassResolve()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _resolveFromName(cls, identifier: str) -> Any:
    """
    This method resolves a member by name (case-insensitive).

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

  def _resolveFromValue(cls, identifier: Any) -> Any:
    """
    Returns the first member whose 'value' equals 'identifier' or returns
    'NotImplemented'.

    Parameters
    ----------
    identifier : Any
      The value identifier to resolve.

    Returns
    -------
    KeeNum
      The resolved member, or 'NotImplemented' if resolution fails.
    """
    if cls.valueType is int:
      if identifier is True or identifier is False:
        return NotImplemented
    if '__unhashable__' in cls.valuedMembers:
      for member in cls:
        if member.value == identifier:
          return member
      return NotImplemented
    try:
      member = cls.valuedMembers[identifier]
    except KeyError:
      return NotImplemented
    else:
      return member

  def _resolveMember(cls, identifier: Any) -> Any:
    """
    Top-level dispatch for resolving a member from an identifier.

    Order
    -----
    1. If 'identifier' is already a member, return it.
    2. If 'identifier' is a string: (case-insensitive) name resolution.
    3. If the class has a custom resolver, use it.
    4. If 'identifier' is of the 'valueType', resolve by value.
    5. If all else fails, raise 'KeeResolveError'.

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
    T
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
    if isinstance(identifier, cls.valueType):
      resolved = cls._resolveFromValue(identifier)
      if resolved is not NotImplemented:
        return resolved
    raise KeeResolveError(cls, identifier)

  def fromValue(cls, value: Any) -> Any:
    """
    Resolves a member by value.

    Returns the lowest-indexed member whose 'value' equals the argument.
    """
    if not isinstance(value, cls.valueType):
      raise TypeException('value', value, cls.valueType)
    resolved = cls._resolveFromValue(value)
    if resolved is NotImplemented:
      raise KeeResolveError(cls, value)
    return resolved


# @formatter:off
if TYPE_CHECKING:  # pragma: no cover
  from . import _KeeBase
  class KeeNum(_KeeBase, metaclass = KeeMeta):  # noqa
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

__all__ = ('KeeMetaMeta', 'KeeMeta', 'KeeNum',)
