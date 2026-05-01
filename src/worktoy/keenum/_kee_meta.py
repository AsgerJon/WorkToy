"""
KeeMeta provides the metaclass for the 'worktoy.num' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from collections.abc import Callable

from ..core import Object
from ..desc import Field
from ..mcls import BaseMeta
from ..utilities import textFmt
from ..waitaminute import TypeException
from ..waitaminute.keenum import KeeResolveError
from . import KeeSpace as KSpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeAlias, Iterator, Optional
  from typing import List, TypeVar

  from . import KeeNum

  Bases: TypeAlias = tuple[type, ...]
  T = TypeVar('T', bound='KeeNum')


class KeeMeta(BaseMeta):
  """
  KeeMeta provides the metaclass for the 'worktoy.num' module.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Annotations
  __class_resolve__: Callable[[Any], Any]

  #  Private Variables
  __allow_instantiation__: bool = False
  __custom_resolve__: Optional[bool] = None
  __num_members__: Optional[List[KeeNum]] = None
  __named_members__: Optional[dict[str, Any]] = None

  #  Virtual Variables
  base: Field[type] = Field()
  mroNum: Field[List[type]] = Field()
  members: Field[List[KeeNum]] = Field()
  valueType: Field[type] = Field()
  namedMembers: Field[dict[str, Any]] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @base.GET
  def _getBase(cls, ) -> type:
    """Returns the nearest non-Object base of 'keeNum'."""
    for b in cls.__bases__:
      if b is not Object:
        return b
    return cls

  @mroNum.GET
  def _getMroNum(cls, ) -> List[type]:
    """Returns the MRO of 'keeNum' filtered to KeeNum classes."""
    mcls = type(cls)
    baseMro = [b for b in cls.__mro__ if isinstance(b, mcls)]
    return [b for b in baseMro if b is not cls]

  @members.GET
  def _getMembers(cls, ) -> List[KeeNum]:
    """Returns the registered enumeration members of 'keeNum'."""
    return [*cls.__num_members__]

  @valueType.GET
  def _getValueType(cls, ) -> type:
    """Returns the value type of the enumeration."""
    type_ = None
    for member in cls.members:
      if type_ is None:
        type_ = type(member.value)
        continue
      if TYPE_CHECKING:  # pragma: no cover
        assert isinstance(type_, type)
      if isinstance(member.value, type_):
        continue
      raise TypeException('value', member.value, type_)
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

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
    bases = (*[b for b in bases if b.__name__ != '_InitSub'],)
    return KSpace(mcls, name, bases, **kw)

  def __call__(cls: type[T], *args: Any, **kwargs: Any) -> T:
    """
    Resolves a member, or instantiates one during class creation.
    """
    if cls.__allow_instantiation__:
      return super().__call__(*args, **kwargs)
    if not args:
      raise TypeException('identifier', None, object)
    return cls._resolveMember(args[0])

  def __getitem__(cls: type[T], identifier: Any) -> T:
    """Gets a member of the enumeration by identifier."""
    return cls._resolveMember(identifier)

  def __getattr__(cls: type[T], name: str) -> T:
    """Gets a member of the enumeration by name."""
    value = cls._resolveByName(name)
    if value is NotImplemented:
      return type.__getattribute__(cls, name)
    return value

  def __iter__(cls: type[T]) -> Iterator[T]:
    """Iterates over the members of the enumeration."""
    if TYPE_CHECKING:  # pragma: no cover
      assert cls.__num_members__ is not None
    yield from cls.__num_members__

  def __len__(cls) -> int:
    """Returns the number of members in the enumeration."""
    return sum(1 for _ in cls)

  def __contains__(cls, identifier: Any) -> bool:
    """Checks if the enumeration contains a matching member."""
    if not cls:
      return False
    try:
      _ = cls._resolveMember(identifier)
    except KeeResolveError:
      return False
    return True

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
    if TYPE_CHECKING:  # pragma: no cover
      assert isinstance(cls.__num_members__, list)
    return infoSpec % (cls.__name__, len(cls.__num_members__))

  __repr__ = __str__

  def __bool__(cls, ) -> bool:
    """KeeNum classes are always truthy."""
    return True if cls.members else False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(cls, name: str, bases: Bases, space: KSpace, **_) -> None:
    cls.__num_members__ = []
    cls.__class_name__ = name
    if [b for b in bases if b is not Object]:
      cls.__allow_instantiation__ = True
      cls._installCustomResolve()
      enumMembers = space.__enumeration_members__
      for i, (key, kee) in enumerate(enumMembers.items()):
        for base in bases:
          try:
            self = getattr(base, key, )
          except AttributeError:
            continue
          else:
            break
        else:
          self = cls(kee, )
        setattr(cls, key, self)
        if TYPE_CHECKING:  # pragma: no cover
          assert isinstance(cls.__num_members__, list)
        cls.__num_members__.append(self)
      cls.__allow_instantiation__ = False
      cls._createNamedMembers()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _installCustomResolve(cls) -> None:
    """
    Detects '__class_resolve__' on the class and validates it.

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
      raise TypeException(
        '__class_resolve__', classResolve, Callable
      )
    cls.__custom_resolve__ = True

  def _resolveMember(cls: type[T], identifier: Any) -> T:
    """
    Top-level dispatch for resolving a member from an identifier.

    Order
    -----
    1. If 'identifier' is already a member of 'keeNum', return it.
    2. If 'identifier' is True or False, route to the bool guard.
    3. If 'identifier' is a 'str', route to the str chain.
    4. If 'identifier' is an 'int', route to the int chain.
    5. Otherwise, route to the generic 'other' chain.

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
      resolved = cls._resolveStrChain(identifier)
      if resolved is NotImplemented:
        raise KeeResolveError(cls, identifier)
    elif identifier is True or identifier is False:
      resolved = cls._resolveBoolChain(identifier)
      if resolved is NotImplemented:
        raise KeeResolveError(cls, identifier)
    elif isinstance(identifier, int):
      resolved = cls._resolveIntChain(identifier)
      if resolved is NotImplemented:
        raise KeeResolveError(cls, identifier)
    elif isinstance(identifier, cls.valueType):
      resolved = cls._resolveByValue(identifier)
      if resolved is NotImplemented:
        raise KeeResolveError(cls, identifier)
    else:
      if cls.__custom_resolve__:
        resolved = cls.__class_resolve__(identifier)
        if resolved is not NotImplemented:
          return resolved
      raise KeeResolveError(cls, identifier)
    return resolved

  def _resolveStrChain(cls, identifier: str) -> Any:
    """
    This method attempts to resolve a 'str' identifier in the following
    order of priority:
    1. By name (case-insensitive)
    2. By custom resolver ('__class_resolve__')
    3. By value (only if 'valueType' is 'str')

    Parameters
    ----------
    identifier : str
      The string identifier to resolve.

    Returns
    -------
    Any
      The resolved member, or 'NotImplemented' if resolution fails.
    """
    resolvers: tuple[Callable[[Any], Any], ...] = (
      cls._resolveByName,
      cls._resolveCustom,
      cls._resolveByValue,
    )
    for resolver in resolvers:
      result = resolver(identifier)
      if result is not NotImplemented:
        return result
    return NotImplemented

  def _resolveBoolChain(cls, identifier: bool) -> Any:
    """
    This method attempts to resolve a 'bool' identifier in the following
    order of priority:
    1. By custom resolver ('__class_resolve__')
    2. By value (only if 'valueType' is 'bool')

    Parameters
    ----------
    identifier : bool
      The boolean identifier to resolve.

    Returns
    -------
    Any
      The resolved member, or 'NotImplemented' if resolution fails.
    """
    resolved = cls._resolveCustom(identifier)
    if resolved is not NotImplemented:
      return resolved
    for member in cls:
      if member.value ^ identifier:
        continue
      return member
    return NotImplemented

  def _resolveIntChain(cls, identifier: int) -> Any:
    """
    This method attempts to resolve an 'int' identifier in the following
    order of priority:
    1. By custom resolver ('__class_resolve__')
    2. By index (if 'identifier' is a valid index)
    3. By value (only if 'valueType' is 'int')

    Please note, that an enumeration using 'valueType' of 'int' are
    strongly encouraged to provide a solid custom resolver implementation.
    Otherwise, if a member has a value lower than the number of elements,
    it the element at that index is returned rather than the element
    having the value equal to the identifier. The member resolution
    machinery here provides no protection against this situation.

    Parameters
    ----------
    identifier : int
      The integer identifier to resolve.

    Returns
    -------
    Any
      The resolved member, or 'NotImplemented' if resolution fails.
    """
    resolvers = []
    if cls.__custom_resolve__:
      resolvers.append(cls._resolveCustom)
    resolvers.append(cls._resolveByIndex)
    if cls.valueType is int:
      resolvers.append(cls._resolveByValue)
    for resolver in resolvers:
      result = resolver(identifier)
      if result is not NotImplemented:
        return result
    return NotImplemented

  def _resolveByIndex(cls, identifier: int) -> Any:
    """
    Resolves an 'int' identifier by index, if valid.

    Parameters
    ----------
    identifier : int
      The integer identifier to resolve.

    Returns
    -------
    Any
      The resolved member, or 'NotImplemented' if 'identifier' is not a valid
      index.
    """
    if identifier < 0:
      return cls._resolveByIndex(len(cls) + identifier)
    if identifier < len(cls):
      return cls.__num_members__[identifier]
    return NotImplemented

  def _resolveByName(cls, identifier: str) -> Any:
    """
    Resolves a 'str' identifier by name (case-insensitive).

    Parameters
    ----------
    identifier : str
      The string identifier to resolve.

    Returns
    -------
    Any
      The resolved member or 'NotImplemented' if no member has a matching
      name.
    """
    key = identifier.lower()
    try:
      value = cls.namedMembers[key]
    except KeyError:
      return NotImplemented
    else:
      return value

  def _resolveCustom(cls, identifier: Any) -> Any:
    """
    Invokes '__class_resolve__' if defined.

    Returns 'NotImplemented' if no resolver is registered or if the
    resolver declines, either by returning 'NotImplemented' or by
    raising 'KeeResolveError'. Any other exception propagates.

    Parameters
    ----------
    identifier : Any
      The identifier passed to the custom resolver.

    Returns
    -------
    Any
      The resolver result, or 'NotImplemented' on decline.
    """
    if cls.__custom_resolve__:
      return cls.__class_resolve__(identifier)
    return NotImplemented

  def _resolveByValue(cls, identifier: Any) -> Any:
    """
    Resolves an identifier by value, if 'valueType' matches.

    Parameters
    ----------
    identifier : Any
      The identifier to resolve.

    Returns
    -------
    Any
      The resolved member, or 'NotImplemented' if 'valueType' does not match
      or if no member has a matching value.
    """
    for member in cls:
      if member.value == identifier:
        return member
    return NotImplemented

  def fromValue(cls: type[T], value: Any) -> T:
    """
    Resolves a member by value.

    Returns the lowest-indexed member whose 'value' equals the
    argument.
    """
    if not isinstance(value, cls.valueType):
      raise TypeException('value', value, cls.valueType)
    resolved = cls._resolveByValue(value)
    if resolved is NotImplemented:
      raise KeeResolveError(cls, value)
    return resolved
