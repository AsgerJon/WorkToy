"""Strict type-casting helper.

The ``typeCast`` function converts a value to a target type using
hand-written rules for the built-in numeric, string, and container
types so that lossy or surprising coercions raise instead of
silently succeeding. For other targets, the target's constructor
is called as a fallback."""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import ValidSlice

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Dict, Tuple, TypeAlias, Union

  Slice: TypeAlias = Union[slice, ValidSlice]


def _exc(target: type, arg: Any) -> Exception:
  """Build a ``TypeCastException``.

  The import is deferred so ``utilities`` does not pull in
  ``waitaminute`` at module load time.
  """
  from worktoy.waitaminute.dispatch import TypeCastException
  return TypeCastException(target, arg)


def _castSlice(arg: Any) -> Slice:
  if isinstance(arg, ValidSlice):
    return arg
  if isinstance(slice(arg), ValidSlice):
    return slice(arg)
  if isinstance(arg, (list, tuple)) and arg:
    a, b, c, *_ = (*arg, None, None, None)
    if isinstance(slice(a, b, c), ValidSlice):
      return slice(a, b, c)
  raise _exc(slice, arg)


def _castStr(arg: Any) -> str:
  if isinstance(arg, (bytes, bytearray)):
    try:
      return arg.decode('utf-8')
    except Exception as exception:
      raise _exc(str, arg) from exception
  raise _exc(str, arg)


def _castBool(arg: Any) -> bool:
  if arg in (True, False, 0, 1):
    return bool(arg)
  raise _exc(bool, arg)


def _castInt(arg: Any) -> int:
  if isinstance(arg, float):
    if arg.is_integer():
      return int(arg)
    raise _exc(int, arg)
  if isinstance(arg, complex):
    if arg.imag == 0 and arg.real.is_integer():
      return int(arg.real)
    raise _exc(int, arg)
  if isinstance(arg, str):
    try:
      return int(arg)
    except Exception as exception:
      raise _exc(int, arg) from exception
  raise _exc(int, arg)


def _castFloat(arg: Any) -> float:
  if isinstance(arg, int):
    return float(arg)
  if isinstance(arg, complex):
    if arg.imag == 0:
      return float(arg.real)
    raise _exc(float, arg)
  if isinstance(arg, str):
    try:
      return float(arg)
    except Exception as exception:
      raise _exc(float, arg) from exception
  raise _exc(float, arg)


def _castComplex(arg: Any) -> complex:
  if isinstance(arg, (int, float)):
    return float(arg) + 0j
  if isinstance(arg, str):
    try:
      return complex(arg)
    except Exception as exception:
      raise _exc(complex, arg) from exception
  raise _exc(complex, arg)


def _castDict(arg: Any) -> dict:
  try:
    return {**arg, }
  except Exception as exception:
    raise _exc(dict, arg) from exception


_CONTAINERS: Tuple[type, ...] = (list, tuple, set, frozenset)


def _castContainer(target: type, arg: Any) -> Any:
  """Convert between built-in containers.

  The early ``isinstance(arg, target)`` check in ``typeCast``
  guarantees ``arg`` is not already the target type by the time
  this runs.
  """
  if isinstance(arg, _CONTAINERS):
    return target(arg)
  if isinstance(arg, dict):
    return target(arg.items())
  raise _exc(target, arg)


_SCALAR_HANDLERS: Dict[type, Callable[[Any], Any]] = {
  str    : _castStr,
  bool   : _castBool,
  int    : _castInt,
  float  : _castFloat,
  complex: _castComplex,
  dict   : _castDict,
}


def typeCast(target: type, arg: Any, **kwargs) -> Any:
  """Cast ``arg`` to ``target``, raising on lossy conversions.

  When ``arg`` is already an instance of ``target``, it is
  returned unchanged (except for ``slice``, which is always
  re-validated through ``ValidSlice``). Otherwise the per-type
  rules below apply; any failure raises ``TypeCastException``.

  Per-target rules
  ----------------
  - ``slice`` : accepts a ``slice``, a single index, or a
    ``list`` / ``tuple`` of up to three values that yield a valid
    slice. Validated via ``ValidSlice``.
  - ``str`` : accepts ``bytes`` / ``bytearray`` (UTF-8 decoded);
    arbitrary objects are *not* stringified.
  - ``bool`` : accepts only values equal to ``0``, ``1``,
    ``True``, ``False`` (note: ``1.0`` compares equal to ``1``).
  - ``int`` : accepts ``float`` if ``is_integer``, real-valued
    integer ``complex``, parseable ``str``.
  - ``float`` : accepts ``int``, real-valued ``complex``,
    parseable ``str``.
  - ``complex`` : accepts ``int``, ``float``, parseable ``str``.
  - ``list`` / ``tuple`` / ``set`` / ``frozenset`` : accept any
    other built-in container; ``dict`` is converted via its
    ``(key, value)`` pairs.
  - ``dict`` : accepts anything that splats with ``{**arg}``.
  - ``type`` : only succeeds if ``arg`` is already a class.
  - any other target : the target's constructor is called on
    ``arg``. Suppress this fallback with
    ``allowInstantiation=False``.

  Parameters
  ----------
  target : type
      The desired result type.
  arg : Any
      The value to cast.
  **kwargs
      allowInstantiation : bool, optional
          Whether to fall back to ``target(arg)`` for non-special
          targets. Defaults to ``True``.

  Returns
  -------
  Any
      ``arg`` cast to ``target``.

  Raises
  ------
  TypeCastException
      If the cast cannot be performed losslessly.

  Examples
  --------
  >>> typeCast(int, 3.0)
  3
  >>> typeCast(str, b'hello')
  'hello'
  >>> typeCast(list, (1, 2, 3))
  [1, 2, 3]
  """
  if target is slice:
    return _castSlice(arg)
  if isinstance(arg, target):
    return arg
  if target is type:
    raise _exc(type, arg)
  handler = _SCALAR_HANDLERS.get(target)
  if handler is not None:
    return handler(arg)
  if target in _CONTAINERS:
    return _castContainer(target, arg)
  if kwargs.get('allowInstantiation', True):
    try:
      return target(arg)
    except Exception as exception:
      raise _exc(target, arg) from exception
  raise _exc(target, arg)
