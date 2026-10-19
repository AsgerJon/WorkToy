"""
TestKeywordDispatch subclasses 'OverloadTest' and pins that a call with
keyword arguments dispatches by binding the keywords to the parameter
names of each registered function: a registration whose names and count
the call fills is a candidate, and among the candidates the best type
match wins, by exact type first, then 'isinstance', then the cast, in
registration order within each tier. Matching used to be positional
alone, so 'Point(x=69, y=420)' never reached '@overload(int, int)' and
the refusal showed an empty 'received' block.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import Dispatcher, overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException

from . import OverloadTest


class Point(BaseObject):
  """Point takes its coordinates as ints or as floats."""

  @overload(int, int)
  def __init__(self, x: int, y: int) -> None:
    self.kind, self.x, self.y = 'int', x, y

  @overload(float, float)
  def __init__(self, x: float, y: float) -> None:
    self.kind, self.x, self.y = 'float', x, y

  @overload(int)
  def area(self, side: int) -> str:
    return 'square %d' % side

  @overload(float)
  def area(self, radius: float) -> str:
    return 'circle %s' % radius

  @overload.flex(int, str)
  def tag(self, n: int, s: str) -> str:
    return '%s%d' % (s, n)

  @overload(int)
  def fill(self, n: int, **extra) -> tuple:
    return (n, sorted(extra))

  @overload(int)
  def scaled(self, n: int, factor: int = 2) -> int:
    return n * factor

  @overload.fallback
  def catch(self, *args, **kwargs) -> tuple:
    return (args, sorted(kwargs))


class Flags(BaseObject):
  """Flags registers the wider type first, so only the exact tier can
  choose the narrower one."""

  @overload(int, int)
  def pick(self, x: int, y: int) -> str:
    return 'int'

  @overload(bool, bool)
  def pick(self, x: bool, y: bool) -> str:
    return 'bool'


class TestKeywordDispatch(OverloadTest):
  """
  TestKeywordDispatch provides tests for dispatch on keyword arguments.
  """

  def test_keywords_bind_by_name(self) -> None:
    """Keywords in any order, and mixed with positionals, reach the
    overload whose parameter names they fill."""
    for point in (Point(x=69, y=420), Point(y=420, x=69), Point(69, y=420)):
      with self.subTest(point=point):
        self.assertEqual((point.kind, point.x, point.y), ('int', 69, 420))

  def test_best_type_wins(self) -> None:
    """Among registrations sharing the names, the exact type match wins,
    then 'isinstance', then the cast."""
    self.assertEqual(Point(x=1.5, y=2.5).kind, 'float')
    self.assertEqual(Point(x=1, y=2).kind, 'int')
    #  Neither exact nor isinstance: 1 casts to float, 2.5 not to int.
    self.assertEqual(Point(x=1, y=2.5).kind, 'float')

  def test_exact_tier_precedes_isinstance(self) -> None:
    """An exact type match wins over an earlier registration the call
    only matches through 'isinstance', so a 'bool' call reaches the
    'bool' overload registered after the 'int' one."""
    self.assertEqual(Flags().pick(x=True, y=False), 'bool')
    self.assertEqual(Flags().pick(x=1, y=0), 'int')

  def test_names_tell_registrations_apart(self) -> None:
    """Registrations of one name with different parameter names are
    chosen by the keyword given."""
    point = Point(0, 0)
    self.assertEqual(point.area(side=3), 'square 3')
    self.assertEqual(point.area(radius=2.0), 'circle 2.0')
    self.assertEqual(point.area(side=2.0), 'square 2')

  def test_flex_binds_canonical_names(self) -> None:
    """A 'flex' registration binds the names of the wrapped function."""
    self.assertEqual(Point(0, 0).tag(s='a', n=1), 'a1')
    self.assertEqual(Point(0, 0).tag(n=2, s='b'), 'b2')

  def test_extra_keywords(self) -> None:
    """Keywords beyond the signature pass through to a function taking
    them, by name or through '**kwargs', and refuse one that does not."""
    self.assertEqual(Point(0, 0).fill(n=1, a=2, b=3), (1, ['a', 'b']))
    self.assertEqual(Point(0, 0).scaled(n=3, factor=3), 9)
    self.assertEqual(Point(0, 0).scaled(n=3), 6)
    with self.assertRaises(DispatchException):
      Point(0, 0).area(side=1, extra=2)

  def test_unmatched_keywords(self) -> None:
    """A keyword naming no parameter, or a parameter left unfilled,
    misses, and the message names the keywords received."""
    with self.assertRaises(DispatchException) as context:
      Point(x=1, z=2)
    text = str(context.exception)
    self.assertIn('x', text)
    self.assertIn('z', text)
    self.assertEqual(context.exception.keyArgs, {'x': 1, 'z': 2})
    with self.assertRaises(DispatchException):
      Point(x=1)

  def test_fallback_gets_keywords(self) -> None:
    """The fallback receives the call as written."""
    self.assertEqual(Point(0, 0).catch(1, q=2), ((1,), ['q']))

  def test_positional_unchanged(self) -> None:
    """Positional calls dispatch as before."""
    self.assertEqual(Point(1, 2).kind, 'int')
    self.assertEqual(Point(1.0, 2.0).kind, 'float')
    self.assertEqual(Point(0, 0).area(3), 'square 3')

  def test_empty_blocks_say_none(self) -> None:
    """A refusal with nothing received, or nothing registered, prints
    '(none)' rather than an empty block."""

    class Bare(BaseObject):
      f = Dispatcher()

    with self.assertRaises(DispatchException) as context:
      Bare().f()
    text = str(context.exception)
    self.assertIn('(none)', text)
