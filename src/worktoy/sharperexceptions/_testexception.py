"""TestException"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from builtins import str
from typing import Never

from worktoy import maybe, maybeType, searchKeys
from worktoy.sharperexceptions import ReadOnlyError


class TestException(Exception):
  """LOL"""

  def __init__(self, *args, **kwargs) -> None:
    msgKwarg = searchKeys('msg') @ str >> kwargs
    msgArg = maybeType(str, *args)
    msgDefault = 'lol'
    self._msg = maybe(msgKwarg, msgArg, msgDefault)

  def __str__(self) -> str:
    """String representation"""
    return self._msg

  def _getMessage(self, ) -> str:
    """Getter-function for message"""
    return self._msg

  def _setMessage(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError()

  def _delMessage(self, *_) -> Never:
    """Illegal deleter function"""
    raise ReadOnlyError()

  msg = property(_getMessage, _setMessage, _delMessage)
