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

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Self


class KeeBox(AttriBox):
  """
  A field typed with an enumeration is declared with the member it
  starts as, and a project wants to write that member the way it
  thinks of it: by name, by the arguments of the value it carries, by
  the value, or by its position. An 'AttriBox' over the enumeration
  hands the parentheses to the class, which takes one identifier and
  no more, so 'AttriBox[CurrencyNum]('JPY', decimals=0)' is refused
  although every argument names the member. The parentheses of a field
  over an enumeration must take what identifies a member, the
  arguments of its value included, while assignment stays what it is on
  every box: a member is stored, anything else is converted as the
  enumeration converts it, or refused.

    class KeyBind(BaseObject):
      key = KeeBox[KeyboardNum]('A')
      mod = KeeBox[KeyModFlags]('ctrl', 'shift')

  Implementation
  --------------

  'KeeBox' is an 'AttriBox' whose subscript must be an enumeration of
  either kind, 'KeeMeta' or 'KeeFlagsMeta', and whose '_resolve' builds
  the value of the parentheses by its own steps instead of calling the
  class with them. For a 'KeeNum' class, a lone member is taken as it
  is; a lone 'str' is a name, in any case; a lone argument the
  enumeration's '__class_resolve__' answers for is that answer, the hook
  being asked where a call of the class asks it, after the name and
  before the position; a lone 'int' other than a 'bool' is a position
  when it is in range; a lone 'bool' is no value of an 'int' enumeration
  and is refused with 'KeeBoxValueError', as the class refuses it; a
  lone instance of the value type is looked up among the member values
  as a call of the class looks it up, and refused with
  'KeeBoxValueError' when no member carries it; any other arguments,
  keywords included, build an instance of the value type, refused with
  'KeeBoxTypeError' when the constructor raises, and that instance is
  looked up the same way. For a 'KeeFlags' class every
  argument, or every element of a lone tuple, list or set, is resolved
  as subscripting the class resolves it, and the member having every
  flag high that any of them has is the value. A member a 'KeeBox'
  hands out is never tagged, since the box built nothing. Assignment,
  storage and deletion are those of 'AttriBox': an assigned member is
  stored, any other value goes through 'typeCast' and the enumeration's
  '__cast_as__', so a name, a value or a tuple of flag names is stored
  as the member it resolves to and a value the class cannot resolve is
  refused with 'TypeException' naming the field.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _isMember(self, value: Any) -> bool:
    """
    The '_isMember' method reports whether 'value' is a member of the
    field enumeration, a member of a subclass of it included.
    """
    return True if isinstance(value, self.getFieldType()) else False

  def _resolve(self, *args, **kwargs) -> Any:
    """
    The box builds the value of its parentheses from the arguments of
    the declaration, placeholders replaced, as every box does; here the
    build is a resolution by the steps the class docstring lists. The
    field type is read through 'getFieldType', past the 'fieldType'
    descriptor, since every instance pays for the build at its first
    read.
    """
    fieldNum = self.getFieldType()
    if isinstance(fieldNum, KeeMeta):
      return self._resolveNum(*args, **kwargs)
    if isinstance(fieldNum, KeeFlagsMeta):
      return self._resolveFlags(*args)
    raise KeeBoxException(self, args)

  def _resolveNum(self, *args, **kwargs) -> Any:
    """
    The '_resolveNum' method resolves the arguments of the parentheses
    to a member of a 'KeeNum' field type: a lone member, name, answer of
    '__class_resolve__', position or value, else an instance of the
    value type built from the arguments and looked up as a value.
    """
    fieldNum = self.getFieldType()
    valueType = fieldNum.valueType
    if len(args) == 1 and not kwargs:
      arg = args[0]
      if self._isMember(arg):
        return arg
      if isinstance(arg, str):
        member = fieldNum._resolveFromName(arg)
        if member is not NotImplemented:
          return member
      if fieldNum.__custom_resolve__:
        #  This branch is reached by the following:
        #  - The enumeration defines '__class_resolve__', which a call of
        #    the class asks after the name and before the position
        member = fieldNum.__class_resolve__(arg)
        if member is not NotImplemented:
          return member
      if isinstance(arg, int) and not isinstance(arg, bool):
        if 0 <= arg < len(fieldNum):
          return fieldNum.members[arg]
      #  A lone 'bool' for an 'int' enumeration is refused by the value
      #  lookup of the class, as a call of the class refuses it.
      if isinstance(arg, valueType):
        return self._resolveValue(fieldNum, arg)
    try:
      tempObject = valueType(*args, **kwargs)
    except Exception as exception:
      raise KeeBoxTypeError(self, *args) from exception
    return self._resolveValue(fieldNum, tempObject)

  def _resolveValue(self, fieldNum: KeeMeta, value: Any) -> Any:
    """
    The '_resolveValue' method gives the first member carrying 'value',
    looked up in the value table of the enumeration as a call of the
    class looks it up, and raises 'KeeBoxValueError' naming the value
    when no member carries it.
    """
    member = fieldNum._resolveFromValue(value, fieldNum.valueType)
    if member is NotImplemented:
      raise KeeBoxValueError(self, fieldNum, value)
    return member

  def _resolveFlags(self, *args, ) -> Any:
    """
    The '_resolveFlags' method resolves the arguments of the parentheses
    to a member of a 'KeeFlags' field type. A lone container argument
    counts as several flag identifiers. Each identifier is resolved by
    subscripting the flags class, so the box accepts and refuses exactly
    what the class itself does, and the result is the member having
    every flag high that any of the resolved members has.
    """
    if len(args) == 1 and isinstance(args[0], (tuple, list, set, frozenset)):
      args = (*args[0],)
    fieldNum = self.getFieldType()
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
    to a class that is an instance of 'KeeMeta' or 'KeeFlagsMeta', raising
    'TypeException' otherwise, before delegating to
    'AttriBox.__class_getitem__'. The restriction simplifies the
    implementation; plain 'AttriBox' performs no such check and accepts
    every 'type'.
    """
    if isinstance(fieldType, KeeMeta) or isinstance(fieldType, KeeFlagsMeta):
      return super().__class_getitem__(fieldType)
    raise TypeException('fieldType', fieldType, KeeMeta, KeeFlagsMeta)
