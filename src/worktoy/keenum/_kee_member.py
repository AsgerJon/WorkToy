"""
Kee is the descriptor that declares a member of a 'KeeNum' enumeration.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from ..desc import Field, AttriBox
from ..utilities import textFmt
from ..waitaminute import VariableNotNone, MissingVariable, TypeException
from ..waitaminute import DeprecatedPromise
from ..waitaminute.keenum import KeeCaseException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Self

T = TypeVar('T')

#  The description of the deprecation of the position of a 'Kee'.
_POSITION = """The position belongs to the enumeration, not to the
declaration of a member: 'Day[x]' gives the member at position 'x'."""


class Kee(AttriBox[T]):
  """
  Kee is the descriptor that declares a member of a KeeNum enumeration.

  Each 'Kee' instance placed in the class body of a KeeNum subclass
  contributes one member, with the following defining properties:

    - name: The name of the member, taken from the class-body
      assignment by 'KeeSpace.addNum'. Names must be unique within an
      enumeration and must be uppercase. The uppercase rule is
      enforced: assigning a 'Kee' to a non-uppercase name (lowercase or
      mixed case) raises 'KeeCaseException' when the class is created. A
      non-'Kee' class-body entry is unaffected and stays an ordinary
      class attribute.
    - value: The value of the member. Values are not required to be
      unique across members of the same enumeration.
    - index: Deprecated. The position of the member, equal to the number
      of members declared before it; reading or writing it, and
      'int(kee)', give a 'DeprecatedPromise', since the position belongs
      to the enumeration.

  'Kee' may be used directly or further subclassed. KeeNum classes are
  created by the KeeMeta metaclass, which defines class-level behavior;
  'Kee' defines how individual members are admitted into the
  enumeration.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_value__ = None
  __value_built__ = False
  __num_index__ = None
  __num_name__ = None

  #  Public Variables
  name: Field[str] = Field()
  index: Field[int] = Field()
  value: Field[T] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @value.GET
  def getValue(self, **kwargs) -> Any:
    """
    The 'getValue' getter realizes the member's value through the
    'AttriBox' lazy instantiation mechanism, building it from the captured
    constructor arguments on first access and type-checking it thereafter.
    A flag beside the value records that it was built, since the value
    itself may be 'None', as 'Kee[object](None)' declares. A 'Kee' of
    'str', or of a subclass of it, declared with empty parentheses takes
    its name as the value, 'RED = Kee[str]()' holding 'RED'; any other
    type builds its value from empty parentheses as its constructor
    does, so 'Kee[int]()' holds 0. A value
    written directly is honoured, built or not. The member reads the
    value once, as the enumeration is created, and keeps it, so a value
    written into the 'Kee' after that does not reach the member.
    """
    if self.__field_value__ is None and not self.__value_built__:
      if kwargs.get('_recursion', False):
        raise RecursionError
      args = self.getPosArgs()
      keyArgs = self.getKeyArgs()
      if not args and not keyArgs and issubclass(self.getFieldType(), str):
        #  This branch is reached by the following:
        #  - A 'Kee' of a text type declared with empty parentheses, as
        #    'RED = Kee[str]()', whose value is its name
        args = (self._getName(),)
      self.__field_value__ = self._resolve(*args, **keyArgs)
      self.__value_built__ = True
      return self.getValue(_recursion=True)  # pragma: no mutate
    fieldType = self.getFieldType()
    if isinstance(self.__field_value__, fieldType):
      return self.__field_value__
    raise TypeException('__field_value__', self.__field_value__, fieldType)

  @name.GET
  def _getName(self) -> str:
    """Set by 'KeeSpace.addNum' when the enumeration is created."""
    if self.__num_name__ is None:
      raise MissingVariable(self, '__num_name__', str)
    if isinstance(self.__num_name__, str):
      return self.__num_name__
    raise TypeException('__num_name__', self.__num_name__, str)

  @index.GET
  def _readIndex(self) -> int:
    """
    The public 'index' is deprecated: a read gives the position with a
    'DeprecatedPromise' at the line that read it. The library reads it
    through '_getIndex'.
    """
    DeprecatedPromise('worktoy.keenum.Kee.index', textFmt(_POSITION)).warn()
    return self._getIndex()

  def _getIndex(self) -> int:
    """Set by 'KeeMeta._createMembers' when the enumeration is created."""
    if self.__num_index__ is None:
      raise MissingVariable(self, '__num_index__', int)
    if isinstance(self.__num_index__, int):
      return self.__num_index__
    raise TypeException('__num_index__', self.__num_index__, int)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  'KeeSpace.addNum' sets 'name' as the class body runs, and
  #  'KeeMeta._createMembers' sets 'index' as the class is created, each
  #  once. A subclass changing either setter changes what those two
  #  expect.

  @name.SET
  def _setName(self, name: str) -> None:
    if not name.isupper():
      raise KeeCaseException(name)
    if self.__num_name__ is not None:
      raise VariableNotNone('name', self.__num_name__)
    self.__num_name__ = name

  @index.SET
  def _writeIndex(self, index: int) -> None:
    """
    The public 'index' is deprecated: a write sets the position with a
    'DeprecatedPromise' at the line that wrote it. The library writes it
    through '_setIndex'.
    """
    DeprecatedPromise('worktoy.keenum.Kee.index', textFmt(_POSITION)).warn()
    self._setIndex(index)

  def _setIndex(self, index: int) -> None:
    if not isinstance(index, int):
      raise TypeException('index', index, int)
    if self.__num_index__ is not None:
      raise VariableNotNone('index', self.__num_index__)
    self.__num_index__ = index

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    A 'Kee' in a 'KeeNum' body is claimed by 'KeeSpaceHook' before the
    namespace stores it, so the interpreter never calls this method for
    it; 'KeeMeta._createMembers' calls it instead, with the enumeration
    as owner, once the class exists, and the placement of a box runs: a
    'Kee' declared without parentheses, or placed on another enumeration
    already, is refused there. The interpreter reaches this method only
    for a 'Kee' in the body of a class not built by 'KeeMeta', which is
    refused with a 'TypeError' saying where a 'Kee' belongs.
    """
    #  Local import: 'KeeMeta' loads after this file in the package.
    from . import KeeMeta
    if isinstance(owner, KeeMeta):
      return AttriBox.__set_name__(self, owner, name, **kwargs)
    infoSpec = """A 'Kee' declares a member of an enumeration and belongs
    in the body of a 'KeeNum' subclass, but '%s' is bound to one at '%s'
    and '%s' is no enumeration."""
    info = infoSpec % (owner.__name__, name, owner.__name__)
    raise TypeError(textFmt(info))

  def __int__(self, ) -> int:
    """
    'int(kee)' gives the deprecated position, with a 'DeprecatedPromise'.
    """
    info = textFmt(_POSITION)
    DeprecatedPromise('worktoy.keenum.Kee.__int__', info).warn()
    return self._getIndex()

  def __reduce__(self) -> tuple:
    """
    A placed box pickles as a reference to its class and name, which for
    a 'Kee' would give the member, not the 'Kee'. A placed 'Kee' pickles
    as the 'kee' of its member instead, so it unpickles as the very
    object; a 'Kee' never placed pickles by its state, as a box does.
    """
    owner, name = self.__field_owner__, self.__field_name__
    if owner is None or name is None:
      return AttriBox.__reduce__(self)
    member = type.__getattribute__(owner, name)
    return getattr, (member, 'kee')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def clone(self) -> Self:
    """
    The 'clone' method copies this 'Kee' so a subclass can register the
    copy in its own namespace. The copy carries the field type, the
    captured constructor arguments and the name, while the index is left
    unset for the registering namespace to assign. Registering the
    original object instead would write the subclass index onto the
    member shared with the parent enumeration.
    """
    cls = type(self)
    cloned = cls[self.getFieldType()]
    cloned(*self.getPosArgs(), **self.getKeyArgs())
    cloned.__num_name__ = self.__num_name__
    return cloned

  def __str__(self) -> str:
    infoSpec = """<%s member: %s>"""
    try:
      keeName = self.name
    except AttributeError:
      keeName = '- N/A -'
    clsName = type(self).__name__
    info = infoSpec % (clsName, keeName)
    return textFmt(info)

  __repr__ = __str__
