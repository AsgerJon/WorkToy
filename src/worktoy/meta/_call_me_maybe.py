"""CallMeMeta provides a metaclass for the CallMeMaybe class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from worktoy.meta import AbstractMetaclass
from worktoy.text import monoSpace


def _func() -> None:
  """Sample Function"""


_function = type(_func)
_lambda = type(lambda: None)


class _CallMeMeta(AbstractMetaclass):
  """CallMeMeta provides a metaclass for the CallMeMaybe class."""

  def __instancecheck__(cls, callMeMaybe: object) -> bool:
    """Reimplementation recognizing function-like objects. """
    if isinstance(callMeMaybe, (_function, _lambda)):
      return True
    call = getattr(type(callMeMaybe), '__call__', )
    if isinstance(call, (_function, _lambda)):
      return True
    return False

  def __subclasscheck__(cls, subCls: object) -> bool:
    """If 'someObject' pass the '__instancecheck__' method,
    then 'type(someObject)' should pass this method. """

    def inner(arg) -> bool:
      """Inner"""
      if not isinstance(subCls, type):
        return False
      if subCls in [_function, _lambda]:
        return True
      call = getattr(subCls, '__call__', )
      if call in [_function, _lambda]:
        return True
      return False

    out = inner(subCls)
    return out

  def __subclasshook__(cls, __subclass) -> Never:
    """Prevents subclassing of the derived classes. """
    e = """Class '%s' derived from '%s' cannot be subclassed!"""
    raise TypeError(monoSpace(e % (cls.__name__, cls.__class__.__name__)))

  def __call__(cls, *__, **_) -> Never:
    """Prevents the instantiation of the derived classes. """
    e = """Class '%s' derived from '%s' cannot be instantiated!"""
    raise TypeError(monoSpace(e % (cls.__name__, cls.__class__.__name__)))


class CallMeMaybe(metaclass=_CallMeMeta):
  """CallMeMaybe represents types that can be treated as functions. """
  pass
