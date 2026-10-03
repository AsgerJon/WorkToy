"""
The 'typeCast' function casts a value to a target type, raising on a lossy
conversion.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING

from . import ValidSlice

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Dict, Optional, Tuple, TypeAlias, Union

  Slice: TypeAlias = Union[slice, ValidSlice]


def _exc(target: type, arg: Any) -> Exception:
  """Build a 'TypeCastException'.

  The import is deferred so 'utilities' does not pull in
  'waitaminute' at module load time.
  """
  from worktoy.waitaminute.dispatch import TypeCastException
  return TypeCastException(target, arg)


def _castSlice(arg: Any) -> Slice:
  if isinstance(arg, ValidSlice):
    return arg
  if isinstance(slice(arg), ValidSlice):
    return slice(arg)
  if isinstance(arg, (list, tuple)) and arg:
    if len(arg) > 3:
      raise _exc(slice, arg)
    #  The values read as the arguments of 'slice' do: a single one is
    #  the stop.
    if isinstance(slice(*arg), ValidSlice):
      return slice(*arg)
  raise _exc(slice, arg)


def _castStr(arg: Any) -> str:
  if isinstance(arg, (bytes, bytearray)):
    try:
      return arg.decode('utf-8')
    except Exception as exception:
      raise _exc(str, arg) from exception
  raise _exc(str, arg)


def _encodeText(target: type, arg: str) -> bytes:
  try:
    return arg.encode('utf-8')
  except UnicodeEncodeError as exception:
    raise _exc(target, arg) from exception


def _castBytes(arg: Any) -> bytes:
  if isinstance(arg, bytearray):
    return bytes(arg)
  if isinstance(arg, str):
    return _encodeText(bytes, arg)
  raise _exc(bytes, arg)


def _castByteArray(arg: Any) -> bytearray:
  if isinstance(arg, bytes):
    return bytearray(arg)
  if isinstance(arg, str):
    return bytearray(_encodeText(bytearray, arg))
  raise _exc(bytearray, arg)


def _castBool(arg: Any) -> bool:
  """Only a number is compared with 0 and 1. Comparing anything else
  would ask its own '__eq__', which may answer 'True' to anything or
  raise."""
  if isinstance(arg, Number) and arg in (True, False, 0, 1):
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
    try:
      out = float(arg)
    except OverflowError as overflowError:
      raise _exc(float, arg) from overflowError
    if int(out) != arg:
      raise _exc(float, arg)
    return out
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
  if isinstance(arg, int):
    try:
      out = float(arg)
    except OverflowError as overflowError:
      raise _exc(complex, arg) from overflowError
    if int(out) != arg:
      raise _exc(complex, arg)
    return out + 0j
  if isinstance(arg, float):
    return arg + 0j
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

  'typeCast' calls this only for an 'arg' that is not already of the
  target type.
  """
  if not isinstance(arg, (*_CONTAINERS, dict)):
    raise _exc(target, arg)
  try:
    if isinstance(arg, dict):
      casted = target(arg.items())
    else:
      casted = target(arg)
  except TypeError as typeError:
    raise _exc(target, arg) from typeError
  else:
    return casted


_SCALAR_HANDLERS: Dict[type, Callable[[Any], Any]] = {
  str      : _castStr,
  bytes    : _castBytes,
  bytearray: _castByteArray,
  bool     : _castBool,
  int      : _castInt,
  float    : _castFloat,
  complex  : _castComplex,
  dict     : _castDict,
}


def _ruledBase(target: type) -> Optional[type]:
  """The first class along the method resolution order of 'target' that
  'typeCast' has a rule for, or 'None' when it has none. A builtin with a
  rule finds itself, and a subclass of one finds that builtin."""
  for base in getattr(target, '__mro__', ()):
    if base in _SCALAR_HANDLERS or base in _CONTAINERS:
      return base
  return None


def _ownsConstructor(target: type, base: type) -> bool:
  """Whether calling 'target' runs a constructor other than that of
  'base': a '__new__' or an '__init__' that the subclass defines, inherits
  from a class between itself and 'base', or takes from a mixin after
  'base'. The attributes are compared as they resolve on each class,
  since a check of the subclass's own namespace would miss the last
  two."""
  ownNew = target.__new__ is not base.__new__
  ownInit = target.__init__ is not base.__init__
  return True if ownNew or ownInit else False


