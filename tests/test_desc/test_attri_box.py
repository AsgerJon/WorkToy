"""
TestAttriBox tests specific functionality of the 'AttriBox' descriptor not
covered by the contextual tests in 'DescTest'.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
import sys

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException, MissingVariable
from . import DescTest
from .geometry import Circle, Point2D

eps = sys.float_info.epsilon


class TestAttriBox(DescTest):
  """
  TestAttriBox tests specific functionality of the 'AttriBox' descriptor not
  covered by the contextual tests in 'DescTest'.
  """

  def test_init(self) -> None:
    """
    Testing that 'AttriBox' descriptors actively instantiate when owning
    classes instantiate.
    """
    points = Point2D.rands(69, -0.1337, 80085)
    for point in points:
      self.assertIsInstance(point.x, float)
      self.assertIsInstance(point.y, float)
    circles = Circle.rands(69, -0.1337, 80085)
    for circle in circles:
      self.assertIsInstance(circle.radius, float)
      self.assertIsInstance(circle.center, Point2D)

  def test_good_set(self, ) -> None:
    """
    Testing setting functions as intended.
    """
    point2D = Point2D(69, 420)
    self.assertEqual(point2D.x, 69)
    self.assertEqual(point2D.y, 420)
    point2D.x = -1337
    point2D.y = 80085
    self.assertEqual(point2D.x, -1337)
    self.assertEqual(point2D.y, 80085)

  def test_bad_set(self, ) -> None:
    """
    Testing that setting to incompatible types raises appropriate errors.
    """
    point2D = Point2D(69, 420)
    self.assertEqual(point2D.x, 69)
    self.assertEqual(point2D.y, 420)

    def _1337() -> None:
      """Imma a float, trust me bro!"""
      pass

    with self.assertRaises(TypeException) as context:
      point2D.x = _1337() or _1337
    e = context.exception
    self.assertEqual(e.varName, 'value')
    self.assertEqual(e.actualObject, _1337)
    self.assertEqual(e.actualType, type(_1337))
    self.assertEqual(e.expectedTypes, (float,))

  def test_good_delete(self, ) -> None:
    """
    Testing that deleting attributes works as intended.
    """
    point2D = Point2D(69, 420)
    self.assertEqual(point2D.x, 69)
    self.assertEqual(point2D.y, 420)
    del point2D.x
    del point2D.y
    with self.assertRaises(MissingVariable) as context:
      _ = point2D.x
    e = context.exception
    self.assertIs(e.instance, point2D)
    self.assertEqual(e.varName, 'x')
    with self.assertRaises(MissingVariable) as context:
      _ = point2D.y
    e = context.exception
    self.assertIs(e.instance, point2D)
    self.assertEqual(e.varName, 'y')

  def test_bad_delete(self, ) -> None:
    """
    Testing that deleting attributes that are not set raises appropriate
    errors.
    """
    point2D = Point2D(69, 420)
    self.assertEqual(point2D.x, 69)
    self.assertEqual(point2D.y, 420)
    del point2D.x
    del point2D.y
    with self.assertRaises(MissingVariable) as context:
      del point2D.x
    e = context.exception
    self.assertIs(e.instance, point2D)
    self.assertEqual(e.varName, 'x')
    with self.assertRaises(MissingVariable) as context:
      del point2D.y
    e = context.exception
    self.assertIs(e.instance, point2D)
    self.assertEqual(e.varName, 'y')

  def test_gymnastics(self) -> None:
    """
    Covering certain edge cases.
    """

    class Bar:
      foo = AttriBox[int]()

    bar = Bar()
    Bar.foo.createContext(bar, Bar)
    try:
      with self.assertRaises(RecursionError):
        Bar.foo.__instance_get__(Bar(), Bar, _recursion=True)
      with self.assertRaises(RecursionError):
        Bar.foo.__instance_set__(Bar(), 'baz', _recursion=True)
    finally:
      Bar.foo.exitContext()

    class Spam:
      eggList = AttriBox[list](69, 420, 1337)
      eggSet = AttriBox[set](69, 420, 1337)
      eggFrozenset = AttriBox[frozenset](69, 420, 1337)
      eggTuple = AttriBox[tuple](69, 420, 1337)

    spam = Spam()
    for egg, num in zip(spam.eggList, [69, 420, 1337]):
      self.assertEqual(egg, num)
    for egg, num in zip(spam.eggTuple, [69, 420, 1337]):
      self.assertEqual(egg, num)

    for num in [69, 420, 1337]:
      self.assertIn(num, spam.eggSet)
      self.assertIn(num, spam.eggFrozenset)

    spam.eggTuple = 80085, 8008135, -8008135
    for egg, num in zip(spam.eggTuple, [80085, 8008135, -8008135]):
      self.assertEqual(egg, num)

  def test_set_tuple(self) -> None:
    """
    Testing setting an 'AttriBox' to a tuple, where the field type needs
    to have them unpacked.
    """

    class Foo:
      bar = AttriBox[complex]()

    foo = Foo()

    setattr(foo, 'bar', (69, 420))
    self.assertAlmostEqual(foo.bar.real, 69)
    self.assertAlmostEqual(foo.bar.imag, 420)

  def test_bad_field_type(self) -> None:
    """
    Testing exception when missing __field_type__.
    """

    susBox = AttriBox()
    with self.assertRaises(MissingVariable) as context:
      _ = susBox.fieldType
    e = context.exception
    self.assertIs(e.instance, susBox)
    self.assertEqual(e.varName, '__field_type__')
    self.assertIn(type, e.expectedTypes)

  def test_set_overflow_int(self) -> None:
    """
    Testing that assigning an int too large for the field type raises
    'OverflowError' rather than masking it with the constructor
    fallback. Stupid args, stupid prizes.
    """
    for box in [float, complex]:
      class Foo:
        # noinspection PyTypeHints
        bar = AttriBox[box](box(0))

      foo = Foo()
      with self.assertRaises(OverflowError):
        foo.bar = 2 ** 2000

  def test_set_exact_large_int(self) -> None:
    """
    Testing that assigning a large int the field type represents
    exactly still succeeds, so the overflow guard does not reject
    in-range values.
    """

    class Foo:
      bar = AttriBox[float](0.0)

    foo = Foo()
    foo.bar = 2 ** 100
    self.assertEqual(int(foo.bar), 2 ** 100)

  def test_set_lossy_scalar_raises(self) -> None:
    """
    Testing that assigning a value a numeric field type would only
    accept by losing data raises 'TypeException' rather than silently
    rounding through the constructor fallback.
    """
    cases = [
      (int, 3.9), (float, 2 ** 60 + 1), (complex, 2 ** 60 + 1),
      (bool, 2), (int, '3.9')
    ]
    for box, value in cases:
      class Foo:
        # noinspection PyTypeHints
        bar = AttriBox[box](box())

      foo = Foo()
      with self.assertRaises(TypeException):
        foo.bar = value

  def test_set_tuple_splat_survives(self) -> None:
    """
    Testing that the constructor fallback still serves the tuple-splat
    path for a numeric field type, so 'complex(re, im)' construction is
    not caught by the scalar guard.
    """

    class Foo:
      bar = AttriBox[complex]()

    foo = Foo()
    # noinspection PyTypeChecker
    foo.bar = 69, 420
    if TYPE_CHECKING:  # pragma: no cover
      assert isinstance(foo.bar, complex)
    self.assertAlmostEqual(foo.bar.real, 69)
    self.assertAlmostEqual(foo.bar.imag, 420)

  def test_bad_resolve(self) -> None:
    """
    This method covers the TypeError, ValueError branch in
    'AttriBox._resolve'.
    """

    class Wessel(complex):
      """
      Wessel is a subclass of 'complex' named after Caspar Wessel,
      who first represented complex numbers geometrically. The purpose of
      this subclass is to bypass a branch that specifically handles
      'complex'.
      """

    class Foo:
      bar = AttriBox[Wessel]()

    foo = Foo()
    with self.assertRaises(TypeException) as context:
      susValue = """some real ones, some imaginary ones, trust me bro!"""
      # noinspection PyTypeChecker
      foo.bar = susValue
    e = context.exception
    self.assertEqual(e.varName, 'value')
    self.assertEqual(e.actualObject, susValue)
    self.assertIs(e.actualType, str)
    self.assertIn(Wessel, e.expectedTypes)

  def test_this_builds_through_constructor(self) -> None:
    """
    Testing that a 'THIS' captured in the deferred default goes through
    the field-type constructor even when the owning instance is already
    an instance of the field type. The earlier passthrough returned the
    owner itself because 'isinstance(child, Parent)' held, which the
    sentinel guard now suppresses.
    """

    class Ancestor(BaseObject):
      """Ancestor can be built from any object, recording its origin."""

      source = AttriBox[object]()

      @overload(object)
      def __init__(self, source: object) -> None:
        self.source = source

      @overload()
      def __init__(self) -> None:
        pass

    class Heir(Ancestor):
      """Heir builds a separate 'Ancestor' from itself, not itself."""

      mom = AttriBox[Ancestor](THIS)
      dad = AttriBox[Ancestor](THIS)

    heir = Heir()
    self.assertIsNot(heir.mom, heir)
    self.assertIsInstance(heir.mom, Ancestor)
    self.assertIs(heir.mom.source, heir)
    #  Each box builds its own field, and the owner is never passed through
    self.assertIsNot(heir.mom, heir.dad)
    #  A second owner gets its own freshly built field
    other = Heir()
    self.assertIsNot(other.mom, heir.mom)
    self.assertIs(other.mom.source, other)

  def test_prebuilt_value_passes_through(self) -> None:
    """
    Testing that the passthrough survives for a genuine pre-built value.
    Without a sentinel in the deferred default, a lone argument already of
    the field type is stored unchanged rather than rebuilt.
    """

    class Ancestor(BaseObject):
      """Ancestor needs no arguments to build."""

      @overload()
      def __init__(self) -> None:
        pass

    seed = Ancestor()

    class Holder(BaseObject):
      """Holder captures an already-built 'Ancestor' as its default."""

      held = AttriBox[Ancestor](seed)

    holder = Holder()
    self.assertIs(holder.held, seed)

  def test_this_requires_compatible_constructor(self) -> None:
    """
    Testing that a 'THIS' default whose field type cannot accept the owner
    raises 'TypeException', chained from the underlying 'TypeError', rather
    than silently passing the owner through. A bare field type falls back
    to 'object.__init__', which rejects the extra argument.
    """

    class Plain:
      """Plain has no constructor that accepts an argument."""

    class Sub(Plain):
      """Sub captures itself as the default of an incompatible box."""

      parent = AttriBox[Plain](THIS)

    sub = Sub()
    with self.assertRaises(TypeException) as context:
      _ = sub.parent
    e = context.exception
    self.assertIs(e.expectedTypes[0], Plain)
    self.assertIsInstance(e.__cause__, TypeError)
