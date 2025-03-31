"""CallMeMeta provides a metaclass for the CallMeMaybe class."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractMetaclass
from worktoy.text import monoSpace

try:
  from typing import Never
except ImportError:
  try:
    from typing import NoReturn as Never
  except ImportError:
    from typing import Any as Never

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False


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

  def __call__(self, *__, **_) -> Never:
    """This is just here to persuade Pycharm that this is a callable. """
    raise RuntimeError('breh')


if TYPE_CHECKING:
  assert callable(CallMeMaybe)
