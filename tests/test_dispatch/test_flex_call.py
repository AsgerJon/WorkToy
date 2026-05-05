"""
TestFlexCall provides tests for the 'flexCall' factory from
'worktoy.dispatch'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType
from typing import TYPE_CHECKING

# noinspection PyUnresolvedReferences
from worktoy.dispatch import flexCall, isFlex
from . import DispatcherTest
from worktoy.waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  # @formatter:off
  from typing import Callable
  from typing import Any
  class flexCall:  # noqa
    __name__: str
    __qualname__: str
    __module__: str
    __doc__: str
    __annotations__: dict[str, Any]
    __wrapped__: Callable
    def __call__(self, *args) -> Any: ...
    def __init__(self, func: Callable) -> None: print(func)
  class isFlex:  # noqa
    def __call__(self, func: Any) -> bool: ...
    def __init__(self, func: Any) -> None: print(func)
  # @formatter:on


#  ____________________________________________________________________
#  Module-level fixtures
#  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

def _binary(a, b) -> tuple[Any, Any]:
  """Standard two-arg function. minPos=2, maxPos=2."""
  return a, b


def _ternaryWithDefault(a, b, c=10) -> tuple[Any, Any, Any]:
  """One default. minPos=2, maxPos=3."""
  return a, b, c


def _zeroArg() -> str:
  """No positional args. minPos=0, maxPos=0."""
  return 'noop'


def _allDefaults(a=1, b=2, c=3) -> tuple[int, int, int]:
  """All defaulted. minPos=0, maxPos=3."""
  return a, b, c


def _kwOnlyTail(a, b, *, k) -> tuple[Any, Any, Any]:
  """Required kwarg-only after positionals. minPos=2, maxPos=2."""
  return a, b, k


def _varargs(*args) -> tuple:
  """CO_VARARGS short-circuit fixture; flexCall must return as-is."""
  return args


def _annotated(a: int, b: str) -> tuple[int, str]:
  """Used to verify annotations are copied to the wrapper."""
  return a, b


def _looksLikeDunder(a, b) -> tuple[Any, Any]:
  """Used to test the dunder short-circuit. __name__ is overridden
  after definition so we don't pollute module scope with a real
  dunder binding."""
  return a, b


_looksLikeDunder.__name__ = '__looks_like_dunder__'


class TestFlexCall(DispatcherTest):
  """Tests for flexCall(func): factory wrapping a FunctionType
  with truncating positional dispatch."""

  #  ================================================================
  #  |
  #  |                    VALIDATION OF HELPERS
  #  ================================================================

  def test_helpers(self, ) -> None:
    """Sanity check that the fixtures are what we expect."""
    self.assertEqual(_binary(1, 2), (1, 2))
    self.assertEqual(_ternaryWithDefault(1, 2), (1, 2, 10))
    self.assertEqual(_zeroArg(), 'noop')
    self.assertEqual(_allDefaults(), (1, 2, 3))
    self.assertEqual(_kwOnlyTail(1, 2, k='kw'), (1, 2, 'kw'))
    self.assertEqual(_varargs(1, 2, 3), (1, 2, 3))
    self.assertEqual(_annotated(42, 'string'), (42, 'string'))
    self.assertEqual(_looksLikeDunder(1, 2), (1, 2))
    self.assertIsInstance(isFlex, FunctionType)
    self.assertIsInstance(flexCall, FunctionType)

  #  ================================================================
  #  |
  #  |                         CONSTRUCTION
  #  ================================================================

  #  ________________________________________________________________
  #  Good construction — wrapping
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_wraps_normal_function(self) -> None:
    """A standard FunctionType produces a new wrapper distinct
    from the original."""
    self.assertFalse(isFlex(_binary))
    wrapped = flexCall(_binary)
    self.assertTrue(isFlex(wrapped))
    self.assertIsNot(wrapped, _binary)

  def test_wrapper_is_function_type(self) -> None:
    """The wrapper itself is a FunctionType, so it can re-enter
    the namespace as a regular function."""
    self.assertIsInstance(flexCall(_binary), FunctionType)

  def test_idempotent_rewrap_returns_same_object(self) -> None:
    """The _FLEX_MARKER short-circuit makes flexCall a no-op on
    already-wrapped functions."""
    once = flexCall(_binary)
    twice = flexCall(once)
    self.assertIs(twice, once)

  #  ________________________________________________________________
  #  Good construction — passthrough cases
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_varargs_function_passes_through(self) -> None:
    """A *args function makes flex truncation meaningless; the
    factory returns the function unchanged."""
    self.assertIs(flexCall(_varargs), _varargs)

  def test_dunder_function_passes_through(self) -> None:
    """A function whose __name__ looks like a dunder is returned
    unchanged; the factory leaves protocol-shaped callables alone."""
    self.assertIs(flexCall(_looksLikeDunder), _looksLikeDunder)

  #  ________________________________________________________________
  #  Bad construction — non-FunctionType
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_rejects_non_function_types(self) -> None:
    """Various non-FunctionType callables and non-callables all
    raise TypeException."""
    cases = [42, 'string', None, len, classmethod(_binary)]
    for bad in cases:
      with self.subTest(bad=type(bad).__name__):
        with self.assertRaises(TypeException):
          flexCall(bad)  # noqa

  def test_rejects_type_exception_attributes(self) -> None:
    """The TypeException carries the standard varName /
    actualObject / expectedTypes triple, matching the convention
    used elsewhere in worktoy."""
    with self.assertRaises(TypeException) as ctx:
      flexCall(42)  # noqa
    e = ctx.exception
    self.assertEqual(e.varName, 'func')
    self.assertEqual(e.actualObject, 42)
    self.assertIn(FunctionType, e.expectedTypes)

  #  ================================================================
  #  |
  #  |                         METADATA COPY
  #  ================================================================

  #  ________________________________________________________________
  #  Standard introspection attributes
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_preserves_name(self) -> None:
    self.assertEqual(flexCall(_binary).__name__, '_binary')

  def test_preserves_qualname(self) -> None:
    self.assertEqual(
      flexCall(_binary).__qualname__, _binary.__qualname__
    )

  def test_preserves_module(self) -> None:
    self.assertEqual(
      flexCall(_binary).__module__, _binary.__module__
    )

  def test_preserves_doc(self) -> None:
    self.assertEqual(flexCall(_binary).__doc__, _binary.__doc__)

  def test_preserves_annotations(self) -> None:
    self.assertEqual(
      flexCall(_annotated).__annotations__,
      _annotated.__annotations__,
    )

  #  ________________________________________________________________
  #  Wrapper-specific attributes
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_sets_wrapped_attribute(self) -> None:
    """__wrapped__ is the breadcrumb back to the original; used by
    inspect.unwrap and various debuggers."""
    wrapped = flexCall(_binary)
    self.assertIs(wrapped.__wrapped__, _binary)

  def test_sets_flex_marker(self) -> None:
    """The idempotency sentinel must be set, otherwise re-wrap
    detection would silently fail."""
    wrapped = flexCall(_binary)
    self.assertTrue(getattr(wrapped, '__flex_wrapped__', False))

  #  ================================================================
  #  |
  #  |                       WRAPPER BEHAVIOUR
  #  |              ( the actual point of the factory )
  #  ================================================================

  #  ________________________________________________________________
  #  Calling — exact arity
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_call_with_exact_args(self) -> None:
    self.assertEqual(flexCall(_binary)(1, 2), (1, 2))

  def test_call_zero_arg_function(self) -> None:
    self.assertEqual(flexCall(_zeroArg)(), 'noop')

  #  ________________________________________________________________
  #  Calling — truncation (n > maxPos)
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_call_with_extra_args_truncates(self) -> None:
    """Positional args beyond maxPos are silently dropped; the
    underlying function receives only the first maxPos."""
    self.assertEqual(flexCall(_binary)(1, 2, 3, 4, 5), (1, 2))

  def test_call_zero_arg_function_with_extras_truncates(self) -> None:
    """maxPos=0: all positionals are dropped."""
    self.assertEqual(flexCall(_zeroArg)(1, 2, 3), 'noop')

  #  ________________________________________________________________
  #  Calling — defaults (minPos < n <= maxPos)
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_call_uses_defaults_when_args_below_maxPos(self) -> None:
    """minPos=2, maxPos=3: passing only 2 args lets 'c' default."""
    self.assertEqual(flexCall(_ternaryWithDefault)(1, 2), (1, 2, 10))

  def test_call_overrides_defaults(self) -> None:
    self.assertEqual(
      flexCall(_ternaryWithDefault)(1, 2, 99), (1, 2, 99)
    )

  def test_call_all_defaults_with_zero_args(self) -> None:
    """minPos=0, all defaulted: zero args is a valid call."""
    self.assertEqual(flexCall(_allDefaults)(), (1, 2, 3))

  #  ________________________________________________________________
  #  Calling — too few args (n < minPos)
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_call_with_too_few_args_raises_type_error(self) -> None:
    with self.assertRaises(TypeError):
      flexCall(_binary)(1)

  def test_call_with_zero_args_when_min_is_two_raises(self) -> None:
    with self.assertRaises(TypeError):
      flexCall(_binary)()

  def test_too_few_args_message_names_the_function(self) -> None:
    """The error message must identify which function the caller
    underspecified, not just say 'a function somewhere'."""
    with self.assertRaises(TypeError) as ctx:
      flexCall(_binary)(1)
    self.assertIn('_binary', str(ctx.exception))

  def test_too_few_args_message_lists_missing_arg_names(self) -> None:
    """Missing positional arg names appear in the error so the
    caller can see exactly what was omitted."""
    with self.assertRaises(TypeError) as ctx:
      flexCall(_binary)(1)
    self.assertIn('b', str(ctx.exception))

  def test_too_few_args_message_includes_counts(self) -> None:
    with self.assertRaises(TypeError) as ctx:
      flexCall(_binary)()
    msg = str(ctx.exception)
    self.assertIn('2', msg)  # required count
    self.assertIn('0', msg)  # received count

  #  ________________________________________________________________
  #  Calling — kwargs passthrough
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_call_passes_kwargs_through(self) -> None:
    """Keyword args are forwarded unchanged."""
    self.assertEqual(
      flexCall(_kwOnlyTail)(1, 2, k='kw'), (1, 2, 'kw')  # noqa
    )

  def test_call_kwargs_combined_with_truncation(self) -> None:
    """Truncation of positional args does not affect kwargs."""
    self.assertEqual(
      flexCall(_kwOnlyTail)(1, 2, 3, 4, k='kw'), (1, 2, 'kw')  # noqa
    )

  def test_missing_kwonly_raises_native_typeerror(self) -> None:
    """Required kwarg-only args are not the wrapper's
    responsibility; the wrapped function raises naturally and
    the wrapper does not interfere."""
    with self.assertRaises(TypeError):
      flexCall(_kwOnlyTail)(1, 2)
