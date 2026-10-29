"""
The 'typeCast' function casts a value to a target type, refusing every
lossy or implicit conversion.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Optional


def _exc(target: type, arg: Any) -> Exception:
  """Build a 'TypeCastException'.

  The import is deferred so 'utilities' does not pull in
  'waitaminute' at module load time.
  """
  from worktoy.waitaminute.dispatch import TypeCastException
  return TypeCastException(target, arg)


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
  raise _exc(complex, arg)


#  The two closed families. Within each, the builtins convert among
#  themselves without loss; outside them, only '__cast_as__' converts.
_NUMBERS = (bool, int, float, complex)
_TEXT = (str, bytes, bytearray)
_FAMILIES = (*_NUMBERS, *_TEXT)
_HANDLERS = (
  (str, _castStr),
  (bytes, _castBytes),
  (bytearray, _castByteArray),
  (bool, _castBool),
  (int, _castInt),
  (float, _castFloat),
  (complex, _castComplex),
)


def _familyHandler(target: type) -> Optional[Callable[[Any], Any]]:
  """The converter of 'target' when it is one of the family builtins
  itself, else None. Compared by identity: a subclass of a builtin is
  not the builtin, and casts only through '__cast_as__'."""
  for builtin, handler in _HANDLERS:
    if target is builtin:
      return handler
  return None


def _findCastHook(target: type) -> Optional[Callable[[Any], Any]]:
  """The '__cast_as__' of 'target' bound to it, or None when no class
  along its resolution order defines one. The hook must be a classmethod,
  since it is called on the class to make an instance; one defined as a
  plain function or a staticmethod raises 'UnboundCastHook' here, where
  it would otherwise run with the value bound as 'self' or fail one frame
  deeper with a misleading 'TypeError'."""
  for klass in getattr(target, '__mro__', ()):
    hook = vars(klass).get('__cast_as__', None)
    if hook is None:
      continue
    if isinstance(hook, classmethod):
      return getattr(target, '__cast_as__')
    from worktoy.waitaminute.dispatch import UnboundCastHook
    raise UnboundCastHook(klass.__name__, target.__name__)
  return None


def hasCastRule(target: type) -> bool:
  """
  The 'hasCastRule' function reports whether 'typeCast' decides for
  'target': a family builtin, a subclass of one, which is refused until it
  declares '__cast_as__', or any class declaring '__cast_as__'.

  Parameters
  ----------
  target : type
      The type a value would be cast to.

  Returns
  -------
  bool
      Whether 'typeCast' has a rule for 'target'.

  Raises
  ------
  UnboundCastHook
      If 'target' defines '__cast_as__' without '@classmethod'.
  """
  if _familyHandler(target) is not None:
    return True
  if isinstance(target, type) and issubclass(target, _FAMILIES):
    return True
  return _findCastHook(target) is not None


def typeCast(target: type, arg: Any) -> Any:
  """
  Cast 'arg' to 'target', or raise 'TypeCastException'. This is the one
  authority on conversion in 'worktoy': the boxes, the overload dispatch
  and the rest of the library ask it the same way.

  A value already an instance of 'target' is returned as it is, a 'bool'
  for an 'int' target included. Otherwise two closed families of
  builtins convert within themselves without loss, and nothing else
  converts unless the target itself says how:

  - Numbers: 'bool', 'int', 'float' and 'complex'. An 'int' is cast from
    an integral 'float' or a real integral 'complex'; a 'float' from an
    'int' it represents exactly or from a real 'complex'; a 'complex'
    from an 'int' a float holds exactly or from a 'float'; a 'bool' from
    a number equal to 0 or 1, without asking the '__eq__' of anything
    that is not a number. An 'int' too large for a 'float' is refused
    with the 'OverflowError' chained. No string is ever parsed.
  - Text: 'str', 'bytes' and 'bytearray' convert among the three as
    UTF-8, with undecodable bytes and unencodable text refused. Nothing
    else becomes text, since 'str(x)' never fails and 'bytes(5)' is five
    zero bytes.
  - Any other class, a subclass of a family builtin included, converts
    only through a classmethod '__cast_as__(cls, value)' of its own,
    consulted when 'value' is not already an instance. It returns an
    instance of 'cls', or 'NotImplemented' to refuse; any other result
    is refused here, so a field or an overload never receives a foreign
    object. A hook may lean on the families:

        class Count(int):
          @classmethod
          def __cast_as__(cls, value):
            return cls(typeCast(int, value))

    Bound to 'cls', the hook builds a subclass when looked up on one. A
    '__cast_as__' that is not a classmethod raises 'UnboundCastHook'.

  No constructor is ever called on 'arg'. Containers, 'slice', 'type' and
  every class without the hook accept their own instances and nothing
  else.

  Parameters
  ----------
  target : type
      The desired result type.
  arg : Any
      The value to cast.

  Returns
  -------
  Any
      'arg' itself, or an instance of 'target' made from it.

  Raises
  ------
  TypeCastException
      If 'arg' is no instance of 'target' and no rule converts it.
  UnboundCastHook
      If 'target' defines '__cast_as__' without '@classmethod'.

  Examples
  --------
  >>> typeCast(int, 3.0)
  3
  >>> typeCast(str, b'hello')
  'hello'
  >>> typeCast(int, True)
  True
  """
  if isinstance(arg, target):
    return arg
  handler = _familyHandler(target)
  if handler is not None:
    return handler(arg)
  hook = _findCastHook(target)
  if hook is None:
    raise _exc(target, arg)
  out = hook(arg)
  if out is NotImplemented or not isinstance(out, target):
    raise _exc(target, arg)
  return out
