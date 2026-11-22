"""
TestABCMeta tests the abstract classes 'ABCMeta' of 'worktoy.mcls'
builds, for methods declared plainly.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import MetaType
from worktoy.core.sentinels import ARGS
from worktoy.dispatch import abstract, overload
from worktoy.mcls import BaseObject, BaseMeta, BaseSpace
from worktoy.mcls import ABCMeta, ABCSpace
from worktoy.mcls.space_hooks import ABCHook
from worktoy.waitaminute.meta import IllegalInstantiation
from worktoy.waitaminute.meta import MissingImplementation
from worktoy.waitaminute.meta import ShadowedClassHook
from . import MclsTest


class TestABCMeta(MclsTest):
  """
  A class built by 'ABCMeta' is abstract while a method declared with
  '@abstract' is not implemented. It is never declared abstract: it is
  so by what is left to write. A subclass may implement any of the
  abstract methods or none, and may declare abstract methods of its
  own. Making an object of an abstract class raises
  'MissingImplementation', a subclass of 'IllegalInstantiation', before
  '__init__' runs. The nearest class along the resolution order that
  binds the name decides, and once a method is implemented the
  declaration holds no further. A call reaching an abstract method does
  nothing. The tests pin each of these for methods declared plainly, as
  bound methods, classmethods and staticmethods.
  """

  def _assertMissing(self, cls: type, *names) -> None:
    """Asserts that 'cls' is abstract for want of 'names'."""
    self.assertEqual(cls.__missing_implementations__, names)
    with self.assertRaises(MissingImplementation) as context:
      cls()
    exception = context.exception
    self.assertIsInstance(exception, IllegalInstantiation)
    self.assertIsInstance(exception, TypeError)
    self.assertIs(exception.cls, cls)
    self.assertEqual(exception.names, names)
    quoted = ', '.join("'%s'" % name for name in names)
    verb = 'is' if len(names) == 1 else 'are'
    expected = ("The class '%s' cannot be instantiated: %s %s declared "
                "abstract and not implemented.") % (
        cls.__name__, quoted, verb)
    self.assertEqual(str(exception), expected)
    self.assertEqual(repr(exception), expected)

  def test_layering(self) -> None:
    self.assertIs(type(ABCMeta), MetaType)
    self.assertIsSubclass(ABCMeta, BaseMeta)
    self.assertIsSubclass(ABCSpace, BaseSpace)
    self.assertIs(ABCMeta.getNamespaceClass(), ABCSpace)
    self.assertIsInstance(ABCSpace.abcHook, ABCHook)
    self.assertIn(ABCSpace.abcHook, ABCSpace.classGetHooks())

  def test_records_are_taken_by_the_namespace(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def run(self) -> str: ...

      @classmethod
      @abstract
      def make(cls) -> object: ...

      @overload(int)
      @abstract
      def scale(self, n: int) -> str: ...

      @abstract
      @overload.flex(int, str, float, bytes)
      def wide(self, n: int, s: str, x: float, b: bytes) -> str: ...

      @overload(ARGS[int])
      @abstract
      def many(self, *n: int) -> str: ...

    space = Model.getNamespace()
    records = (
      Model.__dict__['run'],
      Model.__dict__['make'].__func__,
      space.getOverloads()['scale'][0][1],
      space.getFlexes()['wide'][0][1],
      space.getVariadics()['many'][0][1],
    )
    class More(Model):
      def run(self) -> str:
        """Written here, declared in 'Model'."""

      @staticmethod
      @abstract
      def extra() -> str: ...

    for record in records:
      with self.subTest(record=record):
        self.assertIsInstance(record, abstract)
        self.assertIs(record.__abc_only__, True)
        self.assertIs(record.__declaring_class__, Model)
    extra = More.__dict__['extra'].__func__
    self.assertIs(extra.__declaring_class__, More)

  def test_plain_method(self) -> None:
    built = []

    class Model(BaseObject, metaclass=ABCMeta):
      def __init__(self) -> None:
        built.append(self)

      @abstract
      def rowCount(self) -> int:
        """The number of rows."""

      def name(self) -> str:
        return 'model'

    class Names(Model):
      def rowCount(self) -> int:
        return 3

    class Whole(BaseObject, metaclass=ABCMeta):
      """Declares nothing abstract."""

    self._assertMissing(Model, 'rowCount')
    self.assertEqual(built, [])
    self.assertEqual(Names.__missing_implementations__, ())
    names = Names()
    self.assertEqual(built, [names])
    self.assertEqual(names.rowCount(), 3)
    self.assertEqual(names.name(), 'model')
    self.assertEqual(Whole.__missing_implementations__, ())
    self.assertIsInstance(Whole(), Whole)

  def test_any_or_none(self) -> None:
    class Item(BaseObject, metaclass=ABCMeta):
      @abstract
      def index(self) -> int: ...

      @abstract
      def parent(self) -> int: ...

      @abstract
      def data(self) -> int: ...

    class Quiet(Item):
      """Implements none."""

    class Listed(Item):
      def index(self) -> int:
        return 1

      def parent(self) -> int:
        return 2

    class Named(Listed):
      def data(self) -> int:
        return 3

    self._assertMissing(Item, 'index', 'parent', 'data')
    self._assertMissing(Quiet, 'index', 'parent', 'data')
    self._assertMissing(Listed, 'data')
    named = Named()
    self.assertEqual((named.index(), named.parent(), named.data()),
                     (1, 2, 3))

  def test_subclass_adds_its_own(self) -> None:
    class Base(BaseObject, metaclass=ABCMeta):
      @abstract
      def first(self) -> int: ...

      @abstract
      def second(self) -> int: ...

    class More(Base):
      def first(self) -> int:
        return 1

      @abstract
      def third(self) -> int: ...

    class Done(More):
      def second(self) -> int:
        return 2

      def third(self) -> int:
        return 3

    self._assertMissing(Base, 'first', 'second')
    self._assertMissing(More, 'second', 'third')
    done = Done()
    self.assertEqual((done.first(), done.second(), done.third()), (1, 2, 3))

  def test_declared_again(self) -> None:
    class Base(BaseObject, metaclass=ABCMeta):
      @abstract
      def run(self) -> str: ...

    class Written(Base):
      def run(self) -> str:
        return 'written'

    class Again(Written):
      @abstract
      def run(self) -> str: ...

    class Same(Base):
      @abstract
      def run(self) -> str:
        """Still to be written."""

    self.assertEqual(Written().run(), 'written')
    self._assertMissing(Again, 'run')
    self._assertMissing(Same, 'run')
    self.assertEqual(Same.run.__doc__, 'Still to be written.')

  def test_call_does_nothing(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def rowCount(self) -> int:
        """The number of rows."""

    class Names(Model):
      def rowCount(self) -> int:
        return super().rowCount()

    self.assertIsInstance(Model.__dict__['rowCount'], abstract)
    self.assertEqual(Model.rowCount.__doc__, 'The number of rows.')
    self.assertEqual(Model.rowCount.__name__, 'rowCount')
    self.assertIsNone(Names().rowCount())

  def test_implemented_holds_no_further(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def rowCount(self) -> int: ...

    class Names(Model):
      def rowCount(self) -> int:
        return 3

    class Deeper(Names):
      def rowCount(self, parent: int) -> int:
        return parent

    class Other(Names):
      @staticmethod
      def rowCount() -> int:
        return 7

    self.assertEqual(Names().rowCount(), 3)
    self.assertEqual(Deeper.__missing_implementations__, ())
    self.assertEqual(Deeper().rowCount(5), 5)
    self.assertEqual(Other().rowCount(), 7)

  def test_classmethod_and_staticmethod(self) -> None:
    class Base(BaseObject, metaclass=ABCMeta):
      @classmethod
      @abstract
      def make(cls) -> object: ...

      @abstract
      @classmethod
      def other(cls) -> object: ...

      @staticmethod
      @abstract
      def unit() -> int: ...

    class Sub(Base):
      @classmethod
      def make(cls) -> object:
        return cls

      @classmethod
      def other(cls) -> object:
        return super().other()

      @staticmethod
      def unit() -> int:
        return 1

    self._assertMissing(
        Base, 'classmethod make', 'classmethod other', 'staticmethod unit')
    self.assertIsNone(Base.make())
    self.assertIsNone(Base.unit())
    self.assertIs(Sub.make(), Sub)
    self.assertIsNone(Sub.other())
    self.assertEqual(Sub.unit(), 1)
    self.assertIsInstance(Sub(), Sub)

  def test_nearest_binding_decides(self) -> None:
    class Base(BaseObject, metaclass=ABCMeta):
      @abstract
      def run(self) -> str: ...

    class Mixin:
      def run(self) -> str:
        return 'mixin'

    class Mixed(Mixin, Base):
      """Takes the method of the plain class listed first."""

    class Behind(Base, Mixin):
      """Finds the abstract declaration first."""

    class Left(Base):
      def run(self) -> str:
        return 'left'

    class Right(Base):
      """Implements nothing."""

    class Both(Left, Right):
      """Reaches 'Left' before the declaration."""

    class Turned(Right, Left):
      """Reaches 'Left' before the declaration as well."""

    class Bystander:
      """A plain class holding nothing at the name."""

    class Beside(Bystander, Base):
      """Passes a plain class that does not write the method."""

    self.assertEqual(Mixed().run(), 'mixin')
    self._assertMissing(Behind, 'run')
    self._assertMissing(Beside, 'run')
    self._assertMissing(Right, 'run')
    self.assertEqual(Both().run(), 'left')
    self.assertEqual(Turned().run(), 'left')

  def test_built_from_a_plain_dictionary(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def rowCount(self) -> int: ...

    Bare = ABCMeta('Bare', (Model,), {})
    Rows = ABCMeta('Rows', (Model,), {'rowCount': lambda self: 3})
    self._assertMissing(Bare, 'rowCount')
    self.assertEqual(Rows().rowCount(), 3)

  def test_class_call_hook(self) -> None:
    calls = []

    class Pool(BaseObject, metaclass=ABCMeta):
      @abstract
      def run(self) -> str: ...

      @classmethod
      def __class_call__(cls, *args) -> tuple:
        calls.append(cls)
        return ('hook', cls.__name__, *args)

    class Ready(Pool):
      def run(self) -> str:
        """Written, so the class is whole."""

    self.assertEqual(
        ABCMeta.__dict__['__chained_hooks__'], ('__class_call__',))
    self._assertMissing(Pool, 'run')
    self.assertEqual(calls, [])
    self.assertEqual(Ready(1, 2), ('hook', 'Ready', 1, 2))
    self.assertEqual(calls, [Ready])

  def test_class_call_hook_under_a_metaclass_taking_the_call(self) -> None:
    class Taking(ABCMeta):
      def __call__(cls, *args, **kwargs) -> object:
        """Says nothing of handing the call on."""

    class Quiet(ABCMeta):
      """Writes no '__call__' of its own."""

    class Kept(BaseObject, metaclass=Quiet):
      @classmethod
      def __class_call__(cls, *args) -> tuple:
        return ('kept', *args)

    self.assertEqual(Kept(1), ('kept', 1))
    with self.assertRaises(ShadowedClassHook) as context:
      class Called(BaseObject, metaclass=Taking):
        @classmethod
        def __class_call__(cls, *args) -> str:
          """Never bound: 'Taking' answers the call."""
    self.assertEqual(context.exception.className, 'Called')
    self.assertEqual(context.exception.hookName, '__class_call__')
    self.assertEqual(context.exception.metaclassName, 'Taking')
    self.assertEqual(context.exception.methodName, '__call__')
    self.assertIn("'__class_call__'", str(context.exception))

  def test_only_abc_meta_hosts(self) -> None:
    def plainly() -> None:
      class Plain(BaseObject):
        @abstract
        def run(self) -> str: ...

    def wrapped() -> None:
      class Plain(BaseObject):
        @classmethod
        @abstract
        def run(cls) -> str: ...

    def overloaded() -> None:
      class Plain(BaseObject):
        @overload(int)
        @abstract
        def run(self, n: int) -> str: ...

    def flexed() -> None:
      class Plain(BaseObject):
        @overload.flex(int, str, float, bytes)
        @abstract
        def run(self, n: int, s: str, x: float, b: bytes) -> str: ...

    def tailed() -> None:
      class Plain(BaseObject):
        @overload(ARGS[int])
        @abstract
        def run(self, *n: int) -> str: ...

    for attempt in (plainly, wrapped, overloaded, flexed, tailed):
      with self.subTest(attempt=attempt.__name__):
        with self.assertRaises(TypeError) as context:
          attempt()
        self.assertIn("The class body of 'Plain' declares 'run' abstract",
                      str(context.exception))
        self.assertIn("'BaseMeta'", str(context.exception))

  def test_missing_implementation(self) -> None:
    one = MissingImplementation(int, 'rowCount')
    self.assertIs(one.cls, int)
    self.assertEqual(one.names, ('rowCount',))
    self.assertEqual(
        str(one),
        "The class 'int' cannot be instantiated: 'rowCount' is declared "
        "abstract and not implemented.")
    two = MissingImplementation(int, 'rowCount', 'data(str)')
    self.assertEqual(two.names, ('rowCount', 'data(str)'))
    self.assertEqual(
        str(two),
        "The class 'int' cannot be instantiated: 'rowCount', 'data(str)' "
        "are declared abstract and not implemented.")
    self.assertEqual(repr(two), str(two))
    none = MissingImplementation(int)
    self.assertIs(none.cls, int)
    self.assertEqual(none.names, ())
    self.assertEqual(str(none), "Illegal instantiation of class 'int'")
    self.assertEqual(MissingImplementation.__bases__,
                     (IllegalInstantiation,))
    self.assertEqual(MissingImplementation.__slots__, ('names',))
