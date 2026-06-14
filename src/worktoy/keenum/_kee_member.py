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
from ..waitaminute.keenum import KeeCaseException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type, TypeAlias, Self

  KEENUM: TypeAlias = Type[object]

T = TypeVar('T')


class Kee(AttriBox[T]):
  """
  Kee is the descriptor that declares a member of a KeeNum enumeration.

  Each 'Kee' instance placed in the class body of a KeeNum subclass
  contributes one member, with the following defining properties:

    - name: The name of the member, taken from the class-body
      assignment via '__set_name__'. Names must be unique within an
      enumeration and must be uppercase. The uppercase rule is
      enforced: assigning a 'Kee' to a non-uppercase name (lowercase or
      mixed case) raises 'KeeCaseException' when the class is created. A
      non-'Kee' class-body entry is unaffected and stays an ordinary
      class attribute.
    - value: The value of the member. Values are not required to be
      unique across members of the same enumeration.
    - index: The position of the member, equal to the number of members
      declared before it.

  'Kee' may be used directly or further subclassed. KeeNum classes are
  created by the KeeMeta metaclass, which defines class-level behavior;
  'Kee' defines how individual members are admitted into the
  enumeration.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Annotations
  valueType: Field[Type[T]]
  kee: Field[Type[Self]]

  #  Private Variables
  __field_value__ = None
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
    """
    if self.__field_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      args = self.getPosArgs()
      keyArgs = self.getKeyArgs()
      self.__field_value__ = self._resolve(*args, **keyArgs)
      return self.getValue(_recursion=True)
    fieldType = self.getFieldType()
    if isinstance(self.__field_value__, fieldType):
      return self.__field_value__
    raise TypeException('__field_value__', self.__field_value__, fieldType)

  @name.GET
  def _getName(self) -> str:
    """Set by 'Object.__set_name__' when the enumeration is created."""
    if self.__num_name__ is None:
      raise MissingVariable(self, '__num_name__', str)
    if isinstance(self.__num_name__, str):
      return self.__num_name__
    raise TypeException('__num_name__', self.__num_name__, str)

  @index.GET
  def _getIndex(self) -> int:
    """Set by 'KeeSpace.addNum' when the enumeration is created."""
    if self.__num_index__ is None:
      raise MissingVariable(self, '__num_index__', int)
    if isinstance(self.__num_index__, int):
      return self.__num_index__
    raise TypeException('__num_index__', self.__num_index__, int)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  The 'KeeSpace' namespace class expects to be able to set 'name' and
  #  'index'  before the enumeration class is created. Subclasses that
  #  change this behaviour must also implement these changes  in the
  #  'KeeSpace' class.

  @name.SET
  def _setName(self, name: str) -> None:
    if not name.isupper():
      raise KeeCaseException(name)
    if self.__num_name__ is not None:
      raise VariableNotNone('name', self.__num_name__)
    self.__num_name__ = name

  @index.SET
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
    A 'Kee' declared inside a proper 'KeeNum' class body never receives
    the interpreter-driven call: 'KeeSpaceHook' claims it during class
    body execution, before the namespace stores it. The interpreter
    reaches this method only when a 'Kee' landed in the class body of a
    class not built by 'KeeMeta', so an owner of any other kind is
    rejected with 'TypeException'.
    """
    #  Local import: 'KeeMeta' loads after this file in the package.
    from . import KeeMeta
    if isinstance(owner, KeeMeta):
      return AttriBox.__set_name__(self, owner, name, **kwargs)
    raise TypeException('owner', owner, KeeMeta)

  def __int__(self, ) -> int:
    return self.index

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
