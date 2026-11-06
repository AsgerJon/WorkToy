"""
flexCall wraps a function with truncating positional-argument dispatch.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from functools import wraps
from types import FunctionType
from typing import TYPE_CHECKING

from ..utilities import joinWords, textFmt
from ..waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any

_CO_VARARGS: int = 0x04  # CPython compile flag
_FLEX_MARKER: str = '__flex_wrapped__'  # idempotency sentinel


def isFlex(func: FunctionType) -> bool:
  """
  Wrapping a function twice by 'flexCall' must be avoided, so code needs
  to tell whether a function is wrapped already, even when it is handed an
  object whose class answers every name through '__getattr__'.

  Implementation
  --------------

  The marker 'flexCall' sets on its wrapper is read with
  'object.__getattribute__'.

  Parameters
  ----------

  func : FunctionType
    The function to test.

  Returns
  -------

  bool
    Whether the function is a wrapper made by 'flexCall'.
  """
  try:
    _ = object.__getattribute__(func, _FLEX_MARKER)
  except AttributeError:
    return False
  else:
    return True


def _missingNames(
    requiredNames: tuple[str, ...],
    received: int,
    kwargs: dict,
) -> tuple[str, ...]:
  out = []
  for name in requiredNames[received:]:
    if name not in kwargs:
      out.append(name)
  return (*out,)


def flexCall(func: FunctionType) -> FunctionType:
  """
  A descriptor passes each of its notification callbacks the same
  arguments, the instance and, for some, the value, however few the
  callback declares, and a callback must be free to declare only what it
  uses. A namespace may likewise want every method of its classes to
  accept surplus positional arguments. Such a call must drop the
  arguments the function does not declare, yet still fail clearly when a
  required argument is missing, and the function must look like itself
  to anything inspecting it.

  Implementation
  --------------

  The positional parameter counts are read once, when wrapping. The
  wrapper cuts surplus positional arguments, passes keywords on, and
  raises a 'TypeError' naming the required positional parameters that
  received no value by position or keyword; a missing keyword-only
  argument is left to the function itself. 'functools.wraps' copies the
  name, docstring and attributes, and '__wrapped__' holds the function.
  A function already wrapped, one taking '*args', or one with a dunder
  name, which the interpreter calls with fixed arguments, is returned as
  it is. The wrapper is a plain function, so a wrapped 'async def' or
  generator function still returns its coroutine or generator but is no
  longer recognized as such by 'inspect'.

  Parameters
  ----------

  func : FunctionType
    A plain Python function; a builtin, a bound method, a 'classmethod'
    or 'staticmethod' object or any other callable is refused.

  Returns
  -------

  FunctionType
    The wrapper, or 'func' itself when wrapping does not apply.

  Raises
  ------

  TypeException
    'func' is not a 'types.FunctionType'.
  """
  if not isinstance(func, FunctionType):
    raise TypeException('func', func, FunctionType)

  #  Idempotent re-wrap.
  if isFlex(func):
    return func

  code = func.__code__

  #  *args function: flex truncation is meaningless.
  if code.co_flags & _CO_VARARGS:
    return func

  #  Dunders sit on protocols whose call shapes the interpreter
  #  introspects directly; safer to leave them alone.
  name: str = func.__name__
  if name.startswith('__') and name.endswith('__'):
    return func

  #  Cache positional arity in closure cells: read once, never
  #  re-introspected per call.
  maxPos: int = code.co_argcount
  minPos: int = code.co_argcount - len(func.__defaults__ or ())
  requiredNames: tuple[str, ...] = code.co_varnames[:minPos]

  @wraps(func)
  def wrapper(*args, **kwargs) -> Any:
    n: int = len(args)
    if n < minPos:
      missing = _missingNames(requiredNames, n, kwargs)
      if missing:
        infoSpec: str = """Function '%s' requires at least '%d' positional
        arguments but received only '%d', missing arguments: (%s)!"""
        missingStr = joinWords(*missing, )
        info = infoSpec % (name, minPos, n, missingStr)
        raise TypeError(textFmt(info))
    if n > maxPos:
      args = args[:maxPos]
    return func(*args, **kwargs)

  setattr(wrapper, _FLEX_MARKER, True)

  if TYPE_CHECKING:  # pragma: no cover, no mutate
    assert isinstance(wrapper, FunctionType)  # pycharm, please!
  return wrapper
