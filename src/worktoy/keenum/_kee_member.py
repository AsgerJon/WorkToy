"""
KeeMember encapsulates a member of an enumeration.

Defining properties: (independent properties)
  - name: The name of the member. This is the name by which the member
  appears in the class body of the enumeration. It is the name passed to
  the '__set_name__' method. These must be unique with enumerations and
  must be uppercase. The case requirement is more than convention,
  it is enforced. When an enumeration class body contains key, value pairs
  with the key not in uppercase, it is understood to mean that the value
  does not represent a member of the enumeration.
  - value: The value of the member. Uniquely, this value is not required
  to be unique across members of the same enumeration.
  - index: The index of the member. This index specifies how many members
  are before this member in the enumeration.

KeeMember may be used directly or may be further subclassed. The KeeNum
classes are created by the KeeMeta class which define the class behaviour
post creation, and KeeMember define how members are included in the
enumeration.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..desc import Field, AttriBox
from ..utilities import textFmt
from ..waitaminute import VariableNotNone, MissingVariable, TypeException
from ..waitaminute.keenum import KeeCaseException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type, TypeAlias

  KEENUM: TypeAlias = Type[object]


class Kee(AttriBox):
  """KeeMember encapsulates a member of an enumeration. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __context_instance__ = None
  __context_owner__ = None

  #  Fallback Variables

  #  Private Variables
  __field_value__ = None
  __num_index__ = None
  __num_name__ = None

  #  Public Variables
  name = Field()
  index = Field()
  value = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @value.GET
  def getValue(self, **kwargs) -> Any:
    """
    Uses the 'AttriBox' lazy instantiation mechanism.
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

  def __int__(self, ) -> int:
    return self.index

  def __str__(self) -> str:
    """Return the string representation of the member."""
    infoSpec = """<%s member: %s>"""
    try:
      keeName = self.name
    except AttributeError:
      keeName = '- N/A -'
    clsName = type(self).__name__
    info = infoSpec % (clsName, keeName)
    return textFmt(info)

  __repr__ = __str__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Parent Methods   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
