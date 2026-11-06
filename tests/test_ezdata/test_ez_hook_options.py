"""
TestEZHookOptions tests the build options 'EZHook' from 'worktoy.ezdata'
resolves from the class keywords.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZMeta
from worktoy.ezdata._ez_hook import _unorderable
from . import EzdataTest, Point2D, Circle, Version, Vector, FrozenVector


class TestEZHookOptions(EzdataTest):
  """
  A dataclass is declared frozen, ordered or keyword-only by class
  keyword, under any of the accepted synonyms. A frozen class hashes
  and refuses assignment, an ordered one compares, and a class based
  on a frozen one must be frozen itself. The tests pin the synonyms,
  the flags on the class, the thawing refusal, the unorderable
  comparison and the names the generated methods carry.
  """

  def test_defaults(self) -> None:
    self.assertFalse(Point2D.isFrozen)
    self.assertFalse(Point2D.isOrdered)
    self.assertFalse(Point2D.kwOnly)
    self.assertFalse(Point2D.__is_frozen__)
    self.assertFalse(Point2D.__is_ordered__)
    self.assertFalse(Point2D.__kw_only__)
    self.assertIsNone(Point2D.__hash__)
    with self.assertRaises(TypeError):
      hash(Point2D())

  def test_synonyms(self) -> None:
    frozenKeys = ('frozen', 'immutable', 'hashable')
    orderedKeys = ('ordered', 'order', 'sortable', 'comparable')
    kwOnlyKeys = ('kwOnly', 'keywordOnly', 'kw_only')
    for key in frozenKeys:
      with self.subTest(key=key):
        cls = EZMeta('F', (EZData,), {'x': 1}, **{key: True})
        self.assertTrue(cls.isFrozen)
        self.assertFalse(cls.isOrdered)
        self.assertFalse(cls.kwOnly)
    for key in orderedKeys:
      with self.subTest(key=key):
        cls = EZMeta('O', (EZData,), {'x': 1}, **{key: 1})
        self.assertTrue(cls.isOrdered)
        self.assertIs(cls.__is_ordered__, True)
    for key in kwOnlyKeys:
      with self.subTest(key=key):
        cls = EZMeta('K', (EZData,), {'x': 1}, **{key: 'yes'})
        self.assertTrue(cls.kwOnly)
        self.assertIs(cls.__kw_only__, True)
    falsy = EZMeta('Z', (EZData,), {'x': 1}, frozen=0, ordered=(), kwOnly='')
    self.assertFalse(falsy.isFrozen)
    self.assertFalse(falsy.isOrdered)
    self.assertFalse(falsy.kwOnly)

  def test_frozen_class(self) -> None:
    self.assertTrue(Circle.isFrozen)
    self.assertTrue(Circle.kwOnly)
    self.assertTrue(FrozenVector.isFrozen)
    self.assertEqual(hash(FrozenVector(1, 2)), hash((1.0, 2.0)))
    self.assertEqual({FrozenVector(1, 2): 'v'}[FrozenVector(1.0, 2.0)], 'v')
    #  A frozen class hashes its values, and the centre is a 'Point2D'.
    with self.assertRaises(TypeError):
      hash(Circle(radius=2.0))

  def test_thawing_refused(self) -> None:
    with self.assertRaises(TypeError) as context:
      class Thawed(Circle):
        """A class based on a frozen class must be frozen too."""

    self.assertIn("'Thawed' is based on the frozen class 'Circle' and "
                  "does not declare 'frozen=True' itself",
                  str(context.exception))

    class Still(Circle, frozen=True):
      depth = 0.0

    self.assertTrue(Still.isFrozen)
    self.assertEqual(Still(depth=1.0).depth, 1.0)
    self.assertFalse(Vector.isFrozen)
    self.assertTrue(FrozenVector.isFrozen)

  def test_ordered_class(self) -> None:
    self.assertTrue(Version.isOrdered)
    self.assertLess(Version(1, 2), Version(1, 3))
    self.assertLessEqual(Version(1, 2), Version(1, 2))
    self.assertGreater(Version(2, 0), Version(1, 9))
    self.assertGreaterEqual(Version(2, 0), Version(2, 0))
    self.assertFalse(Version(1, 2) < Version(1, 2))
    self.assertEqual(Version.__lt__.__name__, '__lt__')
    self.assertEqual(Version.__ge__.__qualname__, 'Version.__ge__')
    self.assertIs(Version.__lt__(Version(), 5), NotImplemented)
    with self.assertRaises(TypeError):
      _ = Version() < 5

  def test_unordered_class(self) -> None:
    for name in ('__lt__', '__le__', '__gt__', '__ge__'):
      with self.subTest(name=name):
        self.assertIs(getattr(Point2D, name), _unorderable)
    self.assertIs(_unorderable(1, 2), NotImplemented)
    with self.assertRaises(TypeError):
      _ = Point2D() < Point2D()

    class Unordered(Version, ordered=False):
      patch = 0

    self.assertFalse(Unordered.isOrdered)
    self.assertIs(Unordered.__lt__, _unorderable)
    with self.assertRaises(TypeError):
      _ = Unordered(1, 2, 3) < Unordered(1, 2, 4)

  def test_ordered_is_inherited(self) -> None:
    class Patched(Version):
      patch = 0

    class Tagged(Patched):
      tag = ''

    class Plain(Point2D):
      z = 0.0

    self.assertTrue(Patched.isOrdered)
    self.assertTrue(Tagged.isOrdered)
    self.assertFalse(Plain.isOrdered)
    self.assertIsNot(Patched.__lt__, _unorderable)
    self.assertIsNot(Patched.__lt__, Version.__lt__)
    self.assertTrue(Patched(1, 2, 3) < Patched(1, 2, 4))
    self.assertTrue(Tagged(1, 2, 0, 'a') < Tagged(1, 2, 0, 'b'))
    self.assertFalse(Patched(1, 2, 4) < Patched(1, 2, 3))
    with self.assertRaises(TypeError):
      _ = Plain() < Plain()

  def test_generated_methods_named_after_the_class(self) -> None:
    self.assertEqual(Point2D.asDict.__qualname__, 'Point2D.asDict')
    self.assertEqual(Point2D.__init__.__qualname__, 'Point2D.__init__')
    self.assertEqual(Point2D.__lt__.__qualname__, '_unorderable')
    self.assertIsInstance(Point2D.__match_args__, tuple)

    class Local(EZData):
      x = 1

    method = 'test_generated_methods_named_after_the_class'
    expected = 'TestEZHookOptions.%s' % method
    self.assertEqual(Local.asTuple.__qualname__,
                     '%s.<locals>.Local.asTuple' % expected)
    byCall = EZMeta('ByCall', (EZData,), {'x': 1})
    self.assertEqual(byCall.asDict.__qualname__, 'ByCall.asDict')
    self.assertEqual(byCall.__init__.__qualname__, 'ByCall.__init__')
    self.assertNotIn('__qualname__', byCall.__namespace__)

  def test_generated_names_recorded(self) -> None:
    expected = frozenset((
      '__field_pairs__', 'asDict', 'asTuple', 'replace', '__repr__',
      '__str__', '__match_args__',
    ))
    self.assertEqual(Point2D.__ez_generated__, expected)

  def test_random_versions(self) -> None:
    self.randomInteger.size = 6
    numbers = self.randomInteger.row
    versions = [Version(n, m) for n, m in zip(numbers, reversed(numbers))]
    ordered = sorted(versions)
    for earlier, later in zip(ordered, ordered[1:]):
      with self.subTest(earlier=str(earlier), later=str(later)):
        self.assertLessEqual(earlier, later)
        self.assertLessEqual(earlier.asTuple(), later.asTuple())

  def test_plain_mixin_ahead_of_frozen_and_ordered_bases(self) -> None:
    class Mixin:
      tag = 'mixin'

    with self.assertRaises(TypeError) as context:
      class Thawed(Mixin, FrozenVector):
        """Refused as the class is compiled, after the body ran."""

    self.assertIn("'Thawed' is based on the frozen class 'FrozenVector' "
                  "and does not declare 'frozen=True' itself",
                  str(context.exception))
    class Sub(Mixin, Version):
      pass

    self.assertTrue(Sub.isOrdered)
    self.assertTrue(Sub(1, 2) < Sub(1, 3))
