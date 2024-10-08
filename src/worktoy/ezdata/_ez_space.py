"""EZSpace provides the namespace object class for the EZData class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import FastSpace
from worktoy.ezdata import IllegalInitException, IllegalMethodException, \
  NoDefaultError, AmbiguousDefaultError, DefaultTypeMismatchError
from worktoy.meta import CallMeMaybe
from worktoy.parse import maybe
from worktoy.text import typeMsg

from worktoy.desc import AttriBox

try:
  from typing import Callable
except ImportError:
  Callable = object

try:
  from typing import TypeAlias
except ImportError:
  TypeAlias = object

try:
  Boxes: TypeAlias = list[tuple[str, AttriBox]]
except ImportError:
  Boxes = object


class EZSpace(FastSpace):
  """Expands the FastSpace class with auto generated '__init__' method.
  Additionally, custom methods are disallowed. Classes that require
  methods should instead use FastObject. """

  __allow_init__ = False  # Allow the '__init__' method to be set.

  def _enableInit(self) -> None:
    """Enables the init method"""
    self.__allow_init__ = True

  def _disableInit(self, ) -> None:
    """Disables the init method"""
    self.__allow_init__ = False

  def _getAllowInit(self, ) -> bool:
    """Getter-function for allow init flag"""
    return True if self.__allow_init__ else False

  def __setitem__(self, key: str, value: object, **kwargs) -> None:
    """This method sets the key, value pair in the namespace."""
    if key == '__trust_me_bro__':
      if value:
        return self._enableInit()
      return self._disableInit()
    if kwargs.get('__trust_me_bro__', False):
      return FastSpace.__setitem__(self, key, value)
    if key == '__init__':
      if self._getAllowInit():
        self._disableInit()
        return FastSpace.__setitem__(self, key, value)
      clsName = self.getClassName()
      raise IllegalInitException(clsName, value)
    if self.isSpecialKey(key):
      return dict.__setitem__(self, key, value)
    if isinstance(value, AttriBox):
      return FastSpace.__setitem__(self, key, value)
    if callable(value):
      clsName = self.getClassName()
      raise IllegalMethodException(clsName, key, value)
    return FastSpace.__setitem__(self, key, value)

  def _unpackBoxes(self) -> tuple[list[str], list[object]]:
    """Unpacks the instances of AttriBox into keys and default values."""
    keys, defVals = [], []
    boxes = self._getAllBoxes()
    n = len(boxes)
    defVal = None
    clsName = self.getClassName()
    for (key, box) in boxes:
      keys.append(key)
      posArgs = AttriBox.getArgs(box, None, _root=True)
      if not posArgs:
        raise NoDefaultError(clsName, key, box)
      if len(posArgs) > 1:
        raise AmbiguousDefaultError(clsName, key, box)
      defVal = posArgs[0]
      fieldClass = AttriBox.getFieldClass(box)
      if not isinstance(defVal, fieldClass):
        raise DefaultTypeMismatchError(clsName, key, box, defVal)
      defVals.append(defVal)
    return keys, defVals

  def _getBoxKeys(self) -> list[str]:
    """Getter-function for the keys to the AttriBox instances."""
    return self._unpackBoxes()[0]

  def _getDefaultValues(self) -> list[object]:
    """Getter-function for the default values of the AttriBox instances."""
    return self._unpackBoxes()[1]

  def ezInitFactory(self, ) -> CallMeMaybe:
    """This factory creates a fast, but inflexible '__init__' method."""
    keys, defVals = self._unpackBoxes()
    n = len(keys)

    def __init__(instance, *args, ) -> None:
      pArgs = [*args, *[None, ] * (max([0, n - len(args)]))]
      for (k, arg, v) in zip(keys, pArgs, defVals):
        setattr(instance, k, maybe(arg, v))

    return __init__

  def ezStrFactory(self, ) -> CallMeMaybe:
    """Factory method for the '__str__' method."""
    keys, defVals = self._unpackBoxes()

    def __str__(instance, ) -> str:
      """String representation"""
      clsName = self.getClassName()
      valStr = [str(getattr(instance, key)) for key in keys]
      return '%s(%s)' % (clsName, ', '.join(valStr))

    return __str__

  def ezEqFactory(self) -> CallMeMaybe:
    """Factory method for the '__eq__' method"""
    keys, defVals = self._unpackBoxes()

    def __eq__(instance, other: object) -> bool:
      for key in keys:
        if getattr(instance, key) - getattr(other, key):
          return False
      else:
        return True

    return __eq__
