"""
KeeBase provides the base for 'worktoy.keenum' enumerations.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, overload, TypeVar

from ..core import Object
from ..desc import Field
from ..utilities import textFmt
from ..waitaminute import MissingVariable
from ..waitaminute.desc import ReadOnlyError, ProtectedError
from ..waitaminute.keenum import KeeWriteOnceError
from . import Kee

T = TypeVar('T')

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Never, Self, Optional, TypeAlias

  from . import KeeNum

  MaybeInt: TypeAlias = Optional[int]
  MaybeStr: TypeAlias = Optional[str]
  MaybeKee: TypeAlias = Optional[Kee]
  MaybeBool: TypeAlias = Optional[bool]


class KeeBase(Object, ):
  """
  Base class for all enumerating classes in the KeeNum framework.

  Equality is identity: 'MyEnum.A == MyEnum.A' is True; comparison to
  a member of a different KeeNum subclass returns NotImplemented (and
  '==' therefore yields False).

  Hashability tracks the member's value. The hash is computed from
  the member's qualified name (so distinct members within a class get
  distinct hashes), but '__hash__' first calls 'hash(self.value)' as
  a gate:

    - If the value is hashable, the member is hashable and can be
      used as a dict key, in a set, etc.
    - If the value is unhashable (a list, dict, mutable instance,
      etc.), the member is *also* unhashable. Calling 'hash(member)'
      raises 'TypeError', and the member cannot be used as a dict
      key or set element. This is intentional: it keeps the
      member-side hash semantics consistent with the value-side
      hash semantics that user code might rely on.

  Members declared with unhashable values still work everywhere
  hashability is not required: iteration, attribute access, name and
  index resolution, equality, '__str__', and '__repr__' all behave
  normally. Only hash-keyed containers refuse them.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_value__: Optional[Any] = None
  __frozen_state__: MaybeBool = None
  __field_kee__: MaybeKee = None  # The 'Kee' object of this member.

  #  Public Variables
  index: Field[int] = Field()
  value: Field[Any] = Field()
  valueType: Field[type] = Field()
  kee: Field[Kee] = Field()

  #  Virtual Variables
  name: Field[str] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @kee.GET
  def _getKee(self) -> Kee:
    if self.__field_kee__ is None:
      raise MissingVariable(self, '__field_kee__', Kee)
    return self.__field_kee__

  @name.GET
  def _getName(self) -> str:
    return self.kee.name

  @index.GET
  def _getIndex(self) -> int:
    return self.kee.index

  @value.GET
  def _getValue(self) -> Any:
    return self.kee.getValue()

  @valueType.GET
  def _getValueType(self) -> type:
    return self.kee.getFieldType()

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
    object.__setattr__(self, '__frozen_state__', False)
    self.__field_kee__ = member
    object.__setattr__(self, '__frozen_state__', True)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __setattr__(self, name: str, value: Any) -> None:
    """
    A member is frozen after construction, so '__setattr__' raises
    'KeeWriteOnceError' once the freeze flag is set; assignments during
    construction pass through.
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

  def __set_name__(self, owner: type, name: str, **kw) -> None:
    """This reimplementation of '__set_name__' is necessary to prevent the
    '__setattr__' method above from raising when a class wants an
    enumeration defined in its namespace. """
    pass

  def __get__(self, instance: Any, owner: type, **kw) -> KeeNum:
    """Implementation of '__get__' is necessary for the same reason as
    '__set_name__'. """
    return self

  def __set__(self, instance: Any, value: Any, **kwargs) -> Never:
    """Ensures 'ReadOnlyError' is raised instead of 'KeeWriteOnceError'."""
    raise ReadOnlyError(instance, self, value)

  def __delete__(self, instance: Any, **kwargs) -> Never:
    """Ensures 'ProtectedError' is raised instead of 'KeeWriteOnceError'."""
    raise ProtectedError(instance, self, self)

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

  def __int__(self) -> int:
    return self.index

  __index__ = __int__

  def __hash__(self) -> int:
    """Hash by name, but only when 'value' is itself hashable. Members
    with unhashable values are themselves unhashable, so that any
    hashed lookup on the member side remains consistent with hashed
    lookup on the value side."""
    try:
      hash(self.value)
    except TypeError as typeError:
      infoSpec = """Enumeration member '%s' is unhashable because its
      value of type '%s' is unhashable!"""
      info = infoSpec % (self, type(self.value).__name__)
      raise TypeError(textFmt(info)) from typeError
    base = str.join('::', (type(self).__name__, self.name,))
    return int.from_bytes(base.encode(), 'big')

  def __eq__(self, other: Any) -> bool:
    if type(self) is not type(other):
      return NotImplemented
    return True if self is other else False

  def __str__(self) -> str:
    infoSpec = """%s.%s"""
    clsName = type(self).__name__
    info = infoSpec % (clsName, self.name)
    return info

  __repr__ = __str__

  if TYPE_CHECKING:  # pragma: no cover
    # @formatter:off
    def __call__(self, identifier: Any) -> Self: ...
    # @formatter:on
