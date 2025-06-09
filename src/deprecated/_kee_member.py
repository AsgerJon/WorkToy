"""
_KeeMember encapsulates future enumeration member objects. The 'auto'
function instantiates this class during the class body execution. The
control flow collects these objects during compilation of the final
namespace object. For this reason, _KeeMember is private to the
'worktoy.keenum' module. Instances of _KeeMember are discarded during the
class creation process.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..attr import Field
from ..mcls import AbstractNamespace, BaseObject
from ..parse import maybe
from ..static import AbstractObject, overload
from ..static.zeroton import THIS
from ..waitaminute import MissingVariable, TypeException, VariableNotNone, \
  IllegalInstantiation

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, TypeAlias, Any


class _KeeMember(BaseObject):
  """
  _KeeMember encapsulates future enumeration member objects. The 'auto'
  function instantiates this class during the class body execution. The
  control flow collects these objects during compilation of the final
  namespace object. For this reason, _KeeMember is private to the
  'worktoy.keenum' module. Instances of _KeeMember are discarded during the
  class creation process.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __member_name__ = None  # Future name of the enumeration member
  __member_value__ = None  # Future value of the enumeration member

  #  Public Variables
  name = Field()
  value = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @name.GET
  def _getName(self) -> str:
    """Get the name of the enumeration member."""
    if self.__member_name__ is None:
      raise MissingVariable('__member_name__', str)
    if isinstance(self.__member_name__, str):
      return self.__member_name__
    raise TypeException('__member_name__', self.__member_name__, str)

  @value.GET
  def _getValue(self) -> Any:
    """Get the value of the enumeration member."""
    if self.__member_value__ is None:
      return self.__member_name__
    return self.__member_value__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @name.SET
  def _setName(self, name: str) -> None:
    """Set the name of the enumeration member."""
    if self.__member_name__ is not None:
      raise VariableNotNone('__member_name__', )
    if not isinstance(name, str):
      raise TypeException('__member_name__', name, str)
    self.__member_name__ = name

  @value.SET
  def _setValue(self, value: Any) -> None:
    """Set the value of the enumeration member."""
    if self.__member_value__ is not None:
      raise VariableNotNone('__member_value__', )
    self.__member_value__ = value

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    """
    The control flow instantiates and initializes the members
    automatically. Do not reimplement or change this function. Developers
    of 'worktoy' considers this function guaranteed to remain unchanged.
    Changing it causes undefined behavior. For this reason, future
    versions are planned to specifically raise RuntimeError if this
    function is reimplemented or changed.

    As of development version 0.99.85, this function could be
    reimplemented by setting the '_root' keyword argument to True,
    but a much better method of preventing instantiation is in the works.
    This new prevention scheme will be backwards compatible, ensuring that
    libraries depending on 'worktoy.keenum' can safely upgrade, provided
    they do not reimplement this function!
    """
    if not kwargs.get('_root', False):
      raise IllegalInstantiation(type(self))
