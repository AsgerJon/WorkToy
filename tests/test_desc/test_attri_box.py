"""
TestAttriBox tests specific functionality of the 'AttriBox' descriptor not
covered by the contextual tests in 'DescTest'.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar
import sys

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.desc._attri_box import _RootAlias  # noqa
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException, MissingVariable
from worktoy.waitaminute.desc import PhantomBoxError
from . import DescTest
from .geometry import Circle, Point2D

eps = sys.float_info.epsilon

T = TypeVar('T')

if TYPE_CHECKING:  # pragma: no cover
  from typing import Optional


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

  @staticmethod
  def _raisingFrames(exception: BaseException) -> list:
    """
    Return the function names along an exception's traceback, outermost
    first.

    Several guards in this file exist to fail early rather than to
    change what is raised, so the exception alone cannot distinguish
    them from the deeper failure they pre-empt. The frame list can.
    """
    out = []
    tb = exception.__traceback__
    while tb is not None:
      out.append(tb.tb_frame.f_code.co_name)
      tb = tb.tb_next
    return out

  def test_unsubscripted_box_declaration(self) -> None:
    """
    Testing that a box which never captured a field type is refused as
    the class is created, rather than at the first read of it.

    Nothing can rescue such a box afterwards, since '__class_getitem__'
    is the only place a field type is ever assigned, so the declaration
    itself is already the whole mistake. The bare form covers a box
    built with no subscript at all, and the parametrized-generic form
    covers a subscript that 'AttriBox[T]' declined to claim, whose alias
    then built a box with the field type still unset.

    The generic case spells the subscript as 'List[int]' rather than
    'list[int]' because the builtin form is only subscriptable from
    Python 3.9, and because 'isinstance(list[int], type)' answers 'True'
    on 3.9 and 3.10 alone, which would route that spelling differently on
    those two versions.
    """
    raised = []

    with self.assertRaises(Exception) as context:
      class Bare:  # noqa
        bar = AttriBox()
    raised.append(context.exception)

    with self.assertRaises(Exception) as context:
      class Generic:  # noqa
        bar = AttriBox[List[int]]([1, 2])
    raised.append(context.exception)

    for exception in raised:
      e = self._unwrapSetName(exception, MissingVariable)
      self.assertIsInstance(e, MissingVariable)
      self.assertEqual(e.varName, '__field_type__')
      self.assertIn(type, e.expectedTypes)

  def test_unsubscripted_box_installed_late(self) -> None:
    """
    Testing that a box with no field type is refused on read when it
    reached the class after creation, through 'setattr', which is the
    one route '__set_name__' never sees.

    The guard in '__get__' is what makes this fail at the access itself.
    Removing it does not change which exception arrives, since
    'getFieldType' raises an identical 'MissingVariable' once '_resolve'
    asks for the field type, so only the frame list tells the two apart.
    """

    class Foo:
      pass

    box = AttriBox()
    setattr(Foo, 'bar', box)

    #  The exception is caught by hand rather than through
    #  'assertRaises', which detaches the traceback with
    #  'with_traceback(None)' to avoid a reference cycle and so leaves
    #  nothing to inspect.
    try:
      _ = Foo().bar
    except MissingVariable as exception:
      e, frames = exception, self._raisingFrames(exception)
    else:  # pragma: no cover (the read above always raises)
      self.fail("""Reading 'bar' should have raised!""")
    self.assertIs(e.instance, box)
    self.assertEqual(e.varName, '__field_type__')
    self.assertIn(type, e.expectedTypes)
    self.assertEqual(frames[-1], '__get__')
    self.assertNotIn('_resolve', frames)
    self.assertNotIn('getFieldType', frames)

    #  Class access is unaffected: the descriptor stays introspectable.
    self.assertIs(Foo.bar, box)

  def test_no_parens_box_declaration(self) -> None:
    """
    Testing that a subscript naming a plain type still yields a working
    attribute when the trailing call is left off. The subscript already
    fixed the field type, so the only thing the missing parentheses
    withheld is the deferred argument list, and '__set_name__' captures
    an empty one on the box's behalf. The result is indistinguishable
    from the declaration written out in full.

    This is the one incomplete spelling that is met with a remedy rather
    than a refusal, because it is the only one where the field type
    survives. A subscript the box declines to claim leaves nothing to
    build from, so those raise instead.
    """

    class Foo:
      bar = AttriBox[int]
      baz = AttriBox[list]

    class Bar:
      bar = AttriBox[int]()
      baz = AttriBox[list]()

    for owner in (Foo, Bar):
      box = owner.__dict__['bar']
      #  The captured arguments are asserted on the private names as
      #  well as through the getters, because the getters route through
      #  'maybe' and answer with the empty default whether or not the
      #  capture ever ran. Only the raw attributes show that
      #  '__set_name__' actually performed it.
      self.assertIsNotNone(box.__pos_args__)
      self.assertEqual(box.__pos_args__, ())
      self.assertIsNotNone(box.__key_args__)
      self.assertEqual(box.__key_args__, dict())
      self.assertEqual(box.getPosArgs(), ())
      self.assertEqual(box.getKeyArgs(), dict())
      self.assertEqual(box.getFieldName(), 'bar')
      self.assertIs(box.getFieldOwner(), owner)
      instance = owner()
      self.assertEqual(instance.bar, 0)
      self.assertEqual(instance.baz, [])
      instance.bar = 7
      self.assertEqual(instance.bar, 7)

    #  The mutable default is owned per instance, not shared.
    first, second = Foo(), Foo()
    first.baz.append(69)
    self.assertEqual(first.baz, [69])
    self.assertEqual(second.baz, [])

  @staticmethod
  def _unwrapSetName(
      exception: BaseException,
      expected: type = PhantomBoxError,
  ) -> BaseException:
    """
    Return the exception a class body raised from '__set_name__'.

    Python 3.7 through 3.11 re-raise it wrapped in a 'RuntimeError' with
    the original on '__cause__', while 3.12 onward propagates it
    unchanged. This reads it back either way, with 'expected' naming the
    class the caller is after, so the wrapper can be told apart from the
    exception it wraps.
    """
    if isinstance(exception, expected):
      return exception
    return exception.__cause__  # pragma: no cover (Python < 3.12)

  def test_no_call_box_declaration(self) -> None:
    """
    Testing that a subscript written without its trailing call is
    refused as the class is created. Such a declaration never produces
    an 'AttriBox' at all: the class body binds the alias the generic
    machinery returned, and '_RootAlias.__set_name__' refuses it at that
    binding, so no broken class ever escapes.
    """
    with self.assertRaises((PhantomBoxError, RuntimeError)) as context:
      class Foo:  # pragma: no cover
        bar = AttriBox[List[int]]
    e = self._unwrapSetName(context.exception)
    self.assertIsInstance(e, PhantomBoxError)
    self.assertIsInstance(e.alias, _RootAlias)
    self.assertEqual(e.fieldName, 'bar')
    self.assertEqual(e.owner.__name__, 'Foo')
    self.assertEqual(str(e), repr(e))
    #  The rendering names the binding and keeps the parameters rather
    #  than collapsing the subscript to the bare origin name.
    self.assertIn('bar = ', str(e))
    self.assertIn('List[int]', str(e))
    self.assertIn('Foo', str(e))

  def test_no_call_box_installed_late(self) -> None:
    """
    Testing that an alias installed on a finished class is refused on
    read. Assigning through 'setattr' never triggers '__set_name__', so
    this is the one route that still reaches '_RootAlias.__get__'. With
    no name ever assigned, the message names none.
    """

    class Foo:
      pass

    alias = AttriBox[List[int]]
    setattr(Foo, 'bar', alias)

    for probe in (lambda: Foo().bar, lambda: Foo.bar):
      with self.assertRaises(PhantomBoxError) as context:
        probe()
      e = context.exception
      self.assertIs(e.alias, alias)
      self.assertIs(e.owner, Foo)
      self.assertIsNone(e.fieldName)
      self.assertEqual(str(e), repr(e))
      self.assertNotIn(' = ', str(e))

  def test_alias_substitution_keeps_class(self) -> None:
    """
    Testing that substituting the 'TypeVar' of a generic subscript
    preserves the '_RootAlias' class. The generic machinery routes that
    substitution through 'copy_with', which without the override rebuilds
    the alias as the plain class and quietly drops the hooks that refuse
    a box declared without its trailing call.
    """
    alias = AttriBox[T]
    self.assertIsInstance(alias, _RootAlias)

    concrete = alias[int]
    self.assertIsInstance(concrete, _RootAlias)
    self.assertIs(concrete.__origin__, AttriBox)
    self.assertEqual(concrete.__args__, (int,))

    #  Both are refused on declaration. The unsubstituted alias still
    #  holds a 'TypeVar', which renders through the 'typing' fallback,
    #  while the substituted one holds a plain type, which renders as a
    #  bare class name. A raw subscript reaches neither path.
    for declared, expected in ((alias, 'T'), (concrete, 'AttriBox[int]')):
      with self.assertRaises((PhantomBoxError, RuntimeError)) as context:
        class Foo:  # pragma: no cover
          bar = declared
      e = self._unwrapSetName(context.exception)
      self.assertIsInstance(e, PhantomBoxError)
      self.assertIn(expected, str(e))

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
    foo.bar = 69, 420
    # noinspection PyUnresolvedReferences
    self.assertAlmostEqual(foo.bar.real, 69)
    # noinspection PyUnresolvedReferences
    self.assertAlmostEqual(foo.bar.imag, 420)
    if TYPE_CHECKING:  # pragma: no cover
      assert isinstance(foo.bar, complex)

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

  def test_prebuilt_value_is_copied_per_instance(self) -> None:
    """
    Testing that a genuine pre-built value of the field type is
    deep-copied rather than shared. Without a sentinel in the deferred
    default, a lone argument already of the field type gives every
    instance its own copy, never the single captured object.
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

    a, b = Holder(), Holder()
    self.assertIsInstance(a.held, Ancestor)
    self.assertIsNot(a.held, seed)
    self.assertIsNot(a.held, b.held)

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

  def test_bad_type(self, ) -> None:
    """
    Testing that passing a non-type to 'AttriBox' raises 'TypeException'.
    """
    susType: str = """I'm a type, trust me bro!"""
    with self.assertRaises(TypeException) as context:
      class Foo:  # pragma: no cover
        bar = AttriBox[int](69)
        good = str(bar)
        # noinspection PyTypeChecker
        bad = AttriBox[susType](420)
    e = context.exception
    self.assertEqual(e.varName, 'fieldType')
    self.assertEqual(e.actualObject, susType)
    self.assertIs(e.actualType, str)
    why: Optional[BaseException] = e.__cause__
    self.assertIsInstance(why, SyntaxError)
