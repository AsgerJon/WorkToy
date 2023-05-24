"""CallMeMaybe represents callable types."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import collections.abc
import typing

from icecream import ic

ic.configureOutput(includeContext=True)

_HereIsMyNumber = getattr(typing, '_GenericAlias', None)
_ThisIsCrazy = getattr(typing, 'Callable', None)
_TryToChaseMe = getattr(collections.abc, 'Callable', None)


class _CallMeMaybe(_HereIsMyNumber, _root='F... da police!'):
  """Is this it?"""

  def __init_subclass__(cls, /, *args, **kwargs):
    """LOL"""

  def __init__(self, *args, **kwargs) -> None:
    _HereIsMyNumber.__init__(self, *args, **kwargs)

  @classmethod
  def __instancecheck__(cls, instance) -> bool:
    """Implementing instance check"""
    if cls._typingCheck(instance):
      return True
    if cls._collectionCheck(instance):
      return True
    return False

  @classmethod
  def _typingCheck(cls, instance) -> bool:
    """Checking with typing module"""
    return True if isinstance(instance, _ThisIsCrazy) else False

  @classmethod
  def _collectionCheck(cls, instance) -> bool:
    """Checking with typing module"""
    return True if isinstance(instance, _TryToChaseMe) else False

  @classmethod
  def _nativeCheck(cls, instance) -> bool:
    """Checking with builtin word callable"""
    return True if callable(instance) else False


class NothingAtAll(_CallMeMaybe):
  """HereIsMeNumber!"""

  @classmethod
  def __instancecheck__(cls, instance: typing.Any) -> bool:
    """Reimplementation"""
    return _CallMeMaybe.__instancecheck__(instance)

  def __init__(self, *__, **_) -> None:
    _CallMeMaybe.__init__(self, _TryToChaseMe, (bool,))


CallMeMaybe = NothingAtAll()
