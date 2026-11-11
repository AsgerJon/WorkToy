"""
PromiseOverloadClasses promises how '@overload' meets inheritance,
classmethods and staticmethods, from 'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.meta import MixedMethodKind


class PromiseOverloadClasses(TestCase):
  """
  A subclass overloading a name it inherits keeps the inherited
  declarations and adds its own, a declaration of an equal signature
  replacing the inherited one; a subclass defining the name as another
  kind of method hides the inherited declarations. An overloaded name
  may be a classmethod or a staticmethod, with '@classmethod' or
  '@staticmethod' written above '@overload' or below it; one name
  declared as two kinds of method raises 'MixedMethodKind'. Within one
  class an
  exact match of the classes wins; otherwise the first declaration, in
  the order written, that accepts the arguments as instances wins, so
  the more specific signature is declared first. Source: the docstrings
  of 'overload' and 'Dispatcher'.
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

  def test_mixed_kinds_refused(self) -> None:
    with self.assertRaises(MixedMethodKind) as context:
      class Mixed(BaseObject):
        @classmethod
        @overload(int)
        def make(cls, n: int) -> None:
          pass

        @staticmethod
        @overload(str)
        def make(s: str) -> None:
          pass
    e = context.exception
    self.assertIsInstance(e, SyntaxError)
    self.assertEqual(e.className, 'Mixed')
    self.assertEqual(e.overloadName, 'make')
    self.assertEqual(set(e.kinds), {classmethod, staticmethod})

  def test_instance_and_classmethod_refused(self) -> None:
    with self.assertRaises(MixedMethodKind) as context:
      class Mixed(BaseObject):
        @overload(int)
        def make(self, n: int) -> None:
          pass

        @classmethod
        @overload(str)
        def make(cls, s: str) -> None:
          pass
    self.assertEqual(context.exception.overloadName, 'make')

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
