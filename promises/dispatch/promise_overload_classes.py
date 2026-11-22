"""
PromiseOverloadClasses promises how '@overload' meets inheritance,
classmethods and staticmethods, from 'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.dispatch import overload, Dispatcher
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException


class PromiseOverloadClasses(TestCase):
  """
  A subclass overloading a name it inherits keeps the inherited
  declarations and adds its own, a declaration of an equal signature
  replacing the inherited one; a subclass defining the name as another
  kind of method hides the inherited declarations. An overloaded name
  may be a classmethod or a staticmethod, with '@classmethod' or
  '@staticmethod' written above '@overload' or below it. Within one
  class an
  exact match of the classes wins; otherwise the first declaration, in
  the order written, that accepts the arguments as instances wins, so
  the more specific signature is declared first. From the update after
  1.2.2, one name may hold bound methods, classmethods and staticmethods
  together. Through the class the classmethods and the staticmethods are
  tried, and a bound method is not considered. Through an instance the
  bound methods and the classmethods are tried, and a staticmethod is
  not considered where the name has a bound method. The overload that
  matches receives the instance if it is bound, the class if it is a
  classmethod, and neither if it is static. A bound method and a
  staticmethod at one name may have the same signature. Source: the
  docstrings of 'overload' and 'Dispatcher'.
  """

  def test_subclass_adds_and_replaces(self) -> None:
    class Shape(BaseObject):
      @overload(int)
      def describe(self, n: int) -> str:
        return 'shape int'

      @overload(str)
      def describe(self, s: str) -> str:
        return 'shape str'

    class Square(Shape):
      @overload(int)
      def describe(self, n: int) -> str:
        return 'square int'

    self.assertEqual(Square().describe(1), 'square int')
    self.assertEqual(Square().describe('a'), 'shape str')
    self.assertEqual(Shape().describe(1), 'shape int')

  def test_other_kind_hides(self) -> None:
    class Shape(BaseObject):
      @overload(int)
      def describe(self, n: int) -> str:
        return 'overloaded'

    class Plain(Shape):
      def describe(self, n: int) -> str:
        return 'plain'

    self.assertEqual(Plain().describe(1), 'plain')

  def test_classmethod(self) -> None:
    class Color(BaseObject):
      @classmethod
      @overload(int)
      def make(cls, code: int) -> tuple:
        return cls, code

      @overload(str)
      @classmethod
      def make(cls, name: str) -> tuple:
        return cls, name

    self.assertEqual(Color.make(1), (Color, 1))
    self.assertEqual(Color().make('red'), (Color, 'red'))

  def test_staticmethod(self) -> None:
    class Twice(BaseObject):
      @staticmethod
      @overload(int)
      def double(value: int) -> int:
        return 2 * value

      @overload(str)
      @staticmethod
      def double(value: str) -> str:
        return value + value

    self.assertEqual(Twice.double(2), 4)
    self.assertEqual(Twice().double('ab'), 'abab')

  def test_static_and_bound_of_one_signature(self) -> None:
    class Foo(BaseObject):
      @staticmethod
      @overload(int)
      def bar(value: int) -> tuple:
        return 'static', value

      @overload(int)
      def bar(self, value: int) -> tuple:
        return 'bound', self, value

    foo = Foo()
    self.assertEqual(Foo.bar(69), ('static', 69))
    self.assertEqual(foo.bar(420), ('bound', foo, 420))

  def test_static_and_bound_each_reached_one_way(self) -> None:
    class File(BaseObject):
      @overload()
      def exists(self) -> tuple:
        return 'bound', self

      @staticmethod
      @overload(str)
      def exists(name: str) -> tuple:
        return 'static', name

    file = File()
    self.assertEqual(file.exists(), ('bound', file))
    self.assertEqual(File.exists('notes'), ('static', 'notes'))
    with self.assertRaises(DispatchException) as context:
      file.exists('notes')
    e = context.exception
    self.assertIsInstance(e, TypeError)
    self.assertIs(e.dispatch, vars(File)['exists'])
    self.assertEqual(e.posArgs, ('notes',))
    self.assertEqual(e.keyArgs, {})
    with self.assertRaises(DispatchException) as context:
      File.exists(file)
    e = context.exception
    self.assertIsInstance(e, TypeError)
    self.assertIsInstance(e.dispatch, Dispatcher)
    self.assertEqual(e.posArgs, (file,))
    self.assertEqual(e.keyArgs, {})

  def test_classmethod_and_bound(self) -> None:
    class Color(BaseObject):
      @classmethod
      @overload(str)
      def make(cls, name: str) -> tuple:
        return 'class', cls, name

      @overload(int)
      def make(self, shade: int) -> tuple:
        return 'bound', self, shade

    red = Color()
    self.assertEqual(Color.make('red'), ('class', Color, 'red'))
    self.assertEqual(red.make(3), ('bound', red, 3))
    self.assertEqual(red.make('blue'), ('class', Color, 'blue'))
    with self.assertRaises(DispatchException) as context:
      Color.make(3)
    e = context.exception
    self.assertIsInstance(e, TypeError)
    self.assertIsInstance(e.dispatch, Dispatcher)
    self.assertEqual(e.posArgs, (3,))
    self.assertEqual(e.keyArgs, {})

  def test_static_and_classmethod(self) -> None:
    class Maker(BaseObject):
      @classmethod
      @overload(str)
      def make(cls, name: str) -> tuple:
        return 'class', cls, name

      @staticmethod
      @overload(int)
      def make(number: int) -> tuple:
        return 'static', number

    maker = Maker()
    self.assertEqual(Maker.make('a'), ('class', Maker, 'a'))
    self.assertEqual(Maker.make(1), ('static', 1))
    self.assertEqual(maker.make('a'), ('class', Maker, 'a'))
    self.assertEqual(maker.make(1), ('static', 1))

  def test_all_three_kinds(self) -> None:
    class All(BaseObject):
      @overload(int)
      def f(self, n: int) -> tuple:
        return 'bound', self, n

      @classmethod
      @overload(str)
      def f(cls, s: str) -> tuple:
        return 'class', cls, s

      @staticmethod
      @overload(int)
      def f(n: int) -> tuple:
        return 'static', n

    one = All()
    self.assertEqual(one.f(1), ('bound', one, 1))
    self.assertEqual(All.f(1), ('static', 1))
    self.assertEqual(one.f('s'), ('class', All, 's'))
    self.assertEqual(All.f('s'), ('class', All, 's'))

  def test_first_written_breaks_ties(self) -> None:
    class Pair(BaseObject):
      @overload(int, object)
      def which(self, a, b) -> str:
        return 'int first'

      @overload(object, int)
      def which(self, a, b) -> str:
        return 'int second'

    self.assertEqual(Pair().which(1, 2), 'int first')

  def test_order(self) -> None:
    class Kind(BaseObject):
      @overload(object)
      def kind(self, value: object) -> str:
        return 'object'

      @overload(int)
      def kind(self, value: int) -> str:
        return 'int'

    self.assertEqual(Kind().kind(1), 'int')
    self.assertEqual(Kind().kind(True), 'object')
