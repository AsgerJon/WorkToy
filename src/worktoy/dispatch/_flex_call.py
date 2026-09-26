"""
flexCall wraps a function with truncating positional-argument dispatch.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType
from typing import TYPE_CHECKING

from ..utilities import joinWords, textFmt
from ..waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

_CO_VARARGS: int = 0x04  # CPython compile flag
_FLEX_MARKER: str = '__flex_wrapped__'  # idempotency sentinel


def isFlex(func: FunctionType) -> bool:
  """
  The 'isFlex' function returns True if 'func' has already been wrapped
  by 'flexCall', detected by the presence of the idempotency marker.

  Parameters
  ----------
  func : FunctionType
      The function to test.

  Returns
  -------
  bool
      True if 'func' carries the flex marker, otherwise False.
  """
  try:
    _ = getattr(func, _FLEX_MARKER)
  except AttributeError:
    return False
  else:
    return True


def _missingNames(
    requiredNames: tuple[str, ...],
    received: int,
    kwargs: dict,
) -> tuple[str, ...]:
  """
  The '_missingNames' function returns the names of the required
  positional parameters that a call leaves without a value.
  'requiredNames' lists those parameters in order, and the first
  'received' of them took their values by position. Each later one is
  missing unless 'kwargs' names it. A positional-only parameter named in
  'kwargs' counts as supplied here, and the wrapped function then refuses
  it with its own 'TypeError', which says what went wrong.
  """
  out = []
  for name in requiredNames[received:]:
    if name not in kwargs:
      out.append(name)
  return (*out,)


def flexCall(func: FunctionType) -> FunctionType:
  """Wrap 'func' with truncating positional-argument dispatch.

  The descriptor notification callbacks of 'BaseDescriptor' are wrapped
  this way, since a descriptor passes each of them the same arguments
  however few it declares. So is every plain function in the body of a
  class whose namespace declares 'FlexCallHook'. An ordinary method is
  otherwise left as it was written.

  The returned wrapper:
  - silently drops positional args beyond the wrapped function's
    declared positional arity,
  - raises TypeError when a required positional parameter receives no
    value, neither by position nor by keyword (parameters with
    defaults are not counted as required); a missing required
    keyword-only argument, or a positional-only parameter named by
    keyword, is not checked here and surfaces as the wrapped
    function's own TypeError,
  - passes keyword args through unchanged,
  - carries the attributes set on the wrapped function,
  - caches arity at wrap time; per-call cost is one length check,
    one comparison, and a slice only when truncation fires.

  Returns 'func' itself, not a wrapper, when wrapping is a no-op:
  an already-wrapped function, a *args function, or a dunder.

  Parameters
  ----------
  func : FunctionType
      The function to wrap. Must be a plain Python function, not a
      builtin, method, classmethod, staticmethod, or any other
      non-FunctionType callable.

  Returns
  -------
  FunctionType
      A new function object with flex semantics, or 'func'
      unchanged when wrapping does not apply.

  Raises
  ------
  TypeError
      If 'func' is not an instance of 'types.FunctionType'.
  """
  if not isinstance(func, FunctionType):
    raise TypeException('func', func, FunctionType)

  #  Idempotent re-wrap.
  if getattr(func, _FLEX_MARKER, False):
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

  #  Manual metadata copy: explicit, dependency-free. The attributes set
  #  on 'func' come first, so the ones the wrapper sets below win.
  wrapper.__dict__.update(func.__dict__)
  wrapper.__name__ = func.__name__
  wrapper.__qualname__ = func.__qualname__
  wrapper.__module__ = func.__module__
  wrapper.__doc__ = func.__doc__
  wrapper.__annotations__ = func.__annotations__
  wrapper.__wrapped__ = func
  setattr(wrapper, _FLEX_MARKER, True)

  if TYPE_CHECKING:  # pragma: no cover
    assert isinstance(wrapper, FunctionType)  # pycharm, please!
  return wrapper
