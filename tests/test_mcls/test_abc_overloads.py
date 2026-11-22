"""
TestABCOverloads tests the abstract overloads of a class 'ABCMeta' of
'worktoy.mcls' builds.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import abstract, overload
from worktoy.mcls import AbstractMetaclass, BaseObject, ABCMeta
from worktoy.waitaminute.meta import MissingImplementation
from . import MclsTest


class TestABCOverloads(MclsTest):
  """
  An overloaded name is abstract one signature at a time. '@abstract'
  may stand at any position among the '@overload' decorators of a
  stack, and the signatures of one name may be stacked on one blank
  function or spread over several. A subclass implements such a name
  with a plain function at the name, or with every one of its
  signatures; with some of them it stays abstract for the rest, and a
  signature other than a declared one implements nothing. One body may
  hold written and abstract overloads of one name together.
  The tests pin these for concrete, flexible and variadic signatures,
  and for bound methods, classmethods and staticmethods at one name.
  """

  def _assertMissing(self, cls: type, *names) -> None:
    """Asserts that 'cls' is abstract for want of 'names'."""
    self.assertEqual(cls.__missing_implementations__, names)
    with self.assertRaises(MissingImplementation) as context:
      cls()
    self.assertIs(context.exception.cls, cls)
    self.assertEqual(context.exception.names, names)
    for name in names:
      self.assertIn("'%s'" % name, str(context.exception))

  def test_every_signature_or_a_plain_function(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @overload(str, int)
      @abstract
      def data(self, index: str, role: int) -> tuple: ...

      @overload(bytes)
      @overload(str)
      @abstract
      def data(self, index: object) -> tuple:
        """The data at an index."""

    class SubModel(Model):
      @overload(str, int)
      def data(self, *args) -> tuple:
        return ('two', *args)

      @overload(str)
      def data(self, *args) -> tuple:
        return ('text', *args)

      @overload(bytes)
      def data(self, *args) -> tuple:
        return ('raw', *args)

    class Plain(Model):
      def data(self, *args) -> tuple:
        return ('plain', *args)

    class Half(Model):
      @overload(str)
      def data(self, index: str) -> tuple:
        return 'half', index

    class Full(Half):
      @overload(str, int)
      def data(self, index: str, role: int) -> tuple:
        return 'full', index, role

      @overload(bytes)
      def data(self, raw: bytes) -> tuple:
        return 'full', raw

    class Quiet(Model):
      """Implements nothing."""

    self._assertMissing(Model, 'data(str, int)', 'data(str)', 'data(bytes)')
    self._assertMissing(Quiet, 'data(str, int)', 'data(str)', 'data(bytes)')
    self._assertMissing(Half, 'data(str, int)', 'data(bytes)')
    sub = SubModel()
    self.assertEqual(sub.data('a', 1), ('two', 'a', 1))
    self.assertEqual(sub.data('a'), ('text', 'a'))
    self.assertEqual(sub.data(b'a'), ('raw', b'a'))
    self.assertEqual(Plain().data('a', 1), ('plain', 'a', 1))
    full = Full()
    self.assertEqual(full.data('a'), ('half', 'a'))
    self.assertEqual(full.data('a', 1), ('full', 'a', 1))
    self.assertEqual(full.data(b'a'), ('full', b'a'))

  def test_any_position(self) -> None:
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

    class Done(Above):
      @overload(str)
      def data(self, index: str) -> str:
        return index

    self._assertMissing(Below, 'data(str)')
    self._assertMissing(Above, 'data(str)')
    self._assertMissing(Between, 'data(str)', 'data(bytes)')
    self.assertEqual(Done().data('a'), 'a')

  def test_written_and_abstract_in_one_body(self) -> None:
    class First(BaseObject, metaclass=ABCMeta):
      @overload(str)
      @abstract
      def data(self, index: str) -> str: ...

      @overload(str, int)
      def data(self, index: str, role: int) -> str:
        return 'written'

    class Last(BaseObject, metaclass=ABCMeta):
      @overload(str, int)
      def data(self, index: str, role: int) -> str:
        return 'written'

      @overload(str)
      @abstract
      def data(self, index: str) -> str: ...

    class Done(First):
      @overload(str)
      def data(self, index: str) -> str:
        return 'done'

    class Ended(Last):
      @overload(str)
      def data(self, index: str) -> str:
        return 'ended'

    self._assertMissing(First, 'data(str)')
    self._assertMissing(Last, 'data(str)')
    done, ended = Done(), Ended()
    self.assertEqual((done.data('a'), done.data('a', 1)),
                     ('done', 'written'))
    self.assertEqual((ended.data('a'), ended.data('a', 1)),
                     ('ended', 'written'))

  def test_call_does_nothing(self) -> None:
    class Model(BaseObject, metaclass=ABCMeta):
      @overload(str)
      @abstract
      def data(self, index: str) -> str:
        """The data at an index."""

      @overload(str, int)
      @abstract
      def data(self, index: str, role: int) -> str: ...

    class Half(Model):
      @overload(str)
      def data(self, index: str) -> str:
        return 'half'

    class Full(Half):
      @overload(str, int)
      def data(self, index: str, role: int) -> str:
        return super().data(index, role)

    self.assertEqual(Model.data.__doc__, 'The data at an index.')
    full = Full()
    self.assertEqual(full.data('a'), 'half')
    self.assertIsNone(full.data('a', 1))

  def test_kinds_at_one_name(self) -> None:
    class Base(BaseObject, metaclass=ABCMeta):
      @staticmethod
      @overload(int)
      @abstract
      def scale(n: int) -> str: ...

      @overload(int)
      @abstract
      def scale(self, n: int) -> str: ...

      @classmethod
      @abstract
      @overload(str)
      def scale(cls, s: str) -> str: ...

    class Bound(Base):
      @overload(int)
      def scale(self, n: int) -> str:
        """Written through an instance alone."""

    class Whole(Base):
      @staticmethod
      @overload(int)
      def scale(n: int) -> str:
        return 'static'

      @overload(int)
      def scale(self, n: int) -> str:
        return 'bound'

      @classmethod
      @overload(str)
      def scale(cls, s: str) -> str:
        return 'class'

    self._assertMissing(
        Base,
        'staticmethod scale(int)',
        'scale(int)',
        'classmethod scale(str)',
    )
    self._assertMissing(
        Bound,
        'staticmethod scale(int)',
        'classmethod scale(str)',
    )
    self.assertIsNone(Base.scale(2))
    self.assertIsNone(Base.scale('a'))
    self.assertEqual(Whole.scale(2), 'static')
    self.assertEqual(Whole().scale(2), 'bound')
    self.assertEqual(Whole.scale('a'), 'class')

  def test_flexible_and_variadic(self) -> None:
    class Base(BaseObject, metaclass=ABCMeta):
      @overload.flex(int, str)
      @abstract
      def tag(self, n: int, s: str) -> tuple: ...

      @abstract
      @overload.flex(int, str, float, bytes)
      def wide(self, n: int, s: str, x: float, b: bytes) -> tuple: ...

      @overload(str, ARGS[int])
      @abstract
      def many(self, s: str, *n: int) -> tuple: ...

    class Tagged(Base):
      @overload.flex(int, str)
      def tag(self, n: int, s: str) -> tuple:
        return n, s

    class Sub(Tagged):
      @overload.flex(bytes, float, str, int)
      def wide(self, b: bytes, x: float, s: str, n: int) -> tuple:
        return b, x, s, n

      @overload(str, ARGS[int])
      def many(self, s: str, *n: int) -> tuple:
        return (s, *n)

    self._assertMissing(
        Base,
        'tag(int, str)',
        'tag(str, int)',
        'wide(int, str, float, bytes) in any order',
        'many(str, ARGS[int])',
    )
    self._assertMissing(
        Tagged,
        'wide(int, str, float, bytes) in any order',
        'many(str, ARGS[int])',
    )
    self.assertEqual(Sub.__missing_implementations__, ())
    sub = Sub()
    self.assertEqual(sub.tag('a', 1), (1, 'a'))
    self.assertEqual(sub.wide(1, 'a', .5, b'b'), (b'b', .5, 'a', 1))
    self.assertEqual(sub.many('a', 1, 2), ('a', 1, 2))

  def test_plain_declaration_written_with_overloads(self) -> None:
    class Base(BaseObject, metaclass=ABCMeta):
      @abstract
      def data(self, index: str, role: int) -> tuple: ...

      @abstract
      def rest(self, *args) -> tuple: ...

    class Loaded(Base):
      @overload(str)
      def data(self, index: str) -> tuple:
        return (index,)

      @overload(str, int)
      def data(self, index: str, role: int) -> tuple:
        return index, role

      @overload(str, ARGS[int])
      def rest(self, s: str, *n: int) -> tuple:
        return (s, *n)

      @overload(ARGS[int])
      def rest(self, *n: int) -> tuple:
        return n

    class Counted(Base):
      data = overload(bytes)(len)

      @overload(str, int)
      def data(self, index: str, role: int) -> tuple:
        return index, role

      @overload(ARGS[int])
      def rest(self, *n: int) -> tuple:
        """Takes any number."""

    class Again(Base):
      @overload(str, int)
      @abstract
      def data(self, index: str, role: int) -> tuple: ...

      def rest(self, *args) -> tuple:
        """Takes any number."""

    self._assertMissing(Base, 'data', 'rest')
    loaded = Loaded()
    self.assertEqual(loaded.data('a'), ('a',))
    self.assertEqual(loaded.data('a', 1), ('a', 1))
    self.assertEqual(loaded.rest('a', 1), ('a', 1))
    self.assertEqual(loaded.rest(1, 2), (1, 2))
    self.assertEqual(Counted.__missing_implementations__, ())
    self.assertEqual(Counted().data('a', 1), ('a', 1))
    self._assertMissing(Again, 'data(str, int)')

  def test_overloads_declared_again(self) -> None:
    class Base(BaseObject, metaclass=ABCMeta):
      @overload(str)
      @abstract
      def data(self, index: str) -> str: ...

    class Written(Base):
      @overload(str)
      def data(self, index: str) -> str:
        return 'written'

    class Again(Written):
      @overload(str)
      @abstract
      def data(self, index: str) -> str: ...

    class Plainly(Base):
      @abstract
      def data(self, *args) -> str: ...

    class Left(Base):
      @overload(str)
      def data(self, index: str) -> str:
        return 'left'

    class Right(Base):
      """Implements nothing."""

    class Both(Right, Left):
      """Reaches 'Left' before the declaration."""

    class Loose(metaclass=AbstractMetaclass):
      """Built in a namespace that registers no overloads."""

    class Mixed(Loose, Base):
      """Reaches a class that cannot have written the overload."""

    class Partly(Base):
      @overload(str)
      @abstract
      def data(self, index: str) -> str: ...

      @overload(str, int)
      def data(self, index: str, role: int) -> str:
        """Another signature, written beside the one declared again."""

    class Tail(BaseObject, metaclass=ABCMeta):
      @overload(str, ARGS[int])
      @abstract
      def many(self, s: str, *n: int) -> tuple: ...

    class Still(Tail):
      @overload(str, ARGS[int])
      @abstract
      def many(self, s: str, *n: int) -> tuple: ...

      @overload(int)
      def many(self, n: int) -> tuple:
        """Another signature, written beside the one declared again."""

    self.assertEqual(Written().data('a'), 'written')
    self._assertMissing(Again, 'data(str)')
    self._assertMissing(Plainly, 'data')
    self.assertEqual(Both().data('a'), 'left')
    self._assertMissing(Mixed, 'data(str)')
    self._assertMissing(Partly, 'data(str)')
    self._assertMissing(Still, 'many(str, ARGS[int])')

  def test_another_signature_implements_nothing(self) -> None:
    class Base(BaseObject, metaclass=ABCMeta):
      @overload.flex(int, str)
      @abstract
      def tag(self, n: int, s: str) -> tuple: ...

      @overload(str, ARGS[int])
      @abstract
      def many(self, s: str, *n: int) -> tuple: ...

      @overload(str, int, ARGS[int])
      @abstract
      def lead(self, s: str, n: int, *rest: int) -> tuple: ...

      @overload.flex(int, str, float, bytes)
      @abstract
      def wide(self, n: int, s: str, x: float, b: bytes) -> tuple: ...

      @overload.flex(int, str, float, bytes, bool)
      @abstract
      def five(
          self, n: int, s: str, x: float, b: bytes, t: bool,
      ) -> tuple: ...

    class OneOrder(Base):
      @overload(int, str)
      def tag(self, n: int, s: str) -> tuple:
        """One of the two orders."""

    class OtherTail(Base):
      @overload(int)
      def many(self, n: int) -> tuple:
        """A signature the base did not declare."""

    class MoreClasses(Base):
      @overload.flex(int, str, float, bytes, bool)
      def wide(
          self, n: int, s: str, x: float, b: bytes, t: bool,
      ) -> tuple:
        """The declared classes and one more."""

    class FewerClasses(Base):
      @overload.flex(int, str, float, bytes)
      def five(self, n: int, s: str, x: float, b: bytes) -> tuple:
        """The declared classes but one."""

    class FixedOrder(Base):
      @staticmethod
      @overload(int, str, float, bytes)
      def wide(n: int, s: str, x: float, b: bytes) -> tuple:
        return n, s, x, b

    every = (
      'tag(int, str)',
      'tag(str, int)',
      'wide(int, str, float, bytes) in any order',
      'five(int, str, float, bytes, bool) in any order',
      'many(str, ARGS[int])',
      'lead(str, int, ARGS[int])',
    )
    self._assertMissing(Base, *every)
    self._assertMissing(OneOrder, *every[1:])
    self._assertMissing(OtherTail, *every)
    self._assertMissing(MoreClasses, *every)
    self._assertMissing(FewerClasses, *every)
    self._assertMissing(FixedOrder, *every)
    self.assertEqual(FixedOrder.wide(1, 'a', .5, b'b'), (1, 'a', .5, b'b'))

  def test_plain_declaration_written_flexibly(self) -> None:
    class Base(BaseObject, metaclass=ABCMeta):
      @abstract
      def wide(self, n: int, s: str, x: float, b: bytes) -> tuple: ...

    class Loose(Base):
      @overload.flex(int, str, float, bytes)
      def wide(self, n: int, s: str, x: float, b: bytes) -> tuple:
        return n, s, x, b

    class Pair(BaseObject, metaclass=ABCMeta):
      @abstract
      def tag(self, n: int, s: str) -> tuple: ...

    class Either(Pair):
      @overload.flex(int, str)
      def tag(self, n: int, s: str) -> tuple:
        return n, s

    self._assertMissing(Base, 'wide')
    self.assertEqual(Loose.__missing_implementations__, ())
    self.assertEqual(Loose().wide(b'b', .5, 'a', 1), (1, 'a', .5, b'b'))
    self.assertEqual(Either.__missing_implementations__, ())
    self.assertEqual(Either().tag('a', 1), (1, 'a'))
