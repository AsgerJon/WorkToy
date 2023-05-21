"""Parsify is a class providing a systematic parsing of positional and
keyword arguments for flexible use in functions and classes."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never, NoReturn

from worktoy import PositionalArgumentError, searchKeys, maybeType
from worktoy.sharperexceptions import ReadOnlyError


class Parsify:
  """Parsify is a class providing a systematic parsing of positional and
  keyword arguments for flexible use in functions and classes.
  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    self._curInd = 0
    self._posArgs = [*args]
    self._keyArgs = kwargs

  def _removePosArg(self, posArg: Any = None) -> Any:
    """Arg must be in self._posArgs. This method removes it. This method
    must be invoked by any methods which transmits a positional argument
    to the outside, so that it does not get spent multiple times."""
    if posArg is None:
      return None
    for arg in self:
      pass

  def _removeKeyArg(self, key: str = None) -> Any:
    """The key maps to a member of kwarg which is then overwritten."""
    val = searchKeys(key) >> self._keyArgs
    if val is None:
      return None
    self._keyArgs |= {key: None}
    return val

  def _getPosType(self, type_: type) -> Any:
    """Getter-function for the first positional argument of the given type"""

  def __contains__(self, posArg: Any) -> bool:
    """posArg in self checks if given argument is one of the positional
    arguments"""
    for arg in self:
      if arg == posArg:
        return True
    return False

  def __getitem__(self, index: int | str) -> NoReturn:
    """Implementation of item getting"""
    if isinstance(index, int):
      return self._getByIndex(index, )
    if isinstance(index, str):
      return self._getByKey(index, )
    msg = """Expected index to be one of %s or %s, but received: %s"""
    raise TypeError(msg % (str, int, type(index)))

  def __setitem__(self, index: int | str, val: Any = None) -> NoReturn:
    """Implementation item setting."""
    if isinstance(index, int):
      return self._setByIndex(index, val)
    if isinstance(index, str):
      return self._setByKey(index, val)
    msg = """Expected index to be one of %s or %s, but received: %s"""
    raise TypeError(msg % (str, int, type(index)))

  def _getByIndex(self, index: int) -> Any:
    """Item getter by index"""
    return self._posArgs

  def _setByIndex(self, index: int, val: Any) -> NoReturn:
    """Item getter by index"""
    raise NotImplementedError

  def _getByKey(self, key: str) -> Any:
    """Item getter by index"""
    raise NotImplementedError

  def _setByKey(self, key: str, val: Any) -> Any:
    """Item getter by index"""
    raise NotImplementedError

  def __len__(self) -> int:
    """The length of the instance is understood to mean the number of
    positional arguments"""
    return len(self.posArgs)

  def __iter__(self, ) -> Parsify:
    """Implementation of iteration applies to the positional arguments"""
    self._curInd = 0
    return self

  def __next__(self, ) -> Any:
    """Implementation of iteration applies to the positional arguments"""
    self._curInd += 1
    if self._curInd > len(self):
      raise StopIteration
    return self.posArgs[self._curInd - 1]

  def _getPosArgs(self) -> list[Any]:
    """Getter-function for list of positional arguments"""
    return self._posArgs

  def _setPosArgs(self, *_) -> Never:
    """Illegal setter-function"""
    raise ReadOnlyError('posArgs')

  def _delPosArgs(self, *_) -> Never:
    """Illegal setter-function"""
    raise ReadOnlyError('posArgs')

  posArgs = property(_getPosArgs, _setPosArgs, _delPosArgs)
