"""ZeroFilter provides a callable that replaces instances of Zerotons with
instance variables in the instance. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from warnings import warn

from worktoy.desc import THIS, TYPE, ATTR, BOX, Field
from worktoy.parse import maybe
from worktoy.text import stringList, monoSpace

_zeroDict = dict(this=THIS, type=TYPE, attr=ATTR, box=BOX)


class ZeroFilter:
  """ZeroFilter provides a callable that replaces instances of Zerotons with
  instance variables in the instance. """

  __this_value__ = None
  __type_value__ = None
  __attr_value__ = None
  __box_value__ = None

  thisValue = Field()
  typeValue = Field()
  attrValue = Field()
  boxValue = Field()

  @thisValue.GET
  def _getThisValue(self) -> object:
    if self.__this_value__ is None:
      return THIS
    return self.__this_value__

  @thisValue.SET
  def _setThisValue(self, newThis: object) -> None:
    self.__this_value__ = newThis

  @typeValue.GET
  def _getTypeValue(self) -> object:
    if self.__type_value__ is None:
      return TYPE
    return self.__type_value__

  @typeValue.SET
  def _setTypeValue(self, newType: object) -> None:
    self.__type_value__ = newType

  @attrValue.GET
  def _getAttrValue(self) -> object:
    if self.__attr_value__ is None:
      return ATTR
    return self.__attr_value__

  @attrValue.SET
  def _setAttrValue(self, newAttr: object) -> None:
    self.__attr_value__ = newAttr

  @boxValue.GET
  def _getBoxValue(self) -> object:
    if self.__box_value__ is None:
      return BOX
    return self.__box_value__

  @boxValue.SET
  def _setBoxValue(self, newBox: object) -> None:
    self.__box_value__ = newBox

  def __init__(self, *args, **kwargs) -> None:
    keys = stringList("""this, type, attr, box""")
    keyArgs = [kwargs.get(k, None) for k in keys]
    posArgs = [*args, None, None, None, None][:4]
    self.__this_value__ = maybe(posArgs[0], keyArgs[0])
    self.__type_value__ = maybe(posArgs[1], keyArgs[1])
    self.__attr_value__ = maybe(posArgs[2], keyArgs[2])
    self.__box_value__ = maybe(posArgs[3], keyArgs[3])

  def __getitem__(self, key: object, **kwargs) -> object:
    if isinstance(key, str):
      if kwargs.get('_recursion', False):
        raise RecursionError
      if key in _zeroDict:
        return self.__getitem__(key=_zeroDict[key], _recursion=True)
      raise KeyError(key)
    if key is THIS:
      return self.thisValue
    if key is TYPE:
      return self.typeValue
    if key is ATTR:
      return self.attrValue
    if key is BOX:
      return self.boxValue
    raise KeyError(key)

  def __setitem__(self, key: object, value: object, **kwargs) -> None:
    if isinstance(key, str):
      if kwargs.get('_recursion', False):
        raise RecursionError
      if key in _zeroDict:
        return self.__setitem__(_zeroDict[key], value, _recursion=True)
      raise KeyError(key)
    if key is THIS:
      self.thisValue = value
    elif key is TYPE:
      self.typeValue = value
    elif key is ATTR:
      self.attrValue = value
    elif key is BOX:
      self.boxValue = value
    else:
      raise KeyError(key)

  def __delitem__(self, key: object, **kwargs) -> None:
    if isinstance(key, str):
      if kwargs.get('_recursion', False):
        raise RecursionError
      if key in _zeroDict:
        return self.__delitem__(_zeroDict[key], _recursion=True)
      raise KeyError(key)
    if key is THIS:
      self.thisValue = None
    elif key is TYPE:
      self.typeValue = None
    elif key is ATTR:
      self.attrValue = None
    elif key is BOX:
      self.boxValue = None
    else:
      raise KeyError(key)

  def __call__(self, obj: object) -> object:
    """Replaces the object with the value defined in the filter or falls
    back to the object itself. """
    try:
      return self[obj]
    except KeyError as keyError:
      return obj
    except RecursionError:
      w = """The filter received: '%s' and raised a RecursionError!"""
      warn(monoSpace(w))
      return obj