def castRule(target: type) -> Optional[type]:
  """
  The 'castRule' function names the builtin whose rule 'typeCast' holds
  'target' to, or returns 'None' when 'typeCast' trusts the constructor
  of 'target' instead.

  A builtin with a rule, such as 'str', 'int' or 'list', is its own rule.
  A subclass of one that keeps the constructor of that builtin is the
  builtin under another name, so it is held to the rule of the builtin,
  and the cast then builds the subclass from the result. A subclass with
  a constructor of its own has stated how it converts a value, as an
  'IntEnum' or 'collections.Counter' has, and so has any class based on
  no builtin with a rule; for those the answer is 'None'.

  'AttriBox' asks this as well, so the boxes and the overload dispatch
  decide the same way.

  Parameters
  ----------
  target : type
      The type a value is cast to.

  Returns
  -------
  Optional[type]
      The builtin whose rule applies, or 'None' when the constructor of
      'target' decides.

  Examples
  --------
  >>> class Name(str):
  ...   pass
  >>> castRule(Name)
  <class 'str'>
  >>> from enum import IntEnum
  >>> class Level(IntEnum):
  ...   LOW = 1
  >>> castRule(Level) is None
  True
  """
  base = _ruledBase(target)
  if base is None or base is target:
    return base
  if _ownsConstructor(target, base):
    return None
  return base


def _castRuled(base: type, arg: Any) -> Any:
  handler = _SCALAR_HANDLERS.get(base)
  if handler is not None:
    return handler(arg)
  return _castContainer(base, arg)


def _castSubclass(target: type, base: type, arg: Any) -> Any:
  """Cast 'arg' to 'target', a subclass of the builtin 'base' that keeps
  the constructor of 'base'. 'arg' is held to the rule of 'base', unless
  it is already an instance of it, and 'target' is then built from the
  result, so the cast is as lossless as one to 'base' and gives an
  instance of 'target'. Only a metaclass overriding the call can still
  make that build refuse or return something else, and both are refused
  here."""
  from worktoy.waitaminute.dispatch import TypeCastException
  value = arg
  if not isinstance(arg, base):
    try:
      value = _castRuled(base, arg)
    except TypeCastException as typeCastException:
      raise _exc(target, arg) from typeCastException
  try:
    out = target(value)
  except Exception as exception:
    raise _exc(target, arg) from exception
  if isinstance(out, target):
    return out
  raise _exc(target, arg)


def typeCast(target: type, arg: Any, **kwargs) -> Any:
  """
  This function centralizes conversion between types in the 'worktoy'
  library. 

  When 'arg' is already an instance of 'target', it is
  returned unchanged (except for 'slice', which is always
  re-validated through 'ValidSlice'). Otherwise the per-type
  rules below apply; any failure raises 'TypeCastException'.

  Per-target rules
  ----------------
  - 'slice' : accepts a 'slice', a single index, or a
    'list' / 'tuple' of up to three values that yield a valid
    slice, read as the arguments of 'slice' are, so a single
    value is the stop; more than three values fail. Validated
    via 'ValidSlice'.
  - 'str' : accepts 'bytes' / 'bytearray' (UTF-8 decoded);
    arbitrary objects are *not* stringified.
  - 'bytes' / 'bytearray' : accept 'str' (UTF-8 encoded) and
    each other; an 'int' is *not* turned into zero bytes, nor
    an iterable of integers into a byte string. The three
    text types never reach their constructors, which accept
    almost anything.
  - 'bool' : accepts only numbers equal to '0' or '1', such
    as 'True', '0' or '1.0'. Anything else is refused without
    asking its '__eq__'.
  - 'int' : accepts 'float' if 'is_integer', real-valued
    integer 'complex', parseable 'str'.
  - 'float' : accepts 'int', real-valued 'complex',
    parseable 'str'.
  - 'complex' : accepts 'int', 'float', parseable 'str'.
  - 'list' / 'tuple' / 'set' / 'frozenset' : accept any
    other built-in container; 'dict' is converted via its
    '(key, value)' pairs.
  - 'dict' : accepts anything that splats with '{**arg}'.
  - 'type' : only succeeds if 'arg' is already a class.
  - a subclass of any target above that keeps the constructor
    of its builtin, such as 'class Name(str): pass' : 'arg' is
    held to the rule of that builtin, unless it is already an
    instance of it, and the subclass is built from the result,
    which must give an instance of the subclass. This is part of
    the cast, not the fallback below, so 'allowInstantiation'
    does not affect it.
  - a subclass with a constructor of its own, such as an
    'IntEnum' or 'collections.Counter', is trusted and treated
    as any other target below; see 'castRule'.
  - any other target : the target's constructor is called on
    'arg', and what it returns must be an instance of the
    target, though possibly of a subclass. Suppress this
    fallback with 'allowInstantiation=False'.

  Parameters
  ----------
  target : type
      The desired result type.
  arg : Any
      The value to cast.
  **kwargs
      allowInstantiation : bool, optional
          Whether to fall back to 'target(arg)' for non-special
          targets. Defaults to 'True'.

  Returns
  -------
  Any
      'arg' cast to 'target'.

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
  rule = castRule(target)
  if rule is target:
    return _castRuled(target, arg)
  if rule is not None:
    return _castSubclass(target, rule, arg)
  if kwargs.get('allowInstantiation', True):
    try:
      out = target(arg)
    except Exception as exception:
      raise _exc(target, arg) from exception
    else:
      #  A constructor may return anything at all, and only an instance
      #  of the target is a cast to it.
      if isinstance(out, target):
        return out
  raise _exc(target, arg)
