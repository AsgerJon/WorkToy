"""
TestCallMeMaybe subclasses 'DispatcherTest' from 'tests.test_dispatch' and
provides tests for the 'CallMeMaybe' class from 'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func
from typing import TYPE_CHECKING

from . import DispatcherTest
from worktoy.dispatch import CallMeMaybe
from worktoy.dispatch._call_me_maybe import _Wrapped  # noqa
from worktoy.waitaminute import TypeException, MissingVariable

if TYPE_CHECKING:  # pragma: no cover
  # @formatter:off
  from typing import Any, Callable, Optional
  class CallMeMaybe:  # noqa
    __function_case__: Optional[tuple[Callable]]
    __wrapped__: _Wrapped
    # noinspection PyUnusedLocal
    def __init__(self, func: Optional[Callable] = None) -> None: ...
    def setFunction(self, func: Callable) -> None: ...
    def invoke(self, func: Callable, *args, **kwargs) -> Any: ...
    def __call__(self, *args, **kwargs) -> Any: ...
    def __set_name__(self, owner: type, name: str) -> None: ...
  # @formatter:on


def _no_args() -> str:
  return 'no_args'


def _one_arg(x: Any) -> Any:
  return x


def _two_args(a: Any, b: Any) -> Any:
  return a, b


def _with_kwargs(a: Any, *, k: Any = None) -> Any:
  return a, k


def _varargs(*args: Any, **kwargs: Any) -> Any:
  return args, kwargs


class _CallableObject:
  """A callable that is not a FunctionType."""

  def __call__(self, x: Any) -> Any:
    return 'callable_object', x


class TestCallMeMaybe(DispatcherTest):
  """CallMeMaybe construction and forwarding."""

  #  ________________________________________________________________
  #  Good construction
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_init_empty(self) -> None:
    """No-arg construction leaves the function unset."""
    c = CallMeMaybe()
    self.assertIsNone(c.__function_case__)

  def test_init_with_function(self) -> None:
    c = CallMeMaybe(_one_arg)
    self.assertIs(c.__wrapped__, _one_arg)

  def test_init_with_none_explicit(self) -> None:
    """Passing None explicitly is the same as passing nothing."""
    c = CallMeMaybe(None)
    self.assertIsNone(c.__function_case__)

  def test_init_accepts_lambda(self) -> None:
    """Lambdas are FunctionType; they should work."""
    c = CallMeMaybe(lambda x: x * 2)
    self.assertEqual(c(21), 42)

  #  ________________________________________________________________
  #  Bad construction
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_init_rejects_non_callable(self) -> None:
    with self.assertRaises(TypeException):
      # noinspection PyTypeChecker
      CallMeMaybe(42)

  def test_init_accepts_callable_non_function(self) -> None:
    """CallMeMaybe accepts any callable, not just FunctionType.
    Subclasses (FlexCall) narrow back to FunctionType where they need
    __code__ introspection."""
    c = CallMeMaybe(_CallableObject())
    self.assertEqual(c('test'), ('callable_object', 'test'))

  #  ________________________________________________________________
  #  The tuple-wrapping defense
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_wrapped_function_is_not_bound(self) -> None:
    """The whole point of __function_case__ being a tuple: stored function
    must NOT be bound as a method when retrieved from the instance. If
    the descriptor protocol fired, calling would prepend `c` and the
    function would receive two args instead of one."""
    c = CallMeMaybe(_one_arg)
    self.assertEqual(c('hello'), 'hello')

  def test_function_case_is_tuple(self) -> None:
    """Internal representation is a one-tuple, not a bare function."""
    c = CallMeMaybe(_one_arg)
    self.assertIsInstance(c.__function_case__, tuple)
    self.assertEqual(len(c.__function_case__), 1)
    self.assertIs(c.__function_case__[0], _one_arg)

  #  ________________________________________________________________
  #  __call__ forwarding
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_call_forwards_no_args(self) -> None:
    c = CallMeMaybe(_no_args)
    self.assertEqual(c(), 'no_args')

  def test_call_forwards_positional(self) -> None:
    c = CallMeMaybe(_two_args)
    self.assertEqual(c(1, 2), (1, 2))

  def test_call_forwards_kwargs(self) -> None:
    c = CallMeMaybe(_with_kwargs)
    self.assertEqual(c('a', k='b'), ('a', 'b'))

  def test_call_forwards_varargs(self) -> None:
    c = CallMeMaybe(_varargs)
    self.assertEqual(c(1, 2, 3, x='y'), ((1, 2, 3), {'x': 'y'}))

  def test_call_raises_when_function_unset(self) -> None:
    c = CallMeMaybe()
    with self.assertRaises(MissingVariable):
      c()

  def test_call_propagates_exceptions(self) -> None:
    """Exceptions from the wrapped function bubble up unchanged."""

    def boom() -> None:
      raise RuntimeError('boom')

    c = CallMeMaybe(boom)
    with self.assertRaises(RuntimeError):
      c()

  def test_invoke_is_default_passthrough(self) -> None:
    """The default invoke() forwards args verbatim - subclasses override."""
    c = CallMeMaybe(_two_args)
    self.assertEqual(c.invoke(_two_args, 1, 2), (1, 2))

  #  ________________________________________________________________
  #  Descriptor refusal
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_set_name_raises(self) -> None:
    """
    Using CallMeMaybe as a class attribute must raise at class
    creation. CallMeMaybe is deliberately not a descriptor; subclasses
    that need descriptor behavior must override __set_name__.

    Notes about the error type:
    Please note the ambiguity in the error type. On Python 3.7 through
    3.11, any exception raised inside '__set_name__' is wrapped and
    propagated as a 'RuntimeError', with the original exception
    attached as both '__cause__' and '__context__'. From Python 3.12
    onward, the original exception propagates unchanged. Tests that
    exercise '__set_name__' failure paths therefore accept both the
    expected exception type and 'RuntimeError'.
    """
    with self.assertRaises((TypeError, RuntimeError)):
      class _Owner:  # noqa
        bound = CallMeMaybe(_one_arg)

  #  ________________________________________________________________
  #  Good _Wrapped behaviour
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_wrapped_descriptor_class_access(self) -> None:
    """Accessing '__wrapped__' on the class itself yields the descriptor,
    not a function. This is the 'instance is None' branch of
    _Wrapped.__get__."""
    desc = CallMeMaybe.__wrapped__
    self.assertTrue(hasattr(desc, '__get__'))
    self.assertNotIsInstance(desc, Func)

  #  ________________________________________________________________
  #  Bad _Wrapped behaviour
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_wrapped_raises_when_function_unset(self) -> None:
    """Accessing '__wrapped__' on an instance with no function set raises
    MissingVariable via _getWrappedFunction."""
    c = CallMeMaybe()
    with self.assertRaises(MissingVariable) as context:
      _ = c.__wrapped__
    e = context.exception
    self.assertIs(e.instance, c)
    self.assertEqual(e.varName, '__function_case__')
    self.assertIn(tuple, e.expectedTypes)

  def test_missing_private_key(self, ) -> None:
    """
    This method tests the error handling when '__private_key__' is missing.
    """

    class Foo:
      bar = _Wrapped(None)  # noqa

    foo = Foo()
    with self.assertRaises(MissingVariable) as context:
      _ = foo.bar
    e = context.exception
    self.assertIs(e.instance, Foo.bar)
    self.assertEqual(e.varName, '__private_key__')
    self.assertIn(str, e.expectedTypes)

  def test_badly_typed_private_key(self, ) -> None:
    """
    This method tests the error handling when '__private_key__' is not a
    string.
    """

    class Foo:
      bar = _Wrapped(("""I'm a key, trust me bro!""",))  # noqa

    foo = Foo()
    with self.assertRaises(TypeException) as context:
      _ = foo.bar
    e = context.exception
    self.assertEqual(e.varName, '__private_key__')
    self.assertEqual(e.actualObject, ("""I'm a key, trust me bro!""",))
    self.assertIs(e.actualType, tuple)
    self.assertIn(str, e.expectedTypes)

  def test_badly_typed_func_tuple(self, ) -> None:
    """
    This method tests the error handling when the retrieved 'funcTuple' is
    not a tuple.
    """

    susTuple = """Yeah bro, I totally got your funcs..."""

    class Foo:
      trolololo = susTuple  # noqa
      bar = _Wrapped('trolololo')

    foo = Foo()
    with self.assertRaises(TypeException) as context:
      _ = foo.bar
    e = context.exception
    self.assertEqual(e.varName, 'funcTuple')
    self.assertEqual(e.actualObject, susTuple)
    self.assertIs(e.actualType, str)
    self.assertIn(tuple, e.expectedTypes)

  #  ________________________________________________________________
  #  Attribute passthrough CallMeMaybe to the wrapped function
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_passthrough_attributes(self) -> None:
    """CallMeMaybe should pass through attribute access to the wrapped
    function, so that introspection on the instance reveals the wrapped
    function's attributes."""

    def foo(*_, ) -> None:
      pass

    hereIsMyNumber = foo() or CallMeMaybe(foo)  # noqa
    actualCode = hereIsMyNumber.__code__  # noqa
    expectedCode = hereIsMyNumber.__wrapped__.__code__  # noqa
    self.assertIs(actualCode, expectedCode)

  #  ________________________________________________________________
  #  Preservation of expected 'AttributeError' through __getattr__
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_attribute_error_propagates_through_getattr(self) -> None:
    """
    This method tests that the '__getattr__' correctly falls back to the
    normal 'AttributeError' when '__getattr__' fails to find a fallback.
    """

    def foo(*_, ) -> None:
      pass

    hereIsMyNumber = foo() or CallMeMaybe(foo)  # noqa
    with self.assertRaises(AttributeError):
      _ = getattr(hereIsMyNumber, 'thisIsCrazy')
