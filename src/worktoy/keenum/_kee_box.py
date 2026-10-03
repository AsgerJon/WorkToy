"""
KeeBox is an 'AttriBox' that resolves its arguments to a member of an
enumeration field type.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import KeeMeta, KeeFlagsMeta
from ..desc import AttriBox
from ..waitaminute import TypeException
from ..waitaminute.keenum import KeeBoxException, \
  KeeBoxValueError, KeeBoxTypeError

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class KeeBox(AttriBox):
  """
  KeeBox subclasses AttriBox and provides special support for the
  enumerations. This solves a general problem with 'AttriBox' objects using
  enumerations as their field types. When doing so, the positional arguments
  in the parentheses, *must* be a member of the enumeration. First of all,
  this requires duplication of the enumeration class. Secondly, it fails to
  provide the intended flexibility of passing constructor arguments for
  deferred instantiation. Because enumerations instantiate *during* class
  creation, there is no deferred instantiation. Finally, when an descriptor
  is retrieved from an instance, it is mostly for the purpose of retrieving
  the value of the descriptor.

  The KeeBox makes the following attempts at resolving arguments to a member
  of the enumeration:
  0: Single member of the enumeration received, returned as it is.
  1: Single 'str' object received
  1a: The string matches the 'name' of a member of the enumeration.
  1b: The string matches the 'value' of a member of the enumeration.
  2: Single 'int' object received
  2a: The integer is the 'index' of a member of the enumeration. No member
  has a negative index, so a negative integer is never read as a position
  counted from the end.
  2b: The integer matches the 'value' of a member of the enumeration,
  provided it is an instance of the 'valueType' of the enumeration.
  3: Single argument received of the 'valueType' type of the enumeration.
  3a: The argument matches the 'value' of a member of the enumeration.
  4: Any number of arguments received
  4a: For a 'KeeNum' class, the arguments build an instance of its
  'valueType', which must equal the 'value' of a member. This is how '-1'
  finds a member whose value is '-1.0'.
  4b: For a 'KeeFlags' class, each argument is resolved the way
  subscripting the class resolves it, so a member, a name in any case and
  order, or an index all work. The result is the member having every flag
  high that any of those members has.

  The above process applies to both instantiation and setting.

  Examples:

    #  KeeNum classes:
    class KeyboardNum(KeeNum):
      A = Kee[str]('key A')
      B = Kee[str]('key B')
      ...

    class KeyModFlags(KeeFlags):
      SHIFT = KeeFlag(0)
      CTRL = KeeFlag(1)
      ALT = KeeFlag(2)
      META = KeeFlag(3)

    #  Illustrative classes using the above KeeNum classes:
    class SelectAll:
      key = KeeBox[KeyboardNum]('A')
      mod = KeeBox[KeyModFlags]('ctrl')

    class Settings:  # PyCharm: CTRL+SHIFT+S
      key = KeeBox[KeyboardNum]('S')
      mod = KeeBox[KeyModFlags]('ctrl', 'shift')
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> Any:
    pvtName = self._getStorageName()
    try:
      #  Not 'getattr', whose miss an owner's '__getattr__' could answer.
      return object.__getattribute__(instance, pvtName)
    except AttributeError as attributeError:
      #  A read made before deleting only reports; it must not build.
      if kwargs.get('_deleting', False):
        raise attributeError
      if kwargs.get('_recursion', False):
        raise RecursionError from attributeError
      try:
        fieldObject = self._resolve()
      except Exception as exception:
        raise exception from attributeError
      #  Not 'setattr', which an owner's '__setattr__' could refuse.
      object.__setattr__(instance, pvtName, fieldObject)
      return self.__instance_get__(instance, owner, _recursion=True)

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> Any:
    """
    The '__instance_set__' method stores the member 'value' resolves to,
    and returns it, so the 'onSet' callbacks receive the member.
    """
    pvtName = self._getStorageName()
    if self._isMember(value):
      object.__setattr__(instance, pvtName, value)
      return value
    if kwargs.get('_recursion', False):
      raise RecursionError
    return self.__instance_set__(
      instance, self._resolve(value, ), _recursion=True
    )

  def _isMember(self, value: Any) -> bool:
    """
    The '_isMember' method reports whether 'value' is a member of the
    field enumeration, a member of an enumeration derived from it
    included.
    """
    return True if isinstance(value, self.fieldType) else False

  def _resolve(self, *args, **kwargs) -> Any:
    fieldNum = self.fieldType
    if isinstance(fieldNum, KeeMeta):
      return self._resolveNum(*args, )
    elif isinstance(fieldNum, KeeFlagsMeta):
      return self._resolveFlags(*args, )
    else:
      raise KeeBoxException(self, self.getPosArgs())

  def _resolveNum(self, *args, ) -> Any:
    """
    The '_resolveNum' method resolves to a member of a 'KeeNum' field
    type, falling back to the captured constructor arguments when called
    without any. The captured keyword arguments belong to those, and so
    build the default alone: an assigned value is resolved from the value
    only.
    """
    if args:
      kwargs = dict()
    else:
      args, kwargs = self.getPosArgs(), self.getKeyArgs()
    fieldNum = self.fieldType
    valueType = fieldNum.valueType
    if len(args) == 1:
      if self._isMember(args[0]):
        return args[0]
      if isinstance(args[0], str):
        for member in fieldNum:
          if args[0] == member.name:
            return member
        for member in fieldNum:  # Case-insensitive match
          if str.lower(args[0]) == str.lower(str(member.name)):
            return member
      if isinstance(args[0], int) and 0 <= args[0] < len(fieldNum):
        return fieldNum[args[0]]
      if isinstance(args[0], valueType):
        for member in fieldNum:
          if args[0] == member.value:
            return member
    try:
      tempObject = valueType(*args, **kwargs)
    except Exception as exception:
      raise KeeBoxTypeError(self, *args) from exception
    else:
      for member in fieldNum:
        if tempObject == member.value:
          return member
      else:
        raise KeeBoxValueError(self, fieldNum, tempObject)

  def _resolveFlags(self, *args, ) -> Any:
    """
    The '_resolveFlags' method resolves to a flags member, falling back
    to the captured constructor arguments when called without any. A
    lone container argument counts as several flag identifiers, since
    the descriptor protocol delivers an assigned tuple as one object.
    Each identifier is resolved by subscripting the flags class, so the
    box accepts and refuses exactly what the class itself does, and the
    result is the member having every flag high that any of the
    resolved members has.
    """
    args = args or self.getPosArgs()
    if len(args) == 1 and isinstance(args[0], (tuple, list, set, frozenset)):
      args = (*args[0],)
    fieldNum = self.fieldType
    names = set()
    for arg in args:
      names.update(fieldNum[arg].names)
    return fieldNum.memberDict[frozenset(names)]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_getitem__(cls, fieldType: Any) -> Self:
    """
    The '__class_getitem__' method restricts the 'KeeBox[...]' subscript
    to a class derived from 'KeeMeta' or 'KeeFlagsMeta', raising
    'TypeException' otherwise, before delegating to
    'AttriBox.__class_getitem__'. The restriction simplifies the
    implementation; plain 'AttriBox' performs no such check and accepts
    every 'type'.
    """
    if isinstance(fieldType, KeeMeta) or isinstance(fieldType, KeeFlagsMeta):
      return super().__class_getitem__(fieldType)
    raise TypeException('fieldType', fieldType, KeeMeta, KeeFlagsMeta)
