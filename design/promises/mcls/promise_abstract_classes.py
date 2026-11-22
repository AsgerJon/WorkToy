"""
PromiseAbstractClasses promises the abstract classes 'ABCMeta' of
'worktoy.mcls' builds, with '@abstract' of 'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.dispatch import abstract, overload
from worktoy.mcls import BaseObject, ABCMeta, ABCObject


class PromiseAbstractClasses(TestCase):
  """
  From 1.3.0, a class built by 'ABCMeta' declares a method with
  '@abstract' over a function with no body, and the classes based on it
  have to write that method. 'ABCObject' is 'BaseObject' built by
  'ABCMeta', so a class based on it is such a class without naming the
  metaclass. A class is abstract for as long as a method
  it declares or inherits is not written; it is never declared abstract.
  A subclass may write any of the abstract methods or none, and may
  declare abstract methods of its own, so it may be abstract in turn,
  and an object is made of a class once nothing is left. A method
  written is the same kind of method as the abstract one, a bound
  method, a classmethod or a staticmethod, and receives what that one
  declares: as many arguments by position, a default changing nothing,
  or any number through '*args'; '**kwargs' where the abstract method
  takes '**kwargs'; and each keyword-only parameter of the abstract
  method by the same parameter or by '**kwargs'. An overloaded name is
  abstract one signature at a time: '@abstract' stands at any position
  among the '@overload' decorators of a stack, and a subclass writes the
  name with a plain function at the name or with every one of its
  signatures, a further subclass writing what an earlier one left. A
  call reaching an abstract method does nothing, and once a class has
  written a method, a class based on it overrides that method as in any
  class. Source: the 'ABCMeta' docstring and the 'abstract' docstring.
  """

  def test_written_by_a_subclass(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def rowCount(self) -> int:
        """The number of rows."""

      def describe(self) -> str:
        return '%d rows' % self.rowCount()

    class Names(Model):
      def rowCount(self) -> int:
        return 3

    self.assertEqual(Names().describe(), '3 rows')

  def test_based_on_abc_object(self) -> None:
    class Model(ABCObject):
      @abstract
      def rowCount(self) -> int: ...

    class Names(Model):
      def rowCount(self) -> int:
        return 3

    self.assertIsInstance(ABCObject, ABCMeta)
    self.assertIsInstance(Model, ABCMeta)
    with self.assertRaises(Exception):
      Model()
    self.assertEqual(Names().rowCount(), 3)
    self.assertIsInstance(Names(), BaseObject)

  def test_any_or_none_and_more(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def rowCount(self) -> int: ...

      @abstract
      def title(self) -> str: ...

    class Quiet(Model):
      """Writes none."""

    class Table(Quiet):
      def title(self) -> str:
        return 'table'

      @abstract
      def columnCount(self) -> int: ...

    class Grid(Table):
      def rowCount(self) -> int:
        return 2

      def columnCount(self) -> int:
        return 5

    for cls in (Model, Quiet, Table):
      with self.subTest(cls=cls.__name__):
        with self.assertRaises(Exception):
          cls()
    grid = Grid()
    self.assertEqual((grid.title(), grid.rowCount(), grid.columnCount()),
                     ('table', 2, 5))

  def test_what_an_implementation_takes(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def data(self, index: str, role: int) -> tuple: ...

      @abstract
      def send(self, text: str, *, urgent: bool, **options) -> tuple: ...

    class Same(Model):
      def data(self, index: str = 'a', role: int = 0) -> tuple:
        return index, role

      def send(self, text: str, *, urgent: bool, **options) -> tuple:
        return text, urgent

    class Open(Model):
      def data(self, *args) -> tuple:
        return args

      def send(self, text: str, **kwargs) -> tuple:
        return text, kwargs['urgent']

    for cls in (Same, Open):
      with self.subTest(cls=cls.__name__):
        self.assertEqual(cls().data('b', 2), ('b', 2))
        self.assertEqual(cls().send('c', urgent=True), ('c', True))

  def test_kinds(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @classmethod
      @abstract
      def make(cls) -> object: ...

      @abstract
      @staticmethod
      def unit() -> int: ...

    class Made(Model):
      @classmethod
      def make(cls) -> object:
        return cls()

      @staticmethod
      def unit() -> int:
        return 1

    self.assertIsInstance(Made.make(), Made)
    self.assertEqual(Made.unit(), 1)

  def test_overloaded_name(self) -> None:
    class Source(BaseObject, metaclass=ABCMeta):
      @overload(str, int)
      @abstract
      def data(self, index: str, role: int) -> str: ...

      @overload(bytes)
      @overload(str)
      @abstract
      def data(self, index: object) -> str: ...

    class Loose(Source):
      def data(self, *args) -> tuple:
        return args

    class Half(Source):
      @overload(str)
      def data(self, index: str) -> str:
        return 'text'

    class Full(Half):
      @overload(str, int)
      def data(self, index: str, role: int) -> str:
        return 'text and role'

      @overload(bytes)
      def data(self, index: bytes) -> str:
        return 'bytes'

    self.assertEqual(Loose().data('a', 1), ('a', 1))
    for cls in (Source, Half):
      with self.subTest(cls=cls.__name__):
        with self.assertRaises(Exception):
          cls()
    full = Full()
    self.assertEqual(full.data('a'), 'text')
    self.assertEqual(full.data('a', 1), 'text and role')
    self.assertEqual(full.data(b'a'), 'bytes')

  def test_any_position_among_overloads(self) -> None:
    class Below(BaseObject, metaclass=ABCMeta):
      @overload(str)
      @abstract
      def data(self, index: str) -> str: ...

    class Above(BaseObject, metaclass=ABCMeta):
      @abstract
      @overload(str)
      def data(self, index: str) -> str: ...

    class Between(BaseObject, metaclass=ABCMeta):
      @overload(bytes)
      @abstract
      @overload(str)
      def data(self, index: object) -> str: ...

    for base in (Below, Above, Between):
      with self.subTest(base=base.__name__):
        with self.assertRaises(Exception):
          base()

        class Written(base):
          @overload(bytes)
          @overload(str)
          def data(self, index: object) -> str:
            return 'written'

        self.assertEqual(Written().data('a'), 'written')

  def test_call_does_nothing(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def rowCount(self) -> int: ...

    class Names(Model):
      def rowCount(self) -> int:
        return super().rowCount()

    self.assertIsNone(Names().rowCount())

  def test_written_holds_no_further(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def rowCount(self) -> int: ...

    class Names(Model):
      def rowCount(self) -> int:
        return 3

    class Deeper(Names):
      def rowCount(self, parent: int) -> int:
        return parent

    self.assertEqual(Deeper().rowCount(5), 5)
