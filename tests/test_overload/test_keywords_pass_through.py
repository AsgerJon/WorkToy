"""
TestKeywordsPassThrough subclasses 'OverloadTest' and pins that a call
dispatches on the types of its positional arguments alone, and that its
keyword arguments pass through unchanged to the function the positional
types select. A call with no positional arguments selects the empty
signature, '@overload()', so a class that takes keywords declares that
overload and handles them there, forwarding from its other overloads
with 'if kwargs: self.__init__(**kwargs)'. A keyword the selected function
does not take is refused by that function with its own 'TypeError'. A
call no signature accepts goes to the fallback, else 'DispatchException',
which still lists the keywords received.

The dispatcher used to bind keywords to the parameter names of each
registration, so 'Point(x=69, y=420)' reached '@overload(int, int)' on its
own; that binder is gone, and with it the rules it needed.

Keywords named 'instance' and 'func' pass through as well. The compiled
function and the wrapper of a 'flex' registration used to name their
leading parameters so, and a call passing either keyword failed with
'got multiple values for argument'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import Dispatcher, overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException

from . import OverloadTest


class Point(BaseObject):
  """Point declares the empty signature for keyword calls."""

  @overload(int, int)
  def __init__(self, x: int, y: int) -> None:
    self.kind, self.x, self.y = 'int', x, y

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.kind, self.x, self.y = 'float', x, y

  @overload(int)
  def __init__(self, x: int, **kwargs) -> None:
    self.kind, self.x, self.kwargs = 'int-kw', x, kwargs

  @overload()
  def __init__(self, **kwargs) -> None:
    self.kind, self.kwargs = 'kw', kwargs

  @overload(int)
  def fill(self, n: int, **extra) -> tuple:
    return (n, sorted(extra))

  @overload.flex(int, str)
  def tag(self, n: int, s: str, **extra) -> str:
    return '%s%d%s' % (s, n, ''.join(sorted(extra)))

  @overload(int)
  @overload(str)
  def f(self, x: object) -> tuple:
    return ('f', x)

  @overload()
  def f(self, **kwargs) -> tuple:
    return ('kw', kwargs)

  @overload.fallback
  def catch(self, *args, **kwargs) -> tuple:
    return (args, sorted(kwargs))


class Strict(BaseObject):
  """Strict declares no empty signature and no fallback."""

  @overload(int, int)
  def __init__(self, x: int, y: int) -> None:
    self.x, self.y = x, y


class Sampled(BaseObject):
  """Sampled uses the forwarding pattern of the 'work_test' samplers."""

  @overload(int, int)
  def __init__(self, lo: int, hi: int, **kwargs) -> None:
    self.lo, self.hi = lo, hi
    if kwargs:
      self.__init__(**kwargs)

  @overload()
  def __init__(self, **kwargs) -> None:
    for key, value in kwargs.items():
      setattr(self, key, value)


class TestKeywordsPassThrough(OverloadTest):
  """
  TestKeywordsPassThrough provides tests for keyword arguments passing
  through positional dispatch.
  """

  def test_positional_unchanged(self) -> None:
    """Positional calls dispatch as before."""
    self.assertEqual(Point(1, 2).kind, 'int')
    self.assertEqual(Point(1.0, 2.0).kind, 'float')
    self.assertEqual(Point(0, 0).fill(1), (1, []))
    self.assertEqual(Point(0, 0).f(5), ('f', 5))
    self.assertEqual(Point(0, 0).f('s'), ('f', 's'))

  def test_keywords_ride_along(self) -> None:
    """Keywords reach the function the positional types select, a 'flex'
    registration included."""
    self.assertEqual(Point(0, 0).fill(1, a=2, b=3), (1, ['a', 'b']))
    self.assertEqual(Point(0, 0).tag(1, 'a', k=1), 'a1k')
    self.assertEqual(Point(0, 0).tag('a', 1, k=1), 'a1k')

  def test_positional_types_select_the_overload(self) -> None:
    """A keyword never changes which signature the call matches: one
    positional 'int' selects '@overload(int)', whatever the keyword."""
    point = Point(69, y=420)
    self.assertEqual((point.kind, point.x, point.kwargs), ('int-kw', 69, {'y': 420}))

  def test_keywords_alone_select_the_empty_signature(self) -> None:
    """A call of keywords only has the empty signature."""
    for point in (Point(x=69, y=420), Point(y=420, x=69)):
      with self.subTest(point=point):
        self.assertEqual(point.kind, 'kw')
        self.assertEqual(point.kwargs, {'x': 69, 'y': 420})

  def test_stacked_signatures_take_keywords_alike(self) -> None:
    """A function stacked under several signatures is reached by keyword
    through the empty signature, whatever the keyword's type."""
    self.assertEqual(Point(0, 0).f(x=5), ('kw', {'x': 5}))
    self.assertEqual(Point(0, 0).f(x='s'), ('kw', {'x': 's'}))

  def test_forwarding_pattern(self) -> None:
    """An overload forwards the keywords it received to the empty
    signature, which applies them. A keyword naming a parameter the call
    already filled by position is Python's own error, not the
    dispatcher's."""
    sampled = Sampled(1, 2, step=5)
    self.assertEqual((sampled.lo, sampled.hi, sampled.step), (1, 2, 5))
    self.assertEqual(Sampled(lo=3).lo, 3)
    with self.assertRaises(TypeError) as context:
      Sampled(1, 2, hi=5)
    self.assertNotIsInstance(context.exception, DispatchException)

  def test_refused_without_empty_signature(self) -> None:
    """With no empty signature and no fallback, a keyword-only call and a
    call whose positional types match nothing are refused, and the message
    names the keywords received."""
    with self.assertRaises(DispatchException) as context:
      Strict(x=1, y=2)
    text = str(context.exception)
    self.assertIn('x', text)
    self.assertIn('y', text)
    self.assertEqual(context.exception.keyArgs, {'x': 1, 'y': 2})
    with self.assertRaises(DispatchException):
      Strict(1, y=2)

  def test_unexpected_keyword_is_the_functions_own_error(self) -> None:
    """A keyword the selected function does not take is refused by the
    function itself, not by the dispatcher."""
    with self.assertRaises(TypeError) as context:
      Strict(1, 2, z=3)
    self.assertNotIsInstance(context.exception, DispatchException)
    self.assertIn('z', str(context.exception))

  def test_flex_takes_no_keywords_by_name(self) -> None:
    """A 'flex' registration is selected by positional types only."""
    with self.assertRaises(DispatchException):
      Point(0, 0).tag(s='a', n=1)

  def test_fallback_gets_keywords(self) -> None:
    """The fallback receives the call as written."""
    self.assertEqual(Point(0, 0).catch(1, q=2), ((1,), ['q']))

  def test_keywords_named_like_the_dispatcher(self) -> None:
    """Keywords named 'instance' and 'func' pass through like any other.
    The compiled function takes the instance, and the wrapper of a 'flex'
    registration its function, by position without naming them, so no
    keyword collides with a parameter of theirs."""
    self.assertEqual(Point(0, 0).fill(1, instance=2), (1, ['instance']))
    self.assertEqual(Point(0, 0).fill(1, func=2), (1, ['func']))
    self.assertEqual(Point(0, 0).tag(1, 'a', func=1), 'a1func')
    self.assertEqual(Point(0, 0).tag('a', 1, instance=1), 'a1instance')
    point = Point(instance=69)
    self.assertEqual((point.kind, point.kwargs), ('kw', {'instance': 69}))

  def test_class_level_call_needs_the_instance(self) -> None:
    """Called through the class with no arguments, the compiled function
    refuses as the function of a plain method does, naming 'self'."""
    with self.assertRaises(TypeError) as context:
      Point.fill()
    self.assertNotIsInstance(context.exception, DispatchException)
    self.assertIn("'self'", str(context.exception))

  def test_empty_blocks_say_none(self) -> None:
    """A refusal with nothing received, or nothing registered, prints
    '(none)' rather than an empty block."""

    class Bare(BaseObject):
      f = Dispatcher()

    with self.assertRaises(DispatchException) as context:
      Bare().f()
    text = str(context.exception)
    self.assertIn('(none)', text)
