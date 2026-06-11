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
  1: Single 'str' object received
  1a: The string matches the 'name' of a member of the enumeration.
  1b: The string matches the 'value' of a member of the enumeration.
  2: Single 'int' object received
  2a: The integer matches the 'index' of a member of the enumeration.
  2b: The integer matches the 'value' of a member of the enumeration.
  3: Single argument received of the 'valueType' type of the enumeration.
  3a: The argument matches the 'value' of a member of the enumeration.
  4: Any number of arguments received
  4a: If the enumeration class is a 'KeeFlags' class instead. Then for each
  argument, it attempts to resolve it to a flag member. If all succeed,
  it returns the member having those flags high.

  The above process applies to both instantiation and setting. Please note
  that 'KeeBox' will never attempt to instantiate the 'valueType' of the
  enumeration.

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
    pvtName = self.getPrivateName()
    try:
      return getattr(instance, pvtName)
    except AttributeError as attributeError:
      if kwargs.get('_recursion', False):
        raise RecursionError from attributeError
      try:
        fieldObject = self._resolve()
      except Exception as exception:
        raise exception from attributeError
      setattr(instance, pvtName, fieldObject)
      return self.__instance_get__(instance, owner, _recursion=True)

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    pvtName = self.getPrivateName()
    if isinstance(value, self.fieldType):
      return setattr(instance, pvtName, value)
    if kwargs.get('_recursion', False):
      raise RecursionError
    return self.__instance_set__(
      instance, self._resolve(value, ), _recursion=True
    )

  def _resolve(self, *args, **kwargs) -> Any:
    fieldNum = self.fieldType
    if isinstance(fieldNum, KeeMeta):
      return self._resolveNum(*args, )
    elif isinstance(fieldNum, KeeFlagsMeta):
      return self._resolveFlags(*args, )
    else:
      raise KeeBoxException(self, self.getPosArgs())

  def _resolveNum(self, *args, ) -> Any:
    args = args or self.getPosArgs()
    kwargs = self.getKeyArgs()
    fieldNum = self.fieldType
    valueType = fieldNum.valueType
    if len(args) == 1:
      if isinstance(args[0], str):
        for member in fieldNum:
          if args[0] == member.name:
            return member
        for member in fieldNum:  # Case-insensitive match
          if str.lower(args[0]) == str.lower(str(member.name)):
            return member
      if isinstance(args[0], int):
        if args[0] < len(fieldNum):
          return fieldNum[args[0]]
        for member in fieldNum:
          if args[0] == member.value:
            return member
      elif isinstance(args[0], valueType):
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
    """
    args = args or self.getPosArgs()
    if len(args) == 1 and isinstance(args[0], (tuple, list, set, frozenset)):
      args = (*args[0],)
    highs = []
    for arg in args:
      highs.append(self._resolveNum(arg, ))
    names = frozenset((*(h.name for h in highs),), )
    return self.fieldType.memberDict[names]

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
