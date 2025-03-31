"""AbstractNamespace class provides a base class for custom namespace
objects used in custom metaclasses."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.static import maybe
from worktoy.text import stringList

try:
  from typing import Any
except ImportError:
  Any = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False


class _KeyVal:
  """Represents a key or val"""

  __pvt_name__ = None

  def __init__(self, name: str) -> None:
    self.__pvt_name__ = name

  def __get__(self, instance: object, owner: type) -> Any:
    return getattr(instance, self.__pvt_name__)


class _Item:
  """Baseclass for __getitem__ and __setitem__"""
  pass


class _GetItem(_Item):
  """Represents a call to __getitem__."""

  __key__ = None
  __val__ = None

  key = _KeyVal('__key__')
  val = _KeyVal('__val__')

  def __init__(self, key: str, val: object) -> None:
    self.__key__ = key
    self.__val__ = val


class _SetItem(_Item):
  """Represents a call to __setitem__."""

  __key__ = None
  __old_val__ = None
  __new_val__ = None

  key = _KeyVal('__key__')
  oldVal = _KeyVal('__old_val__')
  newVal = _KeyVal('__new_val__')

  def __init__(self, key: str, old_val: object, new_val: object) -> None:
    self.__key__ = key
    self.__old_val__ = old_val
    self.__new_val__ = new_val


if TYPE_CHECKING:
  ItemList = list[_Item]
else:
  ItemList = object


class AbstractNamespace(dict):
  """AbstractNamespace class provides a base class for custom namespace
  objects used in custom metaclasses."""

  __metaclass__ = None
  __class_name__ = None
  __base_classes__ = None
  __key_args__ = None
  __access_lines__ = None

  __special_keys__ = """__qualname__, __module__, __firstlineno__, 
  __doc__, __annotations__, __dict__, __weakref__, __module__, 
  __metaclass__, __class__, __bases__, __name__, __class_name__,
  __static_attributes__"""

  @classmethod
  def getSpecialKeys(cls) -> list[str]:
    """Getter-function for special keys that are passed to the namespace
    object during class creation from unseen sources. These mysterious
    keys and their values must be respected. The recommended procedure is
    to simply invoke: 'dict.__setitem__(self, key, value)' Not adhering to
    this recommendation may lead to HIGHLY UNDEFINED BEHAVIOUR!"""
    return stringList(cls.__special_keys__)

  @classmethod
  def isSpecialKey(cls, key: str) -> bool:
    """Checks if the key is a special key."""
    return True if key in cls.getSpecialKeys() else False

  def __init__(self, *args, **kwargs) -> None:
    mcls, name, bases = [*args, None, None, None][:3]
    if any([arg is None for arg in args]):
      e = """Unable to parse metaclass, name and baseclasses!"""
      raise ValueError(e)
    self.__metaclass__ = mcls
    self.__class_name__ = name
    self.__base_classes__ = [*bases, ]
    self.__key_args__ = kwargs or {}

  def getMetaclass(self, ) -> type:
    """Returns the metaclass."""
    return self.__metaclass__

  def getClassName(self, ) -> str:
    """Returns the name of the class."""
    return self.__class_name__

  def getBaseClasses(self, ) -> list[type]:
    """Returns the base classes of the class."""
    return self.__base_classes__

  def _getLines(self) -> ItemList:
    """Returns the lines of the class."""
    return maybe(self.__access_lines__, [])

  def _appendGetLine(self, key: str, val: object) -> None:
    """Appends a get line to the class."""
    existing = self._getLines()
    self.__access_lines__ = [*existing, _GetItem(key, val)]

  def _appendSetLine(self, key: str, oldVal: object, newVal: object) -> None:
    """Appends a set line to the class."""
    existing = self._getLines()
    self.__access_lines__ = [*existing, _SetItem(key, oldVal, newVal)]

  def __getitem__(self, key: str) -> Any:
    """Returns the value of the key."""
    try:
      val = dict.__getitem__(self, key)
      self._appendGetLine(key, val)
      return val
    except KeyError as keyError:
      self._appendGetLine(key, keyError)
      raise keyError

  def __setitem__(self, key: str, val: object) -> None:
    """Sets the value of the key."""
    try:
      oldVal = dict.__getitem__(self, key)
    except KeyError:
      oldVal = None
    self._appendSetLine(key, oldVal, val)
    dict.__setitem__(self, key, val)

  def compile(self, ) -> dict:
    """Builds the final namespace object"""
    out = {}
    for (key, val) in self.items():
      out[key] = val
    out['__metaclass__'] = self.getMetaclass()
    out['__namespace__'] = self
    out['__namespace_lines__'] = self._getLines()
    return out
