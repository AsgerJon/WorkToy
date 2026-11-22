"""
RefusedAbstractClasses holds the refusals that belong with
'design.promises.mcls.promise_abstract_classes'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.dispatch import abstract, overload
from worktoy.mcls import BaseObject, ABCMeta
from worktoy.waitaminute.meta import MissingImplementation
from worktoy.waitaminute.meta import WrongImplementation


class RefusedAbstractClasses(TestCase):
  """
  Each of the following is refused, and the exception named is the one
  raised as of 1.3.0. Making an object of an abstract class raises
  'MissingImplementation'. A method written as another kind of method
  than the abstract one, or one that cannot receive what the abstract
  one declares, raises 'WrongImplementation' as its class is created,
  for a method declared plainly and for a signature of an overloaded
  name alike. A function with a body under '@abstract' raises
  'TypeError', and so does '@abstract' in the body of a class that
  'ABCMeta' did not build. Source: the 'ABCMeta' docstring and the
  'abstract' docstring.
  """

  def test_object_of_an_abstract_class(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def rowCount(self) -> int: ...

    with self.assertRaises(Exception) as refused:
      Model()
    self.assertIsInstance(refused.exception, MissingImplementation)

  def test_another_count(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def rowCount(self) -> int: ...

    with self.assertRaises(Exception) as refused:
      class Wrong(Model):
        def rowCount(self, parent: int) -> int: ...
    self.assertIsInstance(refused.exception, WrongImplementation)

  def test_another_kind(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @classmethod
      @abstract
      def make(cls) -> object: ...

    with self.assertRaises(Exception) as refused:
      class Wrong(Model):
        def make(self) -> object: ...
    self.assertIsInstance(refused.exception, WrongImplementation)

  def test_keywords_lost(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @abstract
      def send(self, text: str, *, urgent: bool, **options) -> str: ...

    with self.assertRaises(Exception) as refused:
      class Deaf(Model):
        def send(self, text: str, *, urgent: bool) -> str: ...
    self.assertIsInstance(refused.exception, WrongImplementation)

  def test_overload_short_of_its_signature(self) -> None:
    class Source(BaseObject, metaclass=ABCMeta):
      @overload(str, int)
      @abstract
      def data(self, index: str, role: int) -> str: ...

    with self.assertRaises(Exception) as refused:
      class Plain(Source):
        def data(self, index: str) -> str: ...
    self.assertIsInstance(refused.exception, WrongImplementation)
    with self.assertRaises(Exception) as refused:
      class Loaded(Source):
        @staticmethod
        @overload(str, int)
        def data(index: str, role: int) -> str: ...
    self.assertIsInstance(refused.exception, WrongImplementation)

  def test_body_under_abstract(self) -> None:
    def rowCount(self) -> int:
      return 3

    self.assertEqual(rowCount(None), 3)
    with self.assertRaises(Exception) as refused:
      abstract(rowCount)
    self.assertIsInstance(refused.exception, TypeError)

  def test_abstract_outside_abc_meta(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Plain(BaseObject):
        @abstract
        def rowCount(self) -> int: ...
    self.assertIsInstance(refused.exception, TypeError)
